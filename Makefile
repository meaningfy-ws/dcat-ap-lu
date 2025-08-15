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
XMI_FILE = implementation/dcat_ap_lu/xmi_conceptual_model/dcat_ap_lu_CM.xml
SHACL_FILE = implementation/dcat_ap_lu/shacl_shapes/dcat_ap_lu_CM_shapes.ttl
UML_USAGE = $(REPORT_DIR)/uml_entities
DATA_USAGE = $(REPORT_DIR)/data_entities
SHACL_USAGE = $(REPORT_DIR)/shacl_entities
UML_SCRIPT = $(SCRIPT_DIR)/extract_uml_entities.py
EXTRACT_SCRIPT = $(SCRIPT_DIR)/extract_entity_usage.py
COVERAGE_SCRIPT = $(SCRIPT_DIR)/check_entity_coverage.py
COVERAGE_REPORT = $(REPORT_DIR)/entity_coverage_report

EXTRACT_ARGS_MUST = --prefixed --filter-csv $(UML_USAGE).csv --filter-column qualifier --filter-value mandatory
DATA_ARGS_MUST = $(DATA_USAGE).txt --csv $(DATA_USAGE).csv --json $(DATA_USAGE).json
SHACL_ARGS_MUST = $(SHACL_USAGE).txt --csv $(SHACL_USAGE).csv --json $(SHACL_USAGE).json
COVERAGE_ARGS_MUST = --csv $(COVERAGE_REPORT).csv --json $(COVERAGE_REPORT).json

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
	@ uv run python $(UML_SCRIPT) $(XMI_FILE) --output $(UML_USAGE).csv
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_MUST) $(TEST_DATA_DIR) > $(DATA_ARGS_MUST)
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_MUST) --shacl $(SHACL_FILE) > $(SHACL_ARGS_MUST)
	@ uv run python $(COVERAGE_SCRIPT) $(SHACL_USAGE).txt $(DATA_USAGE).txt $(COVERAGE_ARGS_MUST)
