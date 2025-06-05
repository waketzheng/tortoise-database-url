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
	pdm run fast upgrade

lock:
	pdm lock --group :all --strategy inherit_metadata

deps:
	pdm install --verbose --group :all --without=ci --frozen

bandit:
	pdm run bandit -c pyproject.toml -r .

_check:
	pdm run fast check --bandit
	pdm run twine check dist/*
check: deps _build _check

_lint:
	pdm run fast lint
	$(MAKE) bandit
lint: deps _build _lint

_test:
	pdm run fast test
test: deps _test

_style:
	pdm run fast lint --skip-mypy
style: deps _style

_build:
	rm -fR dist/
	pdm build
build: deps _build

publish: deps _build
	pdm run fast upload

venv314:
	pdm venv create 3.14

ci:
	pdm sync -d -G :all
	$(MAKE) _build
	$(MAKE) _check
	$(MAKE) _test
