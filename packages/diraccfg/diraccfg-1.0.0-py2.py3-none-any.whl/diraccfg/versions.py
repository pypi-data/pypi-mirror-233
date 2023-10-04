from __future__ import annotations

import re


def parseVersion(versionString: str) -> tuple[int, int, int, int | None]:
    """Parse a DIRAC-style version sting

    :param versionString: Version identifier to parse
    :returns: `tuple` of 4 values (major, minor, patch, pre). All values will be
              `int` except "pre" which is `None` for released versions.
    :raises: ValueError if the versionString is invalid
    """
    match = re.match(
        r"^v(?P<major>\d+)r(?P<minor>\d+)(?:p(?P<patch>\d+))?(?:-pre(?P<pre>\d+))?$",
        versionString,
    )
    if not match:
        raise ValueError(f"{versionString} is not a valid version")

    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch") or 0),
        None if match.group("pre") is None else int(match.group("pre")),
    )
