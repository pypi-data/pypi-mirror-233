""" This is the main module that interprets DIRAC cfg format"""
from __future__ import annotations

import copy
import os
import re
import zipfile
import threading

from threading import Lock, RLock
from typing import Generic, Literal, TypeVar, overload, Callable, Union, TYPE_CHECKING, cast
from collections.abc import Iterator

if TYPE_CHECKING:
    from typing_extensions import TypedDict, ParamSpec, NotRequired
    from _typeshed import StrOrBytesPath

    T = TypeVar("T")
    P = ParamSpec("P")

    class DOKReturnType(TypedDict, Generic[T]):
        OK: Literal[True]
        Value: T

    class DErrorReturnType(TypedDict):
        OK: Literal[False]
        Message: str

    DReturnType = Union[DOKReturnType[T], DErrorReturnType]

    class CFGKeySection(TypedDict):
        key: str
        value: CFG
        comment: str
        levelsBelow: NotRequired[str]

    class CFGKey(TypedDict):
        key: str
        value: CFG | str
        comment: str
        levelsBelow: NotRequired[str]

    CFGAsDict = dict[str, Union["CFGAsDict", str]]

    ModificationType = Union[
        tuple[Literal["delOpt", "delSec"], str, int, str],
        tuple[Literal["addOpt", "modOpt", "addSec"], str, int, str, str],
        tuple[Literal["modSec"], str, int, list["ModificationType"], str],
    ]


def S_ERROR(messageString: str = "") -> DErrorReturnType:
    return {"OK": False, "Message": str(messageString)}


# mypy doesn't understand default parameter values with generics so use overloads (python/mypy#3737)
@overload
def S_OK() -> DOKReturnType[Literal[""]]:
    ...


@overload
def S_OK(value: T) -> DOKReturnType[T]:
    ...


def S_OK(value=""):  # type: ignore
    return {"OK": True, "Value": value}


class ListDummy:
    def fromChar(self, inputString: str, sepChar: str = ",") -> list[str]:
        # to prevent getting an empty String as argument
        if not (isinstance(inputString, str) and isinstance(sepChar, str) and sepChar):
            # This makes no sense so just ignore type checking here
            return None  # type: ignore

        return [fieldString.strip() for fieldString in inputString.split(sepChar) if len(fieldString.strip()) > 0]


List: ListDummy = ListDummy()


class Synchronizer:
    """Class encapsulating a lock
    allowing it to be used as a synchronizing
    decorator making the call thread-safe"""

    lockName: str
    lock: Lock | RLock

    def __init__(self, lockName: str = "", recursive: bool = False) -> None:
        envVar = os.environ.get("DIRAC_FEWER_CFG_LOCKS", "no").lower()
        self.__locksEnabled = envVar not in ("y", "yes", "t", "true", "on", "1")
        if self.__locksEnabled:
            self.lockName = lockName
            if recursive:
                self.lock = threading.RLock()
            else:
                self.lock = threading.Lock()

    def __call__(self, funcToCall: Callable[P, T]) -> Callable[P, T]:
        if not self.__locksEnabled:
            return funcToCall

        def lockedFunc(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                if self.lockName:
                    print("LOCKING", self.lockName)
                self.lock.acquire()
                return funcToCall(*args, **kwargs)
            finally:
                if self.lockName:
                    print("UNLOCKING", self.lockName)
                self.lock.release()

        return lockedFunc


gCFGSynchro: Synchronizer = Synchronizer(recursive=True)


class CFG:
    def __init__(self) -> None:
        """
        Constructor
        """
        self.__orderedList: list[str] = []
        self.__commentDict: dict[str, str] = {}
        self.__dataDict: dict[str, CFG | str] = {}
        self.reset()

    @gCFGSynchro
    def reset(self) -> None:
        """
        Empty the CFG
        """
        self.__orderedList = []
        self.__commentDict = {}
        self.__dataDict = {}

    @gCFGSynchro
    def createNewSection(
        self, sectionName: str, comment: str = "", contents: CFG | None = None
    ) -> DErrorReturnType | CFG:
        """
        Create a new section

        :type sectionName: string
        :param sectionName: Name of the section
        :type comment: string
        :param comment: Comment for the section
        :type contents: CFG
        :param contents: Optional cfg with the contents of the section.
        """
        if sectionName == "":
            raise ValueError("Creating a section with empty name! You shouldn't do that!")
        if sectionName.find("/") > -1:
            recDict = self.getRecursive(sectionName, -1)
            if not recDict:
                return S_ERROR(f"Parent section does not exist {sectionName}")
            parentSection = recDict["value"]
            if isinstance(parentSection, str):
                raise KeyError(f"Entry {recDict['key']} doesn't seem to be a section")
            return parentSection.createNewSection(recDict["levelsBelow"], comment, contents)
        self.__addEntry(sectionName, comment)
        if sectionName not in self.__dataDict:
            if not contents:
                contents = CFG()
            self.__dataDict[sectionName] = contents
        else:
            raise KeyError(f"{sectionName} key already exists")
        return contents

    @gCFGSynchro
    def setOption(self, optionName: str, value: str, comment: str = "") -> DErrorReturnType | None:
        """
        Create a new option.

        :type optionName: string
        :param optionName: Name of the option to create
        :type value: string
        :param value: Value of the option
        :type comment: string
        :param comment: Comment for the option
        """
        if optionName == "":
            raise ValueError("Creating an option with empty name! You shouldn't do that!")
        if optionName.find("/") > -1:
            recDict = self.getRecursive(optionName, -1)
            if not recDict:
                return S_ERROR(f"Parent section does not exist {optionName}")
            parentSection = recDict["value"]
            if isinstance(parentSection, str):
                raise KeyError(f"Entry {recDict['key']} doesn't seem to be a section")
            return parentSection.setOption(recDict["levelsBelow"], value, comment)
        self.__addEntry(optionName, comment)
        self.__dataDict[optionName] = str(value)
        return None

    def __addEntry(self, entryName: str, comment: str) -> None:
        """
        Add an entry and set the comment

        :type entryName: string
        :param entryName: Name of the entry
        :type comment: string
        :param comment: Comment for the entry
        """
        if entryName not in self.__orderedList:
            self.__orderedList.append(entryName)
        self.__commentDict[entryName] = comment

    def existsKey(self, key: str) -> bool:
        """
        Check if an option/section with that name exists

        :type key: string
        :param key: Name of the option/section to check
        :return: Boolean with the result
        """
        return key in self.__orderedList

    def sortAlphabetically(self, ascending: bool = True) -> bool:
        """
        Order this cfg alphabetically
        returns True if modified
        """
        if not ascending:
            return self.sortByKey(reverse=True)
        return self.sortByKey()

    def sortByKey(self, key: Callable[[str], bool] | None = None, reverse: bool = False) -> bool:
        """
        Order this cfg by function refered in key, default is None
        corresponds to alphabetic sort
        returns True if modified
        """
        unordered = list(self.__orderedList)
        self.__orderedList.sort(key=key, reverse=reverse)
        return unordered != self.__orderedList

    @gCFGSynchro
    def deleteKey(self, key: str) -> bool:
        """
        Delete an option/section

        :type key: string
        :param key: Name of the option/section to delete
        :return: Boolean with the result
        """
        result = self.getRecursive(key, -1)
        if not result:
            raise KeyError(f"{'/'.join(List.fromChar(key, '/')[:-1])} does not exist")
        cfg = result["value"]
        end = result["levelsBelow"]

        if end in cfg.__orderedList:
            del cfg.__commentDict[end]
            del cfg.__dataDict[end]
            cfg.__orderedList.remove(end)
            return True
        return False

    @gCFGSynchro
    def copyKey(self, oldName: str, newName: str) -> bool:
        """
        Copy an option/section

        :type oldName: string
        :param oldName: Name of the option / section to copy
        :type newName: string
        :param newName: Destination name
        :return: Boolean with the result
        """
        if oldName == newName:
            return True
        result = self.getRecursive(oldName, -1)
        if not result:
            raise KeyError(f"{'/'.join(List.fromChar(oldName, '/')[:-1])} does not exist")
        oldCfg = result["value"]
        oldEnd = result["levelsBelow"]
        if oldEnd in oldCfg.__dataDict:
            result = self.getRecursive(newName, -1)
            if not result:
                raise KeyError(f"{'/'.join(List.fromChar(newName, '/')[:-1])} does not exist")
            newCfg = result["value"]
            newEnd = result["levelsBelow"]

            newCfg.__dataDict[newEnd] = oldCfg.__dataDict[oldEnd]
            newCfg.__commentDict[newEnd] = oldCfg.__commentDict[oldEnd]
            refKeyPos = oldCfg.__orderedList.index(oldEnd)
            newCfg.__orderedList.insert(refKeyPos + 1, newEnd)

            return True
        else:
            return False

    @gCFGSynchro
    def listOptions(self, ordered: bool = True) -> list[str]:
        """
        List options

        :type ordered: boolean
        :param ordered: Return the options ordered. By default is False
        :return: List with the option names
        """
        if ordered:
            return [sKey for sKey in self.__orderedList if isinstance(self.__dataDict[sKey], str)]
        else:
            return [sKey for sKey in self.__dataDict.keys() if isinstance(self.__dataDict[sKey], str)]

    @gCFGSynchro
    def listSections(self, ordered: bool = True) -> list[str]:
        """
        List subsections

        :type ordered: boolean
        :param ordered: Return the subsections ordered. By default is False
        :return: List with the subsection names
        """
        if ordered:
            return [sKey for sKey in self.__orderedList if not isinstance(self.__dataDict[sKey], str)]
        else:
            return [sKey for sKey in self.__dataDict.keys() if not isinstance(self.__dataDict[sKey], str)]

    @gCFGSynchro
    def isSection(self, key: str) -> bool:
        """
        Return if a section exists

        :type key: string
        :param key: Name to check
        :return: Boolean with the results
        """
        if key.find("/") != -1:
            keyDict = self.getRecursive(key, -1)
            if not keyDict:
                return False
            section = keyDict["value"]
            if isinstance(section, str):
                return False
            secKey = keyDict["levelsBelow"]
            return section.isSection(secKey)
        return key in self.__dataDict and not isinstance(self.__dataDict[key], str)

    @gCFGSynchro
    def isOption(self, key: str) -> bool:
        """
        Return if an option exists

        :type key: string
        :param key: Name to check
        :return: Boolean with the results
        """
        if key.find("/") != -1:
            keyDict = self.getRecursive(key, -1)
            if not keyDict:
                return False
            section = keyDict["value"]
            if isinstance(section, str):
                return False
            secKey = keyDict["levelsBelow"]
            return section.isOption(secKey)
        return key in self.__dataDict and isinstance(self.__dataDict[key], str)

    def listAll(self) -> list[str]:
        """
        List all sections and options

        :return: List with names of all options and subsections
        """
        return self.__orderedList

    def __recurse(self, pathList: list[str]) -> CFGKey | Literal[False]:
        """
        Explore recursively a path

        :type pathList: list
        :param pathList: List containing the path to explore
        :return: Dictionary with the contents { key, value, comment }
        """
        if pathList[0] in self.__dataDict:
            value = self.__dataDict[pathList[0]]
            if len(pathList) == 1:
                return {
                    "key": pathList[0],
                    "value": value,
                    "comment": self.__commentDict[pathList[0]],
                }
            if isinstance(value, CFG):
                return value.__recurse(pathList[1:])
        return False

    @overload
    def getRecursive(self, path: str, levelsAbove: Literal[-1]) -> CFGKeySection | None:
        ...

    @overload
    def getRecursive(self, path: str, levelsAbove: Literal[0] = 0) -> CFGKey | None:
        ...

    @gCFGSynchro
    def getRecursive(self, path: str, levelsAbove: int = 0) -> CFGKey | CFGKeySection | None:
        """
        Get path contents

        :type path: string
        :param path: Path to explore recursively and get the contents
        :type levelsAbove: integer
        :param levelsAbove: Number of children levels in the path that won't be explored.
                            For instance, to explore all sections in a path except the last one use
                            levelsAbove = 1
        :return: Dictionary containing:
                    key -> name of the entry
                    value -> content of the key
                    comment -> comment of the key
        """
        pathList = [dirName.strip() for dirName in path.split("/") if not dirName.strip() == ""]
        levelsAbove = abs(levelsAbove)
        if len(pathList) - levelsAbove < 0:
            return None
        if len(pathList) - levelsAbove == 0:
            lBel = ""
            if levelsAbove > 0:
                lBel = "/".join(pathList[len(pathList) - levelsAbove :])
            return {"key": "", "value": self, "comment": "", "levelsBelow": lBel}
        levelsBelow = ""
        if levelsAbove > 0:
            levelsBelow = "/".join(pathList[-levelsAbove:])
            pathList = pathList[:-levelsAbove]
        retDict = self.__recurse(pathList)
        if not retDict:
            return None
        retDict["levelsBelow"] = levelsBelow
        return retDict

    @overload
    def getOption(self, opName: str, defaultValue: None = ...) -> str | None:
        ...

    @overload
    def getOption(self, opName: str, defaultValue: list[str]) -> list[str]:
        ...

    @overload
    def getOption(self, opName: str, defaultValue: bool) -> bool:
        ...

    def getOption(self, opName, defaultValue=None):  # type: ignore
        """
        Get option value with default applied

        :type opName: string
        :param opName: Path to the option to retrieve
        :type defaultValue: optional (any python type)
        :param defaultValue: Default value for the option if the option is not defined.
                             If the option is defined, the value will be returned casted to
                             the type of defaultValue if it is defined.
        :return: Value of the option casted to defaultValue type, or defaultValue
        """
        levels = List.fromChar(opName, "/")

        dataD: CFG | str = self
        while len(levels) > 0:
            assert isinstance(dataD, CFG), (opName, dataD)
            try:
                val = dataD[levels.pop(0)]
            except KeyError:
                return defaultValue
            if val is False:
                return defaultValue
            dataV = val
            dataD = dataV

        if not isinstance(dataV, str):
            optionValue = defaultValue
        else:
            optionValue = dataV

        # Return value if existing, defaultValue if not
        if optionValue == defaultValue:
            if defaultValue is None or isinstance(defaultValue, type):
                return defaultValue
            return optionValue

        # Value has been returned from the configuration
        if defaultValue is None:
            return optionValue

        # Casting to defaultValue's type
        defaultType = defaultValue
        if not isinstance(defaultValue, type):
            defaultType = type(defaultValue)

        if defaultType == list:
            try:
                return List.fromChar(optionValue, ",")
            except Exception:
                return defaultValue
        elif defaultType == bool:
            try:
                return optionValue.lower() in ("y", "yes", "true", "1")
            except Exception:
                return defaultValue
        else:
            try:
                return defaultType(optionValue)
            except Exception:
                return defaultValue

    def getAsCFG(self, path: str = "") -> CFG:
        """Return subsection as CFG object.

        :param str path: Path to the section
        :return: CFG object, of path is not found the CFG is empty
        """
        if not path:
            return self.clone()
        splitPath = path.lstrip("/").split("/")
        basePath = splitPath[0]
        remainingPath = splitPath[1:]
        if basePath not in self.__dataDict:
            return CFG()
        section = self.__dataDict[basePath]
        if not isinstance(section, CFG):
            raise ValueError(f"Path {path} is not a section")
        return section.getAsCFG("/".join(remainingPath))

    def getAsDict(self, path: str = "") -> CFGAsDict:
        """
        Get the contents below a given path as a dict

        :type path: string
        :param path: Path to retrieve as dict
        :return: Dictionary containing the data

        """
        resVal: CFGAsDict = {}
        if path:
            reqDict = self.getRecursive(path)
            if not reqDict:
                return resVal
            keyCfg = reqDict["value"]
            if isinstance(keyCfg, str):
                return resVal
            return keyCfg.getAsDict()
        for op in self.listOptions():
            resVal[op] = cast(str, self[op])
        for sec in self.listSections():
            resVal[sec] = cast(CFG, self[sec]).getAsDict()
        return resVal

    @gCFGSynchro
    def appendToOption(self, optionName: str, value: str) -> None:
        """
        Append a value to an option prepending a comma
        # Doesn't actually append commas!

        :type optionName: string
        :param optionName: Name of the option to append the value
        :type value: string
        :param value: Value to append to the option
        """
        result = self.getRecursive(optionName, -1)
        if not result:
            raise KeyError(f"{'/'.join(List.fromChar(optionName, '/')[:-1])} does not exist")
        cfg = result["value"]
        end = result["levelsBelow"]
        if end not in cfg.__dataDict:
            raise KeyError(f"Option {end} has not been declared")
        current_value = cfg.__dataDict[end]
        if not isinstance(current_value, str):
            raise ValueError(f"Option {end} is not a string")
        cfg.__dataDict[end] = current_value + str(value)

    @gCFGSynchro
    def addKey(self, key: str, value: str | CFG, comment: str, beforeKey: str = "") -> None:
        """
        Add a new entry (option or section)

        :type key: string
        :param key: Name of the option/section to add
        :type value: string/CFG
        :param value: Contents of the new option/section
        :type comment: string
        :param comment: Comment for the option/section
        :type beforeKey: string
        :param beforeKey: Name of the option/section to add the entry above. By default
                            the new entry will be added at the end.
        """
        result = self.getRecursive(key, -1)
        if not result:
            raise KeyError(f"{'/'.join(List.fromChar(key, '/')[:-1])} does not exist")
        cfg = result["value"]
        end = result["levelsBelow"]
        if end in cfg.__dataDict:
            raise KeyError(f"{key} already exists")
        cfg.__dataDict[end] = value
        cfg.__commentDict[end] = comment
        if beforeKey == "":
            cfg.__orderedList.append(end)
        else:
            refKeyPos = cfg.__orderedList.index(beforeKey)
            cfg.__orderedList.insert(refKeyPos, end)

    @gCFGSynchro
    def renameKey(self, oldName: str, newName: str) -> bool:
        """
        Rename a option/section

        :type oldName: string
        :param oldName: Name of the option/section to change
        :type newName: string
        :param newName: New name of the option/section
        :return: Boolean with the result of the rename
        """
        if oldName == newName:
            return True
        result = self.getRecursive(oldName, -1)
        if not result:
            raise KeyError(f"{'/'.join(List.fromChar(oldName, '/')[:-1])} does not exist")
        oldCfg = result["value"]
        oldEnd = result["levelsBelow"]
        if oldEnd in oldCfg.__dataDict:
            result = self.getRecursive(newName, -1)
            if not result:
                raise KeyError(f"{'/'.join(List.fromChar(newName, '/')[:-1])} does not exist")
            newCfg = result["value"]
            newEnd = result["levelsBelow"]

            newCfg.__dataDict[newEnd] = oldCfg.__dataDict[oldEnd]
            newCfg.__commentDict[newEnd] = oldCfg.__commentDict[oldEnd]
            refKeyPos = oldCfg.__orderedList.index(oldEnd)
            oldCfg.__orderedList.remove(oldEnd)
            newCfg.__orderedList.insert(refKeyPos, newEnd)

            del oldCfg.__dataDict[oldEnd]
            del oldCfg.__commentDict[oldEnd]
            return True
        else:
            return False

    # def __getitem__(self, key: str) -> CFG | str | Literal[False]:
    def __getitem__(self, key: str) -> CFG | str:
        """
        Get the contents of a section/option

        :type key: string
        :param key: Name of the section/option to retrieve
        :return: String/CFG with the contents
        """
        if key.find("/") > -1:
            subDict = self.getRecursive(key)
            if not subDict:
                return False  # type: ignore
                # raise KeyError(key)
            return subDict["value"]
        return self.__dataDict[key]

    def __iter__(self) -> Iterator[str]:
        """
        Iterate though the contents in order
        """
        yield from self.__orderedList

    def __contains__(self, key: str) -> bool:
        """
        Check if a key is defined
        """
        if not isinstance(key, str) or not key:
            return False
        return bool(self.getRecursive(key))

    def __str__(self) -> str:
        """
        Get a print friendly representation of the CFG

        :return: String with the contents of the CFG
        """
        return self.serialize()

    def __repr__(self) -> str:
        """
        Get a print friendly representation of the CFG

        :return: String with the contents of the CFG
        """
        return self.serialize()

    def __bool__(self) -> Literal[True]:
        """
        CFGs are not zeroes! ;)
        """
        return True

    def __eq__(self, cfg: object) -> bool:
        """
        Check CFGs
        """
        if not isinstance(cfg, CFG):
            return False
        if not self.__orderedList == cfg.__orderedList:
            return False
        for key in self.__orderedList:
            if not self.__commentDict[key].strip() == cfg.__commentDict[key].strip():
                return False
            if not self.__dataDict[key] == cfg.__dataDict[key]:
                return False
        return True

    @gCFGSynchro
    def getComment(self, entryName: str) -> str:
        """
        Get the comment for an option/section

        :type entryName: string
        :param entryName: Name of the option/section
        :return: String with the comment
        """
        try:
            return self.__commentDict[entryName]
        except KeyError:
            raise ValueError(f"{entryName} does not have any comment defined") from None

    @gCFGSynchro
    def setComment(self, entryName: str, comment: str) -> bool:
        """
        Set the comment for an option/section

        :type entryName: string
        :param entryName: Name of the option/section
        :type comment: string
        :param comment: Comment for the option/section
        """
        if entryName in self.__orderedList:
            self.__commentDict[entryName] = comment
            return True
        return False

    @gCFGSynchro
    def serialize(self, tabLevelString: str = "") -> str:
        """
        Generate a human readable serialization of a CFG

        :type tabLevelString: string
        :param tabLevelString: Tab string to apply to entries before representing them
        :return: String with the contents of the CFG
        """
        indentation = "  "
        cfgString = ""
        for entryName in self.__orderedList:
            if entryName in self.__commentDict:
                for commentLine in List.fromChar(self.__commentDict[entryName], "\n"):
                    cfgString += f"{tabLevelString}#{commentLine}\n"
            if entryName in self.listSections():
                cfgString += f"{tabLevelString}{entryName}\n{tabLevelString}{{\n"
                cfgString += cast(CFG, self.__dataDict[entryName]).serialize(f"{tabLevelString}{indentation}")
                cfgString += "%s}\n" % tabLevelString
            elif entryName in self.listOptions():
                valueList = List.fromChar(cast(str, self.__dataDict[entryName]))
                if len(valueList) == 0:
                    cfgString += f"{tabLevelString}{entryName} = \n"
                else:
                    cfgString += f"{tabLevelString}{entryName} = {valueList[0]}\n"
                    for value in valueList[1:]:
                        cfgString += f"{tabLevelString}{entryName} += {value}\n"
            else:
                raise ValueError("Oops. There is an entry in the order which is not a section nor an option")
        return cfgString

    @gCFGSynchro
    def clone(self) -> CFG:
        """
        Create a copy of the CFG

        :return: CFG copy
        """
        clonedCFG = CFG()
        clonedCFG.__orderedList = copy.deepcopy(self.__orderedList)
        clonedCFG.__commentDict = copy.deepcopy(self.__commentDict)
        for option in self.listOptions():
            value = self[option]
            assert value is not False
            clonedCFG.__dataDict[option] = value
        for section in self.listSections():
            clonedCFG.__dataDict[section] = cast(CFG, self[section]).clone()
        return clonedCFG

    @gCFGSynchro
    def mergeWith(self, cfgToMergeWith: CFG) -> CFG:
        """
        Generate a CFG by merging with the contents of another CFG.

        :type cfgToMergeWith: CFG
        :param cfgToMergeWith: CFG with the contents to merge with. This contents are more
                                preemtive than this CFG ones
        :return: CFG with the result of the merge
        """
        mergedCFG = CFG()
        for option in self.listOptions():
            mergedCFG.setOption(option, cast(str, self[option]), self.getComment(option))
        for option in cfgToMergeWith.listOptions():
            mergedCFG.setOption(option, cast(str, cfgToMergeWith[option]), cfgToMergeWith.getComment(option))
        for section in self.listSections():
            sectionCFG = cast(CFG, self[section])
            if section in cfgToMergeWith.listSections():
                oSectionCFG = sectionCFG.mergeWith(cast(CFG, cfgToMergeWith[section]))
                mergedCFG.createNewSection(section, cfgToMergeWith.getComment(section), oSectionCFG)
            else:
                mergedCFG.createNewSection(section, self.getComment(section), sectionCFG.clone())
        for section in cfgToMergeWith.listSections():
            if section not in self.listSections():
                mergedCFG.createNewSection(
                    section, cfgToMergeWith.getComment(section), cast(CFG, cfgToMergeWith[section])
                )
        return mergedCFG

    def getModifications(
        self,
        newerCfg: CFG,
        ignoreMask: list[str] | None = None,
        parentPath: str = "",
        ignoreOrder: bool = False,
        ignoreComments: bool = False,
    ) -> list[ModificationType]:
        """
        Compare two cfgs

        :type newerCfg: ~DIRAC.Core.Utilities.CFG.CFG
        :param newerCfg: Cfg to compare with
        :param list ignoreMask: List of paths to ignore
        :param str parentPath: Start from this path
        :param ignoreOrder: Do not return changes only in ordering
        :param ignoreComments: Do not return changes for changed commens
        :return: A list of modifications
        """
        modList: list[ModificationType] = []
        # Options
        oldOptions = self.listOptions(True)
        newOptions = newerCfg.listOptions(True)
        for newOption in newOptions:
            iPos = newerCfg.__orderedList.index(newOption)
            newOptPath = f"{parentPath}/{newOption}"
            if ignoreMask and newOptPath in ignoreMask:
                continue
            if newOption not in oldOptions:
                modList.append(
                    ("addOpt", newOption, iPos, cast(str, newerCfg[newOption]), newerCfg.getComment(newOption))
                )
            else:
                modified = False
                if iPos != self.__orderedList.index(newOption) and not ignoreOrder:
                    modified = True
                elif newerCfg[newOption] != self[newOption]:
                    modified = True
                elif newerCfg.getComment(newOption) != self.getComment(newOption) and not ignoreComments:
                    modified = True
                if modified:
                    modList.append(
                        ("modOpt", newOption, iPos, cast(str, newerCfg[newOption]), newerCfg.getComment(newOption))
                    )
        for oldOption in oldOptions:
            oldOptPath = f"{parentPath}/{oldOption}"
            if ignoreMask and oldOptPath in ignoreMask:
                continue
            if oldOption not in newOptions:
                modList.append(("delOpt", oldOption, -1, ""))
        # Sections
        oldSections = self.listSections(True)
        newSections = newerCfg.listSections(True)
        for newSection in newSections:
            iPos = newerCfg.__orderedList.index(newSection)
            newSecPath = f"{parentPath}/{newSection}"
            if ignoreMask and newSecPath in ignoreMask:
                continue
            if newSection not in oldSections:
                modList.append(("addSec", newSection, iPos, str(newerCfg[newSection]), newerCfg.getComment(newSection)))
            else:
                modified = False
                if iPos != self.__orderedList.index(newSection):
                    modified = True
                elif newerCfg.getComment(newSection) != self.getComment(newSection):
                    modified = True
                subMod = cast(CFG, self[newSection]).getModifications(
                    cast(CFG, newerCfg[newSection]), ignoreMask, newSecPath, ignoreOrder, ignoreComments
                )
                if subMod:
                    modified = True
                if modified:
                    modList.append(("modSec", newSection, iPos, subMod, newerCfg.getComment(newSection)))
        for oldSection in oldSections:
            oldSecPath = f"{parentPath}/{oldSection}"
            if ignoreMask and oldSecPath in ignoreMask:
                continue
            if oldSection not in newSections:
                modList.append(("delSec", oldSection, -1, ""))
        return modList

    def applyModifications(self, modList: list[ModificationType], parentSection: str = "") -> DReturnType[Literal[""]]:
        """
        Apply modifications to a CFG

        :type modList: List
        :param modList: Modifications from a getModifications call
        :return: True/False
        """
        for modAction in modList:
            key = modAction[1]
            iPos = modAction[2]
            if modAction[0] == "addSec":
                if key in self.listSections():
                    return S_ERROR(f"Section {parentSection}/{key} already exists")
                # key, value, comment, beforeKey = ""
                sec = CFG().loadFromBuffer(modAction[3])
                comment = modAction[4].strip()
                if iPos < len(self.__orderedList):
                    beforeKey = self.__orderedList[iPos]
                else:
                    beforeKey = ""
                self.addKey(key, sec, comment, beforeKey)
            elif modAction[0] == "delSec":
                if key not in self.listSections():
                    return S_ERROR(f"Section {parentSection}/{key} does not exist")
                self.deleteKey(key)
            elif modAction[0] == "modSec":
                if key not in self.listSections():
                    return S_ERROR(f"Section {parentSection}/{key} does not exist")
                section = self[key]
                assert isinstance(section, CFG)
                # if not isinstance(section, CFG):
                #     return S_ERROR(f"Section {parentSection}/{key} does not exist")
                comment = modAction[4].strip()
                self.setComment(key, comment)
                if modAction[3]:
                    result = section.applyModifications(modAction[3], f"{parentSection}/{key}")
                    if not result["OK"]:
                        return result
                if iPos >= len(self.__orderedList) or key != self.__orderedList[iPos]:
                    prevPos = self.__orderedList.index(key)
                    del self.__orderedList[prevPos]
                    self.__orderedList.insert(iPos, key)
            elif modAction[0] == "addOpt":
                if key in self.listOptions():
                    return S_ERROR(f"Option {parentSection}/{key} exists already")
                # key, value, comment, beforeKey = ""
                comment = modAction[4].strip()
                if iPos < len(self.__orderedList):
                    beforeKey = self.__orderedList[iPos]
                else:
                    beforeKey = ""
                self.addKey(key, modAction[3], comment, beforeKey)
            elif modAction[0] == "modOpt":
                if key not in self.listOptions():
                    return S_ERROR(f"Option {parentSection}/{key} does not exist")
                comment = modAction[4].strip()
                self.setOption(key, modAction[3], comment)
                if iPos >= len(self.__orderedList) or key != self.__orderedList[iPos]:
                    prevPos = self.__orderedList.index(key)
                    del self.__orderedList[prevPos]
                    self.__orderedList.insert(iPos, key)
            elif modAction[0] == "delOpt":
                if key not in self.listOptions():
                    return S_ERROR(f"Option {parentSection}/{key} does not exist")
                self.deleteKey(key)

        return S_OK()

    # Functions to load a CFG
    def loadFromFile(self, fileName: str) -> CFG:
        """
        Load the contents of the CFG from a file

        :type fileName: string
        :param fileName: File name to load the contents from
        :return: This CFG
        """
        if zipfile.is_zipfile(fileName):
            with zipfile.ZipFile(fileName) as zipHandler:
                nameList = zipHandler.namelist()
                fileToRead = nameList[0]
                fileData = zipHandler.read(fileToRead).decode("utf-8")
        else:
            with open(fileName) as fd:
                fileData = fd.read()
        return self.loadFromBuffer(fileData)

    @gCFGSynchro
    def loadFromBuffer(self, data: str) -> CFG:
        """
        Load the contents of the CFG from a string

        :type data: string
        :param data: Contents of the CFG
        :return: This CFG

        :raise SyntaxError: in case the number of opening and closing brackets do not match
        """
        commentRE = re.compile(r"^\s*#")
        self.reset()
        levelList = []
        currentLevel = self
        currentlyParsedString = ""
        currentComment = ""
        for line in data.split("\n"):
            line = line.strip()
            if len(line) < 1:
                continue
            if commentRE.match(line):
                currentComment += f"{line.replace('#', '')}\n"
                continue
            for index in range(len(line)):
                if line[index] == "{":
                    currentlyParsedString = currentlyParsedString.strip()
                    currentLevel.createNewSection(currentlyParsedString, currentComment)
                    levelList.append(currentLevel)
                    currentLevel = cast(CFG, currentLevel[currentlyParsedString])
                    currentlyParsedString = ""
                    currentComment = ""
                elif line[index] == "}":
                    try:
                        currentLevel = levelList.pop()
                    except IndexError:
                        raise ValueError(
                            "The cfg file seems to close more sections than it opens (i.e. to many '}' vs '{'"
                        ) from None
                elif line[index] == "=":
                    lFields = line.split("=")
                    currentLevel.setOption(lFields[0].strip(), "=".join(lFields[1:]).strip(), currentComment)
                    currentlyParsedString = ""
                    currentComment = ""
                    break
                elif line[index : index + 2] == "+=":
                    valueList = line.split("+=")
                    currentLevel.appendToOption(valueList[0].strip(), f", {'+='.join(valueList[1:]).strip()}")
                    currentlyParsedString = ""
                    currentComment = ""
                    break
                else:
                    currentlyParsedString += line[index]
        # At this point, the levelList should be empty
        if levelList:
            raise ValueError("The cfg file seems to open more sections than it closes (i.e. to many '{' vs '}'")
        return self

    @gCFGSynchro
    def loadFromDict(self, data: CFGAsDict) -> CFG:
        for k in data:
            value = data[k]
            if isinstance(value, dict):
                self.createNewSection(k, "", CFG().loadFromDict(value))
            elif isinstance(value, (list, tuple)):
                self.setOption(k, ", ".join(value), "")
            else:
                self.setOption(k, str(value), "")
        return self

    def writeToFile(self, fileName: StrOrBytesPath) -> bool:
        """
        Write the contents of the cfg to file

        :type fileName: string
        :param fileName: Name of the file to write the cfg to
        :return: True/False
        """
        try:
            directory = os.path.dirname(fileName)
            if directory and (not os.path.exists(directory)):
                os.makedirs(directory)
            with open(fileName, "w") as fd:
                fd.write(str(self))
            return True
        except Exception:
            return False
