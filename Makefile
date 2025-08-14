ifeq ($(OS),Windows_NT)
	SHELL := powershell.exe
	.SHELLFLAGS := -NoProfile -Command
	CHECK_UV := if (!(Get-Command uv -ErrorAction SilentlyContinue)) { \
		Write-Host "uv not found. Installing uv..."; \
		powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"; \
		$$env:Path = "C:\Users\$$env:USERNAME\.local\bin;$$env:Path"; \
	}
else
	SHELL := /bin/bash -o pipefail
	CHECK_UV := command -v uv >/dev/null 2>&1 || { \
		echo "uv not found. Installing uv..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	}
endif

TEST_DIR = tests
TEST_DATA_DIR = tests/test_data
REPORT_DIR = reports
SCRIPT_DIR = scripts
SHACL_FILE = implementation/dcat_ap_lu/shacl_shapes/dcat_ap_lu_CM_shapes.ttl
DATA_USAGE = $(REPORT_DIR)/data_entities
SHACL_USAGE = $(REPORT_DIR)/shacl_entities
EXTRACT_SCRIPT = $(SCRIPT_DIR)/extract_entity_usage.py
COVERAGE_SCRIPT = $(SCRIPT_DIR)/check_entity_coverage.py
COVERAGE_REPORT = $(REPORT_DIR)/entity_coverage_report

#-----------------------------------------------------------------------------
# Dev commands
#-----------------------------------------------------------------------------
install: check-uv
	@ echo "Installing dependencies using uv..."
	@ uv sync

check-uv:
	@ $(CHECK_UV)

test:
	@ echo "Running tests..."
	@ uv run pytest $(TEST_DIR)

coverage_report:
	@ echo "Generating coverage report..."
	@ uv run python $(EXTRACT_SCRIPT) $(TEST_DATA_DIR) --prefixed > $(DATA_USAGE).txt --csv $(DATA_USAGE).csv --json $(DATA_USAGE).json
	@ uv run python $(EXTRACT_SCRIPT) --shacl $(SHACL_FILE) --prefixed > $(SHACL_USAGE).txt --csv $(SHACL_USAGE).csv --json $(SHACL_USAGE).json
	@ uv run python $(COVERAGE_SCRIPT) $(SHACL_USAGE).txt $(DATA_USAGE).txt --csv $(COVERAGE_REPORT).csv --json $(COVERAGE_REPORT).json
