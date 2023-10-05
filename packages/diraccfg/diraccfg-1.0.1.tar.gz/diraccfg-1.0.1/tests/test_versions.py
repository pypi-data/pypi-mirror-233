import pytest

import diraccfg


@pytest.mark.parametrize(
    "string,expected",
    [
        ("v7r0p30", (7, 0, 30, None)),
        ("v7r1", (7, 1, 0, None)),
        ("v7r1-pre1", (7, 1, 0, 1)),
        ("v7r1-pre9", (7, 1, 0, 9)),
        ("v7r1p10", (7, 1, 10, None)),
        ("v7r1p9", (7, 1, 9, None)),
        ("v7r2-pre10", (7, 2, 0, 10)),
        ("v7r2-pre9", (7, 2, 0, 9)),
        ("v7r2p8-pre9", (7, 2, 8, 9)),
        ("v10r0p30", (10, 0, 30, None)),
        ("v10r1", (10, 1, 0, None)),
        ("v10r1-pre1", (10, 1, 0, 1)),
        ("v10r1-pre9", (10, 1, 0, 9)),
        ("v10r1p10", (10, 1, 10, None)),
        ("v10r1p9", (10, 1, 9, None)),
        ("v10r2-pre10", (10, 2, 0, 10)),
        ("v10r2-pre9", (10, 2, 0, 9)),
        ("v10r2p8-pre9", (10, 2, 8, 9)),
        ("v100r0p30", (100, 0, 30, None)),
        ("v100r1", (100, 1, 0, None)),
        ("v100r1-pre1", (100, 1, 0, 1)),
        ("v100r1-pre9", (100, 1, 0, 9)),
        ("v100r1p10", (100, 1, 10, None)),
        ("v100r1p9", (100, 1, 9, None)),
        ("v100r2-pre10", (100, 2, 0, 10)),
        ("v100r2-pre9", (100, 2, 0, 9)),
        ("v100r2p8-pre9", (100, 2, 8, 9)),
    ],
)
def test_parseValid(string, expected):
    assert expected == diraccfg.parseVersion(string)


@pytest.mark.parametrize(
    "string",
    [
        "v7r0p30-pre30-pre30",
        "master",
        "dev",
        "integration",
        "7r0p30",
        "v7r2p30p2",
        "1.0.0",
        "v7p30",
        "v7p30-pre2",
        "v10p30",
        "v10p30-pre2",
        "v100p30",
        "v100p30-pre2",
    ],
)
def test_parseInvalid(string):
    with pytest.raises(ValueError):
        diraccfg.parseVersion(string)
