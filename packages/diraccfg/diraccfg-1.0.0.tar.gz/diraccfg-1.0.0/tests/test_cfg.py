import os
import pytest
import zipfile
from copy import deepcopy

from diraccfg.cfg import CFG, S_OK, List

EXAMPLE_CFG_FILE = os.path.join(os.path.dirname(__file__), "releases.cfg")
EXAMPLE_CFG_FILE2 = os.path.join(os.path.dirname(__file__), "releases2.cfg")
BROKEN_OPEN_CFG_FILE = os.path.join(os.path.dirname(__file__), "broken_open.cfg")
BROKEN_CLOSE_CFG_FILE = os.path.join(os.path.dirname(__file__), "broken_close.cfg")

EXPECTED_MODIFICATIONS = [
    (
        "modSec",
        "Sources",
        1,
        [
            ("modOpt", "RESTDIRAC", 1, "git://github.com/DIRACGrid/RESTDIRAC.git", ""),
            ("modOpt", "COMDIRAC", 2, "git://github.com/DIRACGrid/COMDIRAC.git", ""),
            ("modOpt", "MPIDIRAC", 3, "git://github.com/DIRACGrid/MPIDIRAC.git", ""),
            ("modOpt", "Web", 4, "git://github.com/DIRACGrid/DIRACWeb.git", ""),
            ("modOpt", "WebAppDIRAC", 5, "git://github.com/DIRACGrid/WebAppDIRAC.git", ""),
            ("modOpt", "FSDIRAC", 6, "git://github.com/DIRACGrid/FSDIRAC.git", ""),
            ("modOpt", "BoincDIRAC", 7, "git://github.com/DIRACGrid/BoincDIRAC.git", ""),
            ("modOpt", "OAuthDIRAC", 8, "git://github.com/DIRACGrid/OAuthDIRAC.git", ""),
            ("addOpt", "SomethingElse", 9, "AValue", ""),
            ("delOpt", "VMDIRAC", -1, ""),
        ],
        "",
    ),
    (
        "modSec",
        "Releases",
        2,
        [
            (
                "modSec",
                "v7r0-pre19",
                1,
                [
                    (
                        "modOpt",
                        "Modules",
                        0,
                        "DIRAC, VMDIRAC:v2r4-pre2, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1",
                        "",
                    )
                ],
                "",
            ),
            ("modSec", "v6r21p12", 6, [("modOpt", "DIRACOS", 1, "v1r1", ""), ("delOpt", "Externals", -1, "")], ""),
            ("modSec", "v6r11p1", 282, [], ""),
            ("modSec", "v6r11", 283, [], ""),
            ("modSec", "v6r10p25", 284, [], ""),
            ("modSec", "v6r10p23", 285, [], ""),
            ("modSec", "v6r10p9", 286, [], ""),
            ("modSec", "v6r9p33", 287, [], ""),
            (
                "addSec",
                "v6r9p33-pre9",
                288,
                "Modules = DIRAC\n"
                "Modules += VMDIRAC:v0r8\n"
                "Modules += RESTDIRAC:v0r2\n"
                "Modules += COMDIRAC:v0r4p1\n"
                "Modules += Web:v1r2p2\n"
                "Externals = v6r1\n",
                "",
            ),
            ("delSec", "v6r11p2", -1, ""),
        ],
        " Here is where the releases go:\n",
    ),
]
BAD_MODIFICATIONS = [
    ("addOpt", "DefaultModules", 9, "AValue", ""),
    # FIXME: This one raises a KeyError
    # ("addOpt", "Releases", 9, "AValue", ""),
    ("modOpt", "missing", 8, "git://github.com/DIRACGrid/OAuthDIRAC.git", ""),
    ("delOpt", "missing", -1, ""),
    ("addSec", "Releases", 288, "Modules = DIRAC\n", ""),
    ("modSec", "missing", 287, [], ""),
    ("delSec", "missing", -1, ""),
]


def test_load():
    rels = CFG().loadFromFile(EXAMPLE_CFG_FILE)
    assert rels["Releases"]["v6r22"]["DIRACOS"] == "v1r2"  # pylint: disable=unsubscriptable-object


def test_comment():
    c = CFG().loadFromFile(EXAMPLE_CFG_FILE)
    assert c.getComment("Releases").strip() == "Here is where the releases go:"


def test_sanity():
    with pytest.raises(ValueError) as excinfo:
        CFG().loadFromFile(BROKEN_OPEN_CFG_FILE)
    assert "close more section" in str(excinfo)

    with pytest.raises(ValueError) as excinfo:
        CFG().loadFromFile(BROKEN_CLOSE_CFG_FILE)
    assert "open more section" in str(excinfo)


def test_recurse():
    c = CFG().loadFromFile(EXAMPLE_CFG_FILE)
    assert c.getRecursive("/Releases/v6r22/DIRACOS")["value"] == "v1r2"
    assert c.getRecursive("/Releases/v6r99") is None
    assert isinstance(c.getRecursive("/Releases/v6r22")["value"], CFG)
    assert c.getRecursive("/Releases/v6r22/DIRACOS/invalid") is None


def test_recurse2():
    a = CFG().loadFromDict({"a": {"b": {"c": "d"}}})

    assert a.getRecursive("/a/b/c", levelsAbove=0)["value"] == "d"

    expected = CFG().loadFromDict({"c": "d"})
    assert a.getRecursive("/a/b/c", levelsAbove=1)["value"] == expected
    assert a.getRecursive("/a/b/c", levelsAbove=-1)["value"] == expected

    expected = CFG().loadFromDict({"b": {"c": "d"}})
    assert a.getRecursive("/a/b", levelsAbove=1)["value"] == expected
    assert a.getRecursive("/a/b", levelsAbove=-1)["value"] == expected
    assert a.getRecursive("/a/b/c", levelsAbove=2)["value"] == expected
    assert a.getRecursive("/a/b/c", levelsAbove=-2)["value"] == expected

    assert a.getRecursive("/a/b", levelsAbove=2)["value"] == a
    assert a.getRecursive("/a/b", levelsAbove=-2)["value"] == a
    assert a.getRecursive("/a/b/c", levelsAbove=3)["value"] == a
    assert a.getRecursive("/a/b/c", levelsAbove=-3)["value"] == a

    assert a.getRecursive("/a/b/c", levelsAbove=4) is None
    assert a.getRecursive("/a/b/c", levelsAbove=-4) is None


def test_append():
    c = CFG().loadFromFile(EXAMPLE_CFG_FILE)
    assert c.getOption("/Releases/v6r22/DIRACOS") == "v1r2"
    c.appendToOption("/Releases/v6r22/DIRACOS", ",v1r3")
    assert c.getOption("/Releases/v6r22/DIRACOS") == "v1r2,v1r3"

    with pytest.raises(ValueError, match=r"is not a string"):
        c.appendToOption("/Releases/v6r22", "invalid")

    with pytest.raises(KeyError, match=r"does not exist"):
        c.appendToOption("/Releases/v6r23/DIRACOS2", "invalid")

    with pytest.raises(KeyError, match=r"has not been declared"):
        c.appendToOption("/Releases/v6r22/DIRACOS2", "invalid")


def test_getModifications():
    a = CFG()
    a.loadFromFile(EXAMPLE_CFG_FILE)
    b = CFG()
    b.loadFromFile(EXAMPLE_CFG_FILE2)
    modifications = a.getModifications(b)
    assert modifications == EXPECTED_MODIFICATIONS
    assert a != b


def test_getModifications2():
    a = CFG().loadFromDict({"a": {"b": "c"}})
    b = CFG().loadFromDict({"a": {"b": "c"}, "d": {"e": "f"}})
    modifications = a.getModifications(b, ignoreMask=["/d"])
    assert modifications == []


def test_getModifications3():
    a = CFG().loadFromDict({"a": {"b": "c"}, "d": {"e": "f"}})
    b = CFG().loadFromDict({"a": {"b": "c"}})
    modifications = a.getModifications(b, ignoreMask=["/d"])
    assert modifications == []


def test_getModifications4():
    a = CFG().loadFromDict({"a": {"b": "c"}})
    b = CFG().loadFromDict({"a": {"b": "c"}, "d": "123"})
    modifications = a.getModifications(b, ignoreMask=["/d"])
    assert modifications == []


def test_getModifications5():
    a = CFG().loadFromDict({"a": {"b": "c"}, "d": "123"})
    b = CFG().loadFromDict({"a": {"b": "c"}})
    modifications = a.getModifications(b, ignoreMask=["/d"])
    assert modifications == []


@pytest.mark.xfail
def test_getModifications6():
    a = CFG().loadFromDict({"a": {"b": "c"}})
    b = CFG().loadFromDict({"a": {"b": "c"}})
    b.setComment("a", "new comment")
    modifications = a.getModifications(b)
    assert modifications == [("modSec", "a", 0, [], "new comment")]
    modifications = a.getModifications(b, ignoreComments=True)
    assert modifications == []


def test_getModifications7():
    a = CFG().loadFromDict({"a": 5})
    b = CFG().loadFromDict({"a": 5})
    b.setComment("a", "new comment")
    modifications = a.getModifications(b)
    assert modifications == [("modOpt", "a", 0, "5", "new comment")]
    modifications = a.getModifications(b, ignoreComments=True)
    assert modifications == []


def test_applyModifications():
    a = CFG()
    a.loadFromFile(EXAMPLE_CFG_FILE)
    b = CFG()
    b.loadFromFile(EXAMPLE_CFG_FILE2)

    c = CFG()
    c.loadFromFile(EXAMPLE_CFG_FILE)
    assert a == c
    assert b != c
    assert c.applyModifications(EXPECTED_MODIFICATIONS) == S_OK()
    assert a != c
    assert b == c

    d = CFG()
    assert d.applyModifications([("addOpt", "DefaultModules", 9, "AValue", "")]) == S_OK()
    assert d == CFG().loadFromDict({"DefaultModules": "AValue"})

    d = CFG()
    assert d.applyModifications([("addSec", "my-section", 9, "Modules = DIRAC\n", "")]) == S_OK()
    assert d == CFG().loadFromDict({"my-section": {"Modules": "DIRAC"}})


@pytest.mark.parametrize("modification", EXPECTED_MODIFICATIONS + BAD_MODIFICATIONS)
def test_applyModifications_invalid(modification):
    a = CFG()
    a.loadFromFile(EXAMPLE_CFG_FILE2)
    res = a.applyModifications([modification])
    assert not res["OK"]


def test_getOption():
    a = CFG().loadFromDict(
        {
            "a": "1",
            "b": "2",
            "c": {"d": "3", "e": "4"},
            "x": "12,34",
            "y": " 12 , 34 ",
            "bools": {
                "true": "true",
                "True": "True",
                "TRUE": "TRUE",
                "false": "false",
                "False": "False",
                "FALSE": "FALSE",
                "yes": "yes",
                "no": "no",
                "1": "1",
                "0": "0",
                "other": "other",
            },
        }
    )

    assert a.getOption("a") == "1"
    assert a.getOption("a", 0) == 1
    assert a.getOption("a", "") == "1"
    assert a.getOption("a", []) == ["1"]

    assert a.getOption("b") == "2"

    assert a.getOption("x") == "12,34"
    assert a.getOption("x", []) == ["12", "34"]

    assert a.getOption("y") == " 12 , 34 "
    assert a.getOption("y", []) == ["12", "34"]

    assert a.getOption("/bools/true", True) is True
    assert a.getOption("/bools/True", True) is True
    assert a.getOption("/bools/TRUE", True) is True
    assert a.getOption("/bools/false", True) is False
    assert a.getOption("/bools/False", True) is False
    assert a.getOption("/bools/FALSE", True) is False
    assert a.getOption("/bools/yes", True) is True
    assert a.getOption("/bools/no", True) is False
    assert a.getOption("/bools/1", True) is True
    assert a.getOption("/bools/0", True) is False
    assert a.getOption("/bools/other", True) is False
    assert a.getOption("/bools/missing", True) is True

    assert a.getOption("/bools/true", False) is True
    assert a.getOption("/bools/True", False) is True
    assert a.getOption("/bools/TRUE", False) is True
    assert a.getOption("/bools/false", False) is False
    assert a.getOption("/bools/False", False) is False
    assert a.getOption("/bools/FALSE", False) is False
    assert a.getOption("/bools/yes", False) is True
    assert a.getOption("/bools/no", False) is False
    assert a.getOption("/bools/1", False) is True
    assert a.getOption("/bools/0", False) is False
    assert a.getOption("/bools/other", False) is False
    assert a.getOption("/bools/missing", False) is False

    assert a.getOption("missing") is None
    assert a.getOption("missing", None) is None
    assert a.getOption("missing", 1) == 1
    assert a.getOption("missing", True) is True
    assert a.getOption("missing", False) is False
    assert a.getOption("missing", "1") == "1"
    assert a.getOption("missing", ["1"]) == ["1"]

    assert a.getOption("c") is None
    assert a.getOption("c", None) is None
    assert a.getOption("c", 1) == 1
    assert a.getOption("c", True) is True
    assert a.getOption("c", False) is False
    assert a.getOption("c", "1") == "1"
    assert a.getOption("c", ["1"]) == ["1"]

    class CustomType:
        def __init__(self, value: str) -> None:
            if value not in ["yes", "default"]:
                raise ValueError("Invalid value")
            self.value = value

    obj = CustomType("default")
    assert a.getOption("/bools/yes", obj).value == "yes"
    assert a.getOption("/bools/no", obj) is obj


def test_comments():
    a = CFG().loadFromDict({"a": "1", "b": "", "c": {"d": "3", "e": "4"}})

    assert a.getComment("a") == ""
    assert a.setComment("a", "some comment") is True
    assert a.getComment("a") == "some comment"

    assert "missing" not in a
    assert a.setComment("missing", "some comment") is False
    assert "missing" not in a

    assert a.serialize() == "#some comment\na = 1\nb = \nc\n{\n  d = 3\n  e = 4\n}\n"


@pytest.mark.xfail
def test_comments_nested():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.getComment("/c/d") == ""
    assert a.setComment("/c/d", "some other comment") is True
    assert a.getComment("/c/d") == "some other comment"


def test_getitem():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a["a"] == "1"
    assert a["/a"] == "1"
    assert a["c/d"] == "3"
    assert a["/c/d"] == "3"
    assert a["c"] == CFG().loadFromDict({"d": "3", "e": "4"})


@pytest.mark.xfail
def test_getitem_missing():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    with pytest.raises(KeyError):
        assert a["d/e"] is False


def test_getitem_missing2():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    with pytest.raises(KeyError, match=r"e"):
        a["e"]


def test_setOption():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.getOption("a") == "1"
    a.setOption("a", "19")
    assert a.getOption("a") == "19"

    assert a.getOption("x") is None
    a.setOption("x", 42)
    assert a.getOption("x") == "42"

    assert a.getOption("/c/x") is None
    a.setOption("/c/x", "hello world")
    assert a.getOption("/c/x") == "hello world"

    assert a.getOption("/missing/z") is None
    assert a.setOption("/missing/z", "invalid")["OK"] is False
    assert a.getOption("/missing/z") is None

    with pytest.raises(KeyError, match=r"doesn't seem to be a section"):
        a.setOption("/a/b", 42)
    assert "/a/b" not in a

    with pytest.raises(ValueError, match=r"Creating an option with empty name"):
        a.setOption("", 42)
    assert "" not in a


def test_addKey():
    a = CFG()

    assert "a" not in a
    a.addKey("a", "1", "a comment")
    assert a["a"] == "1"
    assert a.getComment("a") == "a comment"
    with pytest.raises(KeyError, match=r"already exists"):
        a.addKey("a", "1", "b comment")
    assert a["a"] == "1"
    assert a.getComment("a") == "a comment"

    with pytest.raises(KeyError, match=r"does not exist"):
        a.addKey("x/y", "1", "b comment")

    a.addKey("b", "2", "b comment")
    a.addKey("abis", "abis", "abis comment", beforeKey="b")
    assert a == CFG().loadFromBuffer("#a comment\na = 1\n#abis comment\nabis = abis\n#b comment\nb = 2")


def test_renameKey():
    a = CFG()
    a.loadFromFile(EXAMPLE_CFG_FILE)
    assert a.getOption("DefaultModules", "UNSET") == "DIRAC"
    assert a.getOption("DefaultModulesRenamed", "UNSET") == "UNSET"
    assert a.renameKey("DefaultModules", "DefaultModulesRenamed")
    assert a.getOption("DefaultModules", "UNSET") == "UNSET"
    assert a.getOption("DefaultModulesRenamed", "UNSET") == "DIRAC"

    assert a.renameKey("DefaultModulesRenamed", "DefaultModulesRenamed")
    assert a.getOption("DefaultModules", "UNSET") == "UNSET"
    assert a.getOption("DefaultModulesRenamed", "UNSET") == "DIRAC"

    assert "Missing" not in a
    with pytest.raises(KeyError, match=r"does not exist"):
        assert a.renameKey("/Missing/integration", "/Missing/integration2")
    assert "Missing" not in a

    with pytest.raises(KeyError, match=r"does not exist"):
        assert a.renameKey("/Releases/integration", "/Missing/integration2")
    assert "Missing" not in a

    assert a.getAsDict("/Releases/integration") == {
        "DIRACOS": "master",
        "Externals": "v6r6p8",
        "Modules": "DIRAC, WebAppDIRAC, VMDIRAC",
    }
    assert "/Releases/integration" in a
    assert "/Releases/integration_renamed" not in a
    assert a.renameKey("/Releases/integration", "/Releases/integration_renamed")
    assert "/Releases/integration" not in a
    assert "/Releases/integration_renamed" in a
    assert a.getAsDict("/Releases/integration_renamed") == {
        "DIRACOS": "master",
        "Externals": "v6r6p8",
        "Modules": "DIRAC, WebAppDIRAC, VMDIRAC",
    }


def test_existsKey():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.existsKey("a") is True
    assert a.existsKey("c") is True
    assert a.existsKey("/c") is False
    assert a.existsKey("c/d") is False
    assert a["c"].existsKey("d") is True  # pylint: disable=no-member


def test_mergeWith():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}, "g": {}})
    b = CFG().loadFromDict({"aa": 1, "bb": 2, "c": {"dd": 3, "e": 5}, "f": {}})
    merged = a.mergeWith(b)
    assert merged == CFG().loadFromDict(
        {
            "a": 1,
            "b": 2,
            "aa": 1,
            "bb": 2,
            "c": {
                "d": 3,
                "e": 5,
                "dd": 3,
            },
            "g": {},
            "f": {},
        }
    )


def test_deleteKey():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})

    assert a.deleteKey("a")
    assert not a.deleteKey("a")
    assert a == CFG().loadFromDict({"b": "2", "c": {"d": "3", "e": "4"}})

    assert a.deleteKey("c/e")
    assert not a.deleteKey("c/e")
    assert a == CFG().loadFromDict({"b": "2", "c": {"d": "3"}})

    assert a.deleteKey("/c")
    assert not a.deleteKey("/c")
    assert a == CFG().loadFromDict({"b": "2"})

    with pytest.raises(KeyError, match=r"does not exist"):
        a.deleteKey("x/y")


def test_sortByKey():
    initial = {"z": "1", "a": "2", "m": {"d": "3", "e": "4"}}
    a = CFG().loadFromDict(deepcopy(initial))
    assert a.sortByKey()
    assert not a.sortByKey()

    a = CFG().loadFromDict(deepcopy(initial))
    a.sortByKey()
    assert a != CFG().loadFromDict(deepcopy(initial))
    assert a == CFG().loadFromDict({"a": "2", "m": {"d": "3", "e": "4"}, "z": "1"})

    a = CFG().loadFromDict(deepcopy(initial))
    a.sortByKey(reverse=False)
    assert a != CFG().loadFromDict(deepcopy(initial))
    assert a == CFG().loadFromDict({"a": "2", "m": {"d": "3", "e": "4"}, "z": "1"})

    a = CFG().loadFromDict(deepcopy(initial))
    a.sortByKey(reverse=True)
    assert a != CFG().loadFromDict(deepcopy(initial))
    assert a == CFG().loadFromDict({"z": "1", "m": {"d": "3", "e": "4"}, "a": "2"})
    # Make sure it isn't applied recursively
    assert a != CFG().loadFromDict({"z": "1", "m": {"e": "4", "d": "3"}, "a": "2"})


def test_sortAlphabetically():
    # TODO: sortAlphabetically is the same as sortByKey except reverse/ascending have inverted meanings of True/False
    initial = {"z": "1", "a": "2", "m": {"d": "3", "e": "4"}}
    a = CFG().loadFromDict(deepcopy(initial))
    assert a.sortAlphabetically()
    assert not a.sortAlphabetically()

    a = CFG().loadFromDict(deepcopy(initial))
    a.sortAlphabetically()
    assert a != CFG().loadFromDict(deepcopy(initial))
    assert a == CFG().loadFromDict({"a": "2", "m": {"d": "3", "e": "4"}, "z": "1"})

    a = CFG().loadFromDict(deepcopy(initial))
    a.sortAlphabetically(ascending=True)
    assert a != CFG().loadFromDict(deepcopy(initial))
    assert a == CFG().loadFromDict({"a": "2", "m": {"d": "3", "e": "4"}, "z": "1"})

    a = CFG().loadFromDict(deepcopy(initial))
    a.sortAlphabetically(ascending=False)
    assert a != CFG().loadFromDict(deepcopy(initial))
    assert a == CFG().loadFromDict({"z": "1", "m": {"d": "3", "e": "4"}, "a": "2"})
    # Make sure it isn't applied recursively
    assert a != CFG().loadFromDict({"z": "1", "m": {"e": "4", "d": "3"}, "a": "2"})


def test_copyKey():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.copyKey("c", "c")
    assert a == CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})

    assert a.copyKey("c", "cc")
    assert a != CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.getAsDict() == {
        "a": "1",
        "b": "2",
        "c": {
            "d": "3",
            "e": "4",
        },
        "cc": {
            "d": "3",
            "e": "4",
        },
    }


def test_copyKey_deeper():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.copyKey("c/d", "m")
    assert a != CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a == CFG().loadFromDict(
        {
            "a": "1",
            "m": "3",
            "b": "2",
            "c": {
                "d": "3",
                "e": "4",
            },
        }
    )

    assert a.copyKey("b", "/c/x")
    assert a != CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a == CFG().loadFromDict(
        {
            "a": "1",
            "m": "3",
            "b": "2",
            "c": {
                "d": "3",
                "e": "4",
                "x": "2",
            },
        }
    )

    with pytest.raises(KeyError, match=r"does not exist"):
        a.copyKey("x/y", "c/y")

    with pytest.raises(KeyError, match=r"does not exist"):
        a.copyKey("c/d", "x/y")


@pytest.mark.xfail
def test_copyKey_mutability():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    a.renameKey("/c/d", "/c/dd")
    assert a.getAsDict() == {
        "a": "1",
        "b": "2",
        "c": {
            "dd": "3",
            "e": "4",
        },
        "cc": {
            "d": "3",
            "e": "4",
        },
    }


def test_isSection():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.isSection("a") is False
    assert a.isSection("c") is True
    assert a.isSection("/a") is False
    assert a.isSection("/c") is True
    assert a.isSection("/a/") is False
    assert a.isSection("/c/") is True
    assert a.isSection("/c/d") is False
    assert a.isSection("c/d") is False
    assert a.isSection("c/d/e") is False
    assert a.isSection("/c/d/e") is False
    assert a.isSection("c/d/e/f") is False
    assert a.isSection("/c/d/e/f") is False


def test_isOption():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.isOption("a") is True
    assert a.isOption("c") is False
    assert a.isOption("/a") is True
    assert a.isOption("/c") is False
    assert a.isOption("/a/") is True
    assert a.isOption("/c/") is False
    assert a.isOption("/c/d") is True
    assert a.isOption("c/d") is True
    assert a.isOption("c/d/e") is False
    assert a.isOption("/c/d/e") is False
    assert a.isOption("c/d/e/f") is False
    assert a.isOption("/c/d/e/f") is False


def test_listOptions():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.listOptions() == ["a", "b"]
    assert a.listOptions(ordered=True) == ["a", "b"]
    assert a.listOptions(ordered=False) == ["a", "b"]


def test_listSections():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.listSections() == ["c"]
    assert a.listSections(ordered=True) == ["c"]
    assert a.listSections(ordered=False) == ["c"]


def test_listAll():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.listAll() == ["a", "b", "c"]


def test_createNewSection():
    initial = {"a": "1", "b": "2", "c": {"d": "3", "e": "4"}}
    a = CFG().loadFromDict(initial)
    a.createNewSection("new1")
    assert a.getAsDict() == initial | {"new1": {}}
    a.createNewSection("new2", contents=CFG().loadFromDict({"12": "24"}))
    assert a.getAsDict() == initial | {"new1": {}, "new2": {"12": "24"}}
    a.createNewSection("new1/d", contents=CFG())
    assert a.getAsDict() == initial | {"new1": {"d": {}}, "new2": {"12": "24"}}

    with pytest.raises(ValueError, match="Creating a section with empty name"):
        a.createNewSection("")

    with pytest.raises(KeyError, match="key already exists"):
        a.createNewSection("/new2")

    with pytest.raises(KeyError, match="Entry a doesn't seem to"):
        a.createNewSection("/a/new9")

    assert a.createNewSection("/new2/new9/new10")["OK"] is False
    assert a.createNewSection("new3/new4")["OK"] is False
    assert a.createNewSection("/new3/new4")["OK"] is False


def test_writeToFile(tmp_path):
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    f = tmp_path / "test.cfg"
    assert a.writeToFile(f) is True
    assert f.read_text() == "a = 1\nb = 2\nc\n{\n  d = 3\n  e = 4\n}\n"

    f = tmp_path / "a" / "b" / "c" / "test.cfg"
    assert a.writeToFile(f) is True
    assert f.read_text() == "a = 1\nb = 2\nc\n{\n  d = 3\n  e = 4\n}\n"

    f = "/dev/null/test.cfg"
    assert a.writeToFile(f) is False


def test_getAsCFG():
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    assert a.getAsCFG("/c") == CFG().loadFromDict({"d": "3", "e": "4"})
    assert a.getAsCFG("/d/x") == CFG()
    assert a.getAsCFG("x/y/z") == CFG()


def test_fromChar():
    assert List.fromChar("") == []
    assert List.fromChar("a,b") == ["a", "b"]
    assert List.fromChar("a, b") == ["a", "b"]
    assert List.fromChar(" a, b ") == ["a", "b"]
    assert List.fromChar(" a,\n b ") == ["a", "b"]
    assert List.fromChar(" a,\n b ", sepChar=";") == ["a,\n b"]
    assert List.fromChar(None, sepChar=";") is None


def test_loadFromDict(tmp_path):
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": ["1", "4"]}})
    assert a.serialize() == "a = 1\nb = 2\nc\n{\n  d = 3\n  e = 1\n  e += 4\n}\n"


def test_load_zip(tmp_path):
    a = CFG().loadFromDict({"a": "1", "b": "2", "c": {"d": "3", "e": "4"}})
    as_text = a.serialize()
    with zipfile.ZipFile(tmp_path / "test.zip", "w") as z:
        z.writestr("test.cfg", as_text)
    b = CFG().loadFromFile(tmp_path / "test.zip")
    assert a == b
    assert b.getAsDict() == {"a": "1", "b": "2", "c": {"d": "3", "e": "4"}}


def test_getAsDict():
    initial = {"a": "1", "b": "2", "c": {"d": "3", "e": "4"}}
    a = CFG().loadFromDict(initial)
    assert a.getAsDict() == initial
    assert a.getAsDict("c") == initial["c"]
    assert a.getAsDict("b") == {}
    assert a.getAsDict("/missing/xxx") == {}


def test_bool():
    a = CFG()
    assert bool(a) is True


def test_eq():
    a = CFG()
    b = CFG()
    assert a == b

    a.setOption("a", "1")
    assert a != b

    b.setOption("a", "1")
    assert a == b

    a.setComment("a", "Some comment")
    assert a != b


def test_iter():
    initial = {"a": "1", "b": "2", "c": {"d": "3", "e": "4"}}
    a = CFG().loadFromDict(deepcopy(initial))
    assert list(a) == ["a", "b", "c"]


def test_clone():
    initial = {"a": "1", "b": "2", "c": {"d": "3", "e": "4"}}
    a = CFG().loadFromDict(deepcopy(initial))
    b = a.clone()
    assert a == b

    b.setOption("a", "2")
    assert a.getOption("a") == "1"
    assert b.getOption("a") == "2"

    b.setOption("c/d", "2")
    assert a.getOption("c/d") == "3"
    assert b.getOption("c/d") == "2"
