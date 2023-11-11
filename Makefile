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

# .PHONY: test
# test:
# 	poetry run pythom -m unittest tests/

.PHONY: build
build:
	poetry build

# prints out the commands to run to tag the release and push it
.PHONY: tag
tag:
	@echo "Run $(BOLD)git tag -a $(VERSION) -m <message>$(NORMAL) to tag the release"
	@echo "Then run $(BOLD)git push upstream $(VERSION)$(NORMAL) to push the tag"
