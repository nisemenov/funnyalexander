SHELL := /bin/bash
# =============================================================================
# Tests, Linting, Coverage
# =============================================================================
.PHONY: lint
lint: 												## Runs pre-commit hooks; includes ruff linting, ruff formatting, codespell
	@echo "=> Running pre-commit process"
	@uv run pre-commit run --all-files
	@echo "=> Pre-commit complete"

.PHONY: test
test:  												## Run the tests
	@echo "=> Running test cases"
	@uv run pytest tests
	@echo "=> Tests complete"
