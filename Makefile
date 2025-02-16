SHELL := /bin/bash
# =============================================================================
# Tests, Linting, Coverage
# =============================================================================
.PHONY: test
test:  												## Run the tests
	@echo "=> Running test cases"
	@uv run pytest tests -sv
	@echo "=> Tests complete"
