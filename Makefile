SRC_DIR := plasnet

.PHONY: format lint type_check

pre_commit: format lint type_check

# Format code with black and isort
format:
	@echo "Formatting code..."
	@black $(SRC_DIR)
	@isort $(SRC_DIR)

# Lint code with flake8
lint:
	@echo "Linting code..."
	@flake8 $(SRC_DIR)

# Type check code with mypy
type_check:
	@echo "Type checking..."
	@mypy $(SRC_DIR)
