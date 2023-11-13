# Inspired by https://github.com/snakemake/snakefmt/blob/master/Makefile
PROJECT = plasnet
OS := $(shell uname -s)
VERSION := $(shell poetry version -s)
BOLD := $(shell tput bold)
NORMAL := $(shell tput sgr0)

.PHONY: all
all: install

.PHONY: install
install:
	poetry install

.PHONY: install-ci
install-ci:
	poetry install --no-interaction
	poetry run plasnet --version

.PHONY: pre-commit
pre-commit:
	poetry run pre-commit run --all-files -v

.PHONY: test
test:
	poetry run python -m unittest discover -s tests -t .

.PHONY: build
build:
	poetry build
