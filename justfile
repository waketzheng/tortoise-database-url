#!/usr/bin/env -S just --justfile
# Keep this as a small command index. Workflow details live in pyproject.toml.

default:
    @just --list

PY_EXEC := if os_family() == "windows" { ".venv/Scripts/python.exe" } else { ".venv/bin/python" }

# Create or update the local virtualenv.
[unix]
venv *args:
    @if test ! -e .venv; then just _venv {{ args }}; fi
[windows]
venv *args:
    @if (-Not (Test-Path '.venv')) { just _venv {{ args }}}

_venv *args:
    pdm venv create --with-pip --with uv {{ args }}

# Normalize uv.lock registry URLs to PyPI.
pypi *args:
    pdm run pypi {{ args }}

# Install all development dependencies.
deps *args:
    pdm run deps {{ args }}

# Refresh uv.lock without upgrading versions.
lock *args:
    @just pypi --quiet --reverse
    uv lock {{ args }}
    @just deps --frozen
    @just pypi --quiet

add *args:
    @just pypi --quiet --reverse
    uv add {{ args }}
    @just pypi --quiet

# Upgrade dependencies.
up *args:
    @just lock --upgrade {{ args }}

# Install production dependencies only.
prod *args:
    pdm run prod {{ args }}

# Install pre-commit hooks and dependencies.
start:
    prek install
    @just deps

# Format code.
style *args: deps
    pdm run style {{ args }}

alias fmt := style

# Lint code.
lint *args: deps
    @just _lint {{ args }}

_lint *args:
    pdm run lint {{ args }}
    @just _codeqc

_codeqc:
    @just pyright
    @just mypy

# Run static checks.
check *args: build
    pdm run check {{ args }}
    @just _codeqc
    pdm run twine check dist/*

_uvx *args:
    uvx --python={{ PY_EXEC }} {{ args }}

pyright path="src" *args: venv
    @just _uvx pyright --pythonpath={{ PY_EXEC }} {{ path }} {{ args }}

mypy path="src" *args:
    @just _uvx mypy --python-executable={{ PY_EXEC }} {{ path }} {{ args }}

# Run tests.
test *args: deps
    @just _test {{ args }}

_test *args:
    pdm run test {{ args }}

# Build distribution files.
build *args: deps
    uv build {{ args }}

_build *args:
    uv build --offline {{ args }}

# Run the local CI workflow.
ci:
    pdm run ci

# Show dependency tree.
tree *args:
    pdm run tree {{ args }}

# Bump patch version and commit the change.
bump *args:
    pdm run bump {{ args }}

# Bump minor version(0.1.1->0.2.0), commit and tag.
minor *args: deps
    pdm run fast bump minor --commit {{args}}
    @just tag

# Create a release tag.
tag *args:
    pdm run tag {{ args }}

# Bump patch version and tag it.
release:
    pdm run release
