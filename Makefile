help:
	@echo  "Development makefile"
	@echo
	@echo  "Usage: make <target>"
	@echo  "Targets:"
	@echo  "    up      Updates dev/test dependencies"
	@echo  "    deps    Ensure dev/test dependencies are installed"
	@echo  "    check   Checks that build is sane"
	@echo  "    test    Runs all tests"
	@echo  "    style   Auto-formats the code"
	@echo  "    lint    Auto-formats the code and check type hints"

up:
	poetry run fast upgrade

deps:
	poetry install --all-extras

bandit:
	poetry run bandit -c pyproject.toml -r .

_check:
	poetry run fast check
	$(MAKE) bandit
check: deps _build _check

_lint:
	poetry run fast lint
	$(MAKE) bandit
lint: deps _build _lint

_test:
	poetry run fast test
test: deps _test

_style:
	poetry run fast lint --skip-mypy
style: deps _style

_build:
	poetry build --clean
build: deps _build

ci:
	poetry install --all-extras --all-groups
	$(MAKE) _build
	$(MAKE) _check
	$(MAKE) _test
