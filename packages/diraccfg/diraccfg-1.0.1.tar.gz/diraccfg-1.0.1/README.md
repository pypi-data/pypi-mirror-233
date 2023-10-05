# Parser for DIRAC cfg files

[![CI](https://github.com/DIRACGrid/diraccfg/workflows/CI/badge.svg?branch=master)](https://github.com/DIRACGrid/diraccfg/actions?query=branch%3Amaster)
[![PyPI](https://badge.fury.io/py/diraccfg.svg)](https://pypi.org/project/diraccfg/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/diraccfg)](https://github.com/conda-forge/diraccfg-feedstock/)

`diraccfg` provides a parser for the configuration files used by
[DIRAC](https://github.com/DIRACGrid) and its associated projects.


## Installation

```bash
pip install diraccfg
```

## Command line usage

The command line mode of `diraccfg` primarily serves to convert the
configuration into a JSON file which can then be processed using standard tools
such as [`jq`](https://stedolan.github.io/jq/).

The following examples are ran using the following configuration file:

```
DefaultModules = DIRAC
Sources
{
  DIRAC = git://github.com/DIRACGrid/DIRAC.git
}
Releases
{
  integration
  {
    Modules = DIRAC, WebAppDIRAC, VMDIRAC
    Externals = v6r6p8
    DIRACOS = master
  }
  v7r0-pre19
  {
    Modules = DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r5, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1
    DIRACOS = master
  }
  v6r22p2
  {
    Modules = DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r6, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1
    Externals = v6r6p8
    DIRACOS = v1r3
  }
  v6r22p1
  {
    Modules = DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r6, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1
    Externals = v6r6p8
    DIRACOS = v1r3
  }
}
```

### Print as JSON

```
$ diraccfg as-json example.cfg
{"DefaultModules": "DIRAC", "Sources": {"DIRAC": "git://github.com/DIRACGrid/DIRAC.git"}, "Releases": {"integration": {"Modules": "DIRAC, WebAppDIRAC, VMDIRAC", "Externals": "v6r6p8", "DIRACOS": "master"}, "v7r0-pre19": {"Modules": "DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r5, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1", "DIRACOS": "master"}, "v6r22p2": {"Modules": "DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r6, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1", "Externals": "v6r6p8", "DIRACOS": "v1r3"}, "v6r22p1": {"Modules": "DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r6, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1", "Externals": "v6r6p8", "DIRACOS": "v1r3"}}}
```

### Extract available releases with using `jq`

```bash
$ diraccfg as-json example.cfg | jq '.Releases'
{
  "integration": {
    "Modules": "DIRAC, WebAppDIRAC, VMDIRAC",
    "Externals": "v6r6p8",
    "DIRACOS": "master"
  },
  "v7r0-pre19": {
    "Modules": "DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r5, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1",
    "DIRACOS": "master"
  },
  "v6r22p2": {
    "Modules": "DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r6, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1",
    "Externals": "v6r6p8",
    "DIRACOS": "v1r3"
  },
  "v6r22p1": {
    "Modules": "DIRAC, VMDIRAC:v2r4-pre2, RESTDIRAC:v0r6, COMDIRAC:v0r17, WebAppDIRAC:v4r0p7, OAuthDIRAC:v0r1-pre1",
    "Externals": "v6r6p8",
    "DIRACOS": "v1r3"
  }
}
```

### Get a sorted list of stable version numbers

```bash
$ diraccfg as-json example.cfg | jq '.Releases' | diraccfg sort-versions
["v6r22p2", "v6r22p1"]
```

### Get a sorted list of version numbers including prereleases

```bash
$ diraccfg as-json example.cfg | jq '.Releases' | diraccfg sort-versions --allow-pre-releases
["v7r0-pre19", "v6r22p2", "v6r22p1"]
```

### Find the latest releases

```bash
$ diraccfg as-json example.cfg | jq '.Releases' | diraccfg sort-versions | jq -r '.[0]'
v6r22p2
```

```bash
$ diraccfg as-json example.cfg | jq '.Releases' | diraccfg sort-versions --allow-pre-releases | jq -r '.[0]'
v7r0-pre19
```
