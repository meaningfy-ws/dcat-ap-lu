# DCAT‑AP‑LU

**DCAT‑AP‑LU** is the Luxembourg-specific Application Profile of the DCAT‑AP standard, aligned with the [SEMIC guidelines](https://semiceu.github.io/style-guide/1.0.0/index.html) and built upon [DCAT v3](https://www.w3.org/TR/vocab-dcat-3/) and its [DCAT‑AP v3.0.1](https://semiceu.github.io/DCAT-AP/releases/3.0.1/) extension. The files in this branch are the files of DCAT-AP-LU 1.1.0 of January 2026.

## Overview

This repository hosts the **DCAT‑AP‑LU specification** and associated artefacts, including:

- **DCAT-AP-LU vocabulary** in Turtle format
- **DCAT-AP-LU vocabulary and constraints** in Turtle format
- **SHACL Shapes** 
- **Glossary** 
- **ReSpec Documentation and source files** 
- **SEMIC Conventions Report** 
- **SHACL Rule & Data Validation Test Suite** 
- **RDF/Turtle Test Data for Validation** 
- **Coverage Reports for Sample Data** 

## SHACL Validation Test Suite and Coverage Reports

The SHACL validation test suite consists of 

The test setup, based on Python, is responsible for:

- **SHACL rule validation** using RDF data fragments against the DCAT-AP-LU profile
- **Coverage reports** showing usage of profile elements among representative sample data

See [SHACLtesting.md](SHACLtesting.md) for details.

## CI/CD Pipeline

The CI/CD pipeline automates the generation of semantic web artifacts and documentation. See [CICD.md](CICD.md) for details on the pipeline architecture, stages, and artifacts.

## ReSpec Templates

For instructions on adapting the ReSpec-generated HTML pages, see [TEMPLATES.md](TEMPLATES.md) or [implementation/dcat_ap_lu/respec_resources/README.md](implementation/dcat_ap_lu/respec_resources/README.md).

## Version

`v0.0.2-rc.1` – _Release Candidate – for internal review and testing_

## Contact

Maintained by **[Meaningfy](http://meaningfy.ws/)** for the **[Ministère de la Digitalisation](https://mindigital.gouvernement.lu/) (MinDig)** and **[Luxembourg National Data Service](https://lnds.lu/) (LNDS)**.

For questions or clarifications, reach out to the editorial team via [email](mailto:hi@meaningfy.ws).

_Note: If you have any questions or discover any bugs, please put them on the [issue tracker](https://github.com/meaningfy-ws/dcat-ap-lu/issuesd) and we will address them._

## License

The documents, such as reports and specifications, are licenced under a  **CC‑BY 4.0**  licence.


