#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
Check style by `ruff` and verify type hints by `mypy`,
then run `bandit -r <package>` to find security issue.


Usage::
    ./scripts/check.py

"""

import os
import sys
from enum import IntEnum


class Tools(IntEnum):
    poetry = 0
    pdm = 1
    uv = 2
    none = 3


CMD = "fast check --skip-mypy"
_tool = Tools.pdm
BANDIT = True
TOOL = getattr(_tool, "name", str(_tool))
PREFIX = (TOOL + " run ") if TOOL and Tools.none.name != TOOL else ""
parent = os.path.abspath(os.path.dirname(__file__))
work_dir = os.path.dirname(parent)
if os.getcwd() != work_dir:
    os.chdir(work_dir)

cmd = PREFIX + CMD
if os.system(cmd) != 0:
    print("\033[1m Please run './scripts/format.py' to auto-fix style issues \033[0m")
    sys.exit(1)
cmd = PREFIX + "mypy ."
if os.system(cmd) != 0:
    sys.exit(1)

if BANDIT:
    cmd = PREFIX + "bandit -c pyproject.toml -r ."
    print("--> " + cmd)
    if os.system(cmd) != 0:
        sys.exit(1)
print("Done. ✨ 🍰 ✨")
