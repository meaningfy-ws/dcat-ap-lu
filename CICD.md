# CI/CD Pipeline

*What happens when you push, and where to find outputs*

The **CI/CD pipeline**:

- Transforms UML conceptual models into OWL ontologies and SHACL shapes
- Generates ReSpec HTML documentation
- Deploys to GitLab Pages

## Pipeline Flow

```text
┌─────────────────────┐     ┌─────────────┐     ┌─────────┐
│ report_and_glossary │ ──► │  transform  │ ──► │  test   │
└─────────────────────┘     └─────────────┘  │  └─────────┘
                                             │
                                             │  ┌──────────────────┐     ┌─────────┐
                                             └► │  generate_respec │ ──► │  pages  │
                                                └──────────────────┘     └─────────┘
```

After `transform` completes, `test` and `generate_respec` run in parallel. The `test` job only runs on `main`, `develop`, `feature/*`, and `release/*` branches. The `pages` job only runs on `main` and `master`.

## Artifacts

The GitLab CI pipeline stores generated files as **pipeline artifacts** rather than committing them back to the repository.

### Pipeline Outputs

Each step of the pipeline generates files that serve as dependencies for subsequent jobs. These outputs can also be downloaded directly from the GitLab interface. The repository contains reference versions at the paths listed below; these are not automatically updated but can be refreshed manually.

| Output | Contents |
| ------ | -------- |
| **report-and-glossary** | Convention report and glossary HTML |
| **transform** | OWL ontology and SHACL shapes (`.ttl`, `.rdf`) |
| **respec** | ReSpec build output (same content as pages, as downloadable files) |
| **dcat-ap-lu-test-reports** | pytest report and coverage data |
| **pages** | Published GitLab Pages site |

Reference versions are stored in the repository at:

```text
implementation/dcat_ap_lu/
├── conventions_report/     # report-and-glossary output
├── owl_ontology/           # transform output (OWL)
├── shacl_shapes/           # transform output (SHACL)
└── respec/                 # respec output / pages source
glossary/                   # report-and-glossary output
reports/                    # test reports
pytest-report.html          # test report
```

Take note: The **pages** and **transform** outputs are retained indefinitely. Other outputs are retained for 1 week; the pipeline can be re-run at any time to regenerate them.

### Downloading outputs

From the pipeline overview page (**Build → Pipelines**), click the **Download artifacts** button (download icon) next to any job.

### Migrating from GitHub Actions

This pipeline was migrated from GitHub Actions. The GitHub Actions workflow automatically committed generated files back to the repository after each run. The GitLab CI approach stores outputs as pipeline artifacts instead, leaving the repository unchanged. This results in a cleaner git history, clearer separation between source and generated content, and eliminates the need for repository write tokens.

| Aspect | GitHub Actions | GitLab CI |
| ------ | -------------- | --------- |
| **Data passing** | Git commits pushed between jobs | Artifacts passed via `needs:` |
| **Checkout** | `actions/checkout` fetches latest HEAD | Checks out original trigger commit |
| **Deployment** | GitHub Pages can serve per-branch | GitLab Pages serves single `public/` folder |
