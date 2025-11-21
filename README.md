# DCAT‑AP‑LU

**DCAT‑AP‑LU** is the Luxembourg-specific Application Profile of the DCAT‑AP standard, aligned with the [SEMIC guidelines](https://semiceu.github.io/style-guide/1.0.0/index.html) and built upon [DCAT‑AP v3](https://www.w3.org/TR/vocab-dcat-3/).

## Overview

This repository hosts the **DCAT‑AP‑LU specification** and associated artefacts, including:

- **DCAT-AP-LU vocabulary:** [dcat-ap-lu vocabulary in Turtle format](https://github.com/meaningfy-ws/dcat-ap-lu/blob/main/implementation/dcat_ap_lu/owl_ontology/dcat_ap_lu_CM.ttl)
- **DCAT-AP-LU vocabulary and constraints:** [dcat-ap-lu vocabulary and constraints in Turtle format](https://github.com/meaningfy-ws/dcat-ap-lu/blob/main/implementation/dcat_ap_lu/owl_ontology/dcat_ap_lu_CM_restrictions.ttl)
- **SHACL Shapes:** [dcat-ap-lu SHACL Shapes](https://github.com/meaningfy-ws/dcat-ap-lu/blob/main/implementation/dcat_ap_lu/shacl_shapes/dcat_ap_lu_CM_shapes.ttl)
- **Glossary:** [dcat-ap-lu Glossary](https://github.com/meaningfy-ws/dcat-ap-lu/blob/main/glossary/dcat_ap_lu_CM_glossary.html)
- **ReSpec Documentation:** [dcat-ap-lu ReSpec Documentation](https://github.com/meaningfy-ws/dcat-ap-lu/blob/main/implementation/dcat_ap_lu/respec_report/dcat_ap_lu_respec.html)
- **Conventions Report:** [dcat-ap-lu Conventions Report](https://github.com/meaningfy-ws/dcat-ap-lu/blob/main/implementation/dcat_ap_lu/conventions_report/dcat_ap_lu_CM_convention_report.html)
- **SHACL Rule & Data Validation Test Suite:**  [dcat-ap-lu SHACL Validation](https://github.com/meaningfy-ws/dcat-ap-lu/tree/main/tests/features/shacl/)
- **RDF/Turtle Test Data for Validation:** [dcat-ap-lu Test Data](https://github.com/meaningfy-ws/dcat-ap-lu/tree/main/tests/test_data/shacl/)
- **Coverage Reports for Sample Data:**  [dcat-ap-lu Coverage Reports](https://github.com/meaningfy-ws/dcat-ap-lu/tree/main/reports/coverage_by_data/)

## SHACL Validation Test Suite and Coverage Reports

The test setup, based on Python, is responsible for:

- **SHACL rule validation** using RDF data fragments against the DCAT-AP-LU profile
- **Coverage reports** showing usage of profile elements among representative sample data

The rule validation is done with [pytest-bdd](https://pytest-bdd.readthedocs.io/en/latest/#) based on the idea of [behaviour-driven development](https://cucumber.io/docs/bdd/) (BDD), where data fragments serve as fixtures or examples and are tested with a single, naturally-described [Gherkin](https://cucumber.io/docs/gherkin/reference) [scenario outline](https://pytest-bdd.readthedocs.io/en/latest/#scenario-outlines).

The coverage reports are generated using custom Python scripts that analyse the UML XMI, SHACL and RDF data and produce reports in CSV, JSON and in some cases plain text.

The tests are run automatically on every push so that divergence from the model can be captured continuously, but this can be configured with the relevant GitHub CI workflow `.github/workflows/tests.yml` so as to run selectively, like on PRs only.

_Note: Currently, due to a technicality, failures in the Gherkin tests fail the workflow, but failures in coverage report generation do not. The Gherkin and overall coverage tests produce HTML & JSON reports which are made available as an artefact of the workflow run._

### Testing Environment

Python (at least version 3.9) should be installed from [official sources](https://www.python.org/downloads/), but [pyenv](https://github.com/pyenv/pyenv)[(-win)](https://github.com/pyenv-win/pyenv-win) and the [conda](https://docs.conda.io/projects/conda/en/latest/index.html) tool (if you don't mind all the data science baggage) are good options as well.

The project uses the [uv](https://docs.astral.sh/uv/) package manager which takes care of setting up a runtime environment. You may still prefer to create a local virtual environment beforehand which will isolate the installation from your system Python:

```bash
python -m venv .venv
source .venv/bin/activate
```

Run `deactivate` to exit out of this environment at any time.

Your Python programming IDE of choice should also have a way to select
this as the "interpreter runtime".

### Installation

Installation is as simple as running Make, which defaults to `make install` and takes care of getting `uv` and installing prerequisite software/library dependencies.

```bas
make
```

If you don't have Make, it (and other UNIX/Bash tools) may be accessible on Windows 10+ via [Chocolatey](https://chocolatey.org/install) (the WinGet version may be problematic) and on Mac via [HomeBrew](https://brew.sh/).

We provide a traditional `requirements.txt` so you may also do the installation via Pip, if you know what you're doing.

### Usage

For manual testing of individual data files, you can use the `scripts/validation_runner.py` script. For example:

```bash
python scripts/validation_runner.py -d tests/test_data/shacl/dcat-ap-lu_dummy/dcat-ap-lu_dummy.ttl # or only -h to see all options
```

Run all SHACL automated rule validation tests with:

```bash
make test
```

Produce coverage reports for _all_ test data (including representative samples/examples) with:

```bash
make coverage-report
```

Produce coverage reports for a set of predefined sample dataset with:

```bash
make coverage-report-by-data
```

If you still find yourself without Make, you can run the underlying commands directly (with or without `uv`). See the `Makefile` for details.

The coverage reports are generated under the `reports/` folder. The `data_entities` and `shacl_entities` subfolders contain intermediate reports that may be useful for debugging or further analysis. The `coverage_by_data` subfolder contains the reports for the predefined sample datasets (with their own `data` and `shacl` intermediates).

What you are interested in are the `coverage_overall.*` files (named according to a MoSCow qualifier, information about which is extracted from the model and stored in the `uml_entities.csv` file) and the `coverage` subfolder per dataset under `coverage_by_data`.

## Version

`v0.0.1-rc.1` – _Release Candidate – for internal review and testing_

## Contact

Maintained by **[Meaningfy](http://meaningfy.ws/)** for the **[Ministère de la Digitalisation](https://mindigital.gouvernement.lu/) (MinDig)** and **[Luxembourg National Data Service](https://lnds.lu/) (LNDS)**.

For questions or clarifications, reach out to the editorial team via [email](mailto:hi@meaningfy.ws).

_Note: If you have any questions or discover any bugs, please put them on the [issue tracker](https://github.com/meaningfy-ws/dcat-ap-lu/issuesd) and we will address them._

## License

The documents, such as reports and specifications, are licenced under a  **CC‑BY 4.0**  licence.
