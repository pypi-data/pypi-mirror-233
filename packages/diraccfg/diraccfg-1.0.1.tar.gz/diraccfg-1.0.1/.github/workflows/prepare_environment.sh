#!/usr/bin/env bash
set -euo pipefail

PYTHON_VERSION=$1

conda create --quiet -c conda-forge -n test-env \
    python="$PYTHON_VERSION" \
    "pytest>=4.6" pylint pytest-cov pycodestyle \
    setuptools setuptools_scm wheel mypy
source "${CONDA}/bin/activate" test-env
pip install ".[testing]"
