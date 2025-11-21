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
TEST_DATA_DIR = tests/test_data/shacl
REPORT_DIR = reports
SCRIPT_DIR = scripts
XMI_FILE = implementation/dcat_ap_lu/xmi_conceptual_model/dcat_ap_lu_CM.xml
OWL_DIR =  implementation/dcat_ap_lu/owl_ontology
SHACL_DIR = implementation/dcat_ap_lu/shacl_shapes
SHACL_FILE = implementation/dcat_ap_lu/shacl_shapes/dcat_ap_lu_CM_shapes.ttl
UML_USAGE = $(REPORT_DIR)/uml_entities
DATA_USAGE = data_entities
SHACL_USAGE = shacl_entities
UML_SCRIPT = $(SCRIPT_DIR)/extract_uml_entities.py
EXTRACT_SCRIPT = $(SCRIPT_DIR)/extract_entity_usage.py
COVERAGE_SCRIPT = $(SCRIPT_DIR)/check_entity_coverage.py
COVERAGE_REPORT = coverage_overall

JENA_TOOLS_DIR = $(shell test ! -z ${JENA_HOME} && echo ${JENA_HOME} || echo `pwd`/jena)
JENA_TOOLS_RIOT = $(JENA_TOOLS_DIR)/bin/riot

REFERENCE_DATA_FOLDERS = $(TEST_DATA_DIR)/dcat-ap-dummy-example-1 \
	$(TEST_DATA_DIR)/dcat-ap-dummy-example-2 \
	$(TEST_DATA_DIR)/dcat-ap-dummy-example-3 \
	$(TEST_DATA_DIR)/dcat-ap-full-dummy \
	$(TEST_DATA_DIR)/dcat-ap-lu_dummy

DATA_ENTITIES_TXT = $(REPORT_DIR)/$(DATA_USAGE)/txt
DATA_ENTITIES_CSV = $(REPORT_DIR)/$(DATA_USAGE)/csv
DATA_ENTITIES_JSON = $(REPORT_DIR)/$(DATA_USAGE)/json

SHACL_ENTITIES_TXT = $(REPORT_DIR)/$(SHACL_USAGE)/txt
SHACL_ENTITIES_CSV = $(REPORT_DIR)/$(SHACL_USAGE)/csv
SHACL_ENTITIES_JSON = $(REPORT_DIR)/$(SHACL_USAGE)/json

COVERAGE_OVERALL_CSV = $(REPORT_DIR)/$(COVERAGE_REPORT)/csv
COVERAGE_OVERALL_JSON = $(REPORT_DIR)/$(COVERAGE_REPORT)/json

EXTRACT_ARGS_MUST = --prefixed --filter-csv $(UML_USAGE).csv --filter-column qualifier --filter-value mandatory
DATA_ARGS_MUST = $(DATA_ENTITIES_TXT)/$(DATA_USAGE)_must.txt --csv $(DATA_ENTITIES_CSV)/$(DATA_USAGE)_must.csv --json $(DATA_ENTITIES_JSON)/$(DATA_USAGE)_must.json
SHACL_ARGS_MUST = $(SHACL_ENTITIES_TXT)/$(SHACL_USAGE)_must.txt --csv $(SHACL_ENTITIES_CSV)/$(SHACL_USAGE)_must.csv --json $(SHACL_ENTITIES_JSON)/$(SHACL_USAGE)_must.json
COVERAGE_ARGS_MUST = --csv $(COVERAGE_OVERALL_CSV)/$(COVERAGE_REPORT)_must.csv --json $(COVERAGE_OVERALL_JSON)/$(COVERAGE_REPORT)_must.json --label MUST

EXTRACT_ARGS_SHOULD = --prefixed --filter-csv $(UML_USAGE).csv --filter-column qualifier --filter-value recommended
DATA_ARGS_SHOULD = $(DATA_ENTITIES_TXT)/$(DATA_USAGE)_should.txt --csv $(DATA_ENTITIES_CSV)/$(DATA_USAGE)_should.csv --json $(DATA_ENTITIES_JSON)/$(DATA_USAGE)_should.json
SHACL_ARGS_SHOULD = $(SHACL_ENTITIES_TXT)/$(SHACL_USAGE)_should.txt --csv $(SHACL_ENTITIES_CSV)/$(SHACL_USAGE)_should.csv --json $(SHACL_ENTITIES_JSON)/$(SHACL_USAGE)_should.json
COVERAGE_ARGS_SHOULD = --csv $(COVERAGE_OVERALL_CSV)/$(COVERAGE_REPORT)_should.csv --json $(COVERAGE_OVERALL_JSON)/$(COVERAGE_REPORT)_should.json --label SHOULD

EXTRACT_ARGS_COULD = --prefixed --filter-csv $(UML_USAGE).csv --filter-column qualifier --filter-value optional
DATA_ARGS_COULD = $(DATA_ENTITIES_TXT)/$(DATA_USAGE)_could.txt --csv $(DATA_ENTITIES_CSV)/$(DATA_USAGE)_could.csv --json $(DATA_ENTITIES_JSON)/$(DATA_USAGE)_could.json
SHACL_ARGS_COULD = $(SHACL_ENTITIES_TXT)/$(SHACL_USAGE)_could.txt --csv $(SHACL_ENTITIES_CSV)/$(SHACL_USAGE)_could.csv --json $(SHACL_ENTITIES_JSON)/$(SHACL_USAGE)_could.json
COVERAGE_ARGS_COULD = --csv $(COVERAGE_OVERALL_CSV)/$(COVERAGE_REPORT)_could.csv --json $(COVERAGE_OVERALL_JSON)/$(COVERAGE_REPORT)_could.json --label COULD

#-----------------------------------------------------------------------------
# Dev commands
#-----------------------------------------------------------------------------
install: check-uv
	@ echo "Installing dependencies using uv..."
	@ uv sync

check-uv:
	@ $(CHECK_UV)

setup-jena-tools:
	@ echo "Installing Apache Jena CLI tools locally"
	@ curl "https://archive.apache.org/dist/jena/binaries/apache-jena-4.10.0.zip" -o jena.zip
	@ unzip jena.zip
	@ mv apache-jena-4.10.0 jena
	@ echo "Done installing Jena tools, accessible at $(JENA_TOOLS_DIR)/bin"

validate:
	@ echo "Using $(JENA_TOOLS_RIOT)"
	@ echo "Validating model2owl artefacts.."
	@ $(JENA_TOOLS_RIOT) --validate $(SHACL_DIR)/*
	@ $(JENA_TOOLS_RIOT) --validate $(OWL_DIR)/*
	@ echo -n "Validating test data.."
	@ $(JENA_TOOLS_RIOT) --validate $(TEST_DATA_DIR)/*/*
	@ echo "Done validating RDF"

test:
	@ echo "Running tests..."
	@ uv run pytest $(TEST_DIR)

test-report:
	@ echo "Generating test report..."
	@ uv run pytest --html=pytest-report.html --self-contained-html $(TEST_DIR)

extract-uml-entities:
	@ uv run python $(UML_SCRIPT) $(XMI_FILE) --output $(UML_USAGE).csv

coverage-report: extract-uml-entities
	@ echo "Generating coverage reports..."
	@ mkdir -p $(DATA_ENTITIES_TXT)
	@ mkdir -p $(DATA_ENTITIES_CSV)
	@ mkdir -p $(DATA_ENTITIES_JSON)
	@ mkdir -p $(SHACL_ENTITIES_TXT)
	@ mkdir -p $(SHACL_ENTITIES_CSV)
	@ mkdir -p $(SHACL_ENTITIES_JSON)
	@ mkdir -p $(COVERAGE_OVERALL_CSV)
	@ mkdir -p $(COVERAGE_OVERALL_JSON)
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_MUST) $(TEST_DATA_DIR) > $(DATA_ARGS_MUST)
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_MUST) --shacl $(SHACL_FILE) > $(SHACL_ARGS_MUST)
	@ uv run python $(COVERAGE_SCRIPT) $(SHACL_ENTITIES_TXT)/$(SHACL_USAGE)_must.txt $(DATA_ENTITIES_TXT)/$(DATA_USAGE)_must.txt $(COVERAGE_ARGS_MUST)
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_SHOULD) $(TEST_DATA_DIR) > $(DATA_ARGS_SHOULD)
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_SHOULD) --shacl $(SHACL_FILE) > $(SHACL_ARGS_SHOULD)
	@ uv run python $(COVERAGE_SCRIPT) $(SHACL_ENTITIES_TXT)/$(SHACL_USAGE)_should.txt $(DATA_ENTITIES_TXT)/$(DATA_USAGE)_should.txt $(COVERAGE_ARGS_SHOULD)
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_COULD) $(TEST_DATA_DIR) > $(DATA_ARGS_COULD)
	@ uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_COULD) --shacl $(SHACL_FILE) > $(SHACL_ARGS_COULD)
	@ uv run python $(COVERAGE_SCRIPT) $(SHACL_ENTITIES_TXT)/$(SHACL_USAGE)_could.txt $(DATA_ENTITIES_TXT)/$(DATA_USAGE)_could.txt $(COVERAGE_ARGS_COULD)

# for generating reports based on specific test data folders
coverage-report-by-data: extract-uml-entities
	@echo "Generating reports for each test data folder..."
	@for folder in $(REFERENCE_DATA_FOLDERS); do \
		name=$$(basename $$folder); \
		output_dir=$(REPORT_DIR)/coverage_by_data/$$name; \
		echo "Processing $$folder..."; \
		mkdir -p $$output_dir/{shacl,data}/txt $$output_dir/{shacl,data,coverage}/csv $$output_dir/{shacl,data,coverage}/json; \
		uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_MUST) $$folder > $$output_dir/data/txt/$(DATA_USAGE)_must.txt; \
		uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_MUST) --shacl $(SHACL_FILE) > $$output_dir/shacl/txt/$(SHACL_USAGE)_must.txt; \
		uv run python $(COVERAGE_SCRIPT) $$output_dir/shacl/txt/$(SHACL_USAGE)_must.txt $$output_dir/data/txt/$(DATA_USAGE)_must.txt --csv $$output_dir/coverage/csv/coverage_$${name}_must.csv --json $$output_dir/coverage/json/coverage_$${name}_must.json --label MUST; \
		uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_SHOULD) $$folder > $$output_dir/data/txt/$(DATA_USAGE)_should.txt; \
		uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_SHOULD) --shacl $(SHACL_FILE) > $$output_dir/shacl/txt/$(SHACL_USAGE)_should.txt; \
		uv run python $(COVERAGE_SCRIPT) $$output_dir/shacl/txt/$(SHACL_USAGE)_should.txt $$output_dir/data/txt/$(DATA_USAGE)_should.txt --csv $$output_dir/coverage/csv/coverage_$${name}_should.csv --json $$output_dir/coverage/json/coverage_$${name}_should.json --label SHOULD; \
		uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_COULD) $$folder > $$output_dir/data/txt/$(DATA_USAGE)_could.txt; \
		uv run python $(EXTRACT_SCRIPT) $(EXTRACT_ARGS_COULD) --shacl $(SHACL_FILE) > $$output_dir/shacl/txt/$(SHACL_USAGE)_could.txt; \
		uv run python $(COVERAGE_SCRIPT) $$output_dir/shacl/txt/$(SHACL_USAGE)_could.txt $$output_dir/data/txt/$(DATA_USAGE)_could.txt --csv $$output_dir/coverage/csv/coverage_$${name}_could.csv --json $$output_dir/coverage/json/coverage_$${name}_could.json --label COULD; \
	done
