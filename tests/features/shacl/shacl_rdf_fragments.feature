Feature: Validate RDF data fragments against SHACL shapes

  Scenario Outline: Valid and invalid RDF data fragments should conform accordingly
    Given the RDF data fragments of the SHACL test case <test_case>
    And the full SHACL shapes graph
    When I validate the valid and invalid data against the shapes
    Then the valid data validation result should conform to <expected_valid_violation_count>
    And the invalid data validation result should conform to <expected_invalid_violation_count>

    Examples:
      | test_case                                        | expected_valid_violation_count | expected_invalid_violation_count |
      | dcat-Distribution-dcat-mediaType                 |                              0 |                                4 |
      | dcat-Distribution-dcatap-availability            |                              1 |                                6 |
      | dcat-Distribution-adms-status                    |                              0 |                                4 |
      | dcat-Distribution-dcat-accessService             |                              0 |                                3 |
      | dcat-Distribution-dcat-accessURL                 |                              0 |                                1 |
      | dcat-Distribution-dcat-byteSize                  |                              1 |                                4 |
      | dcat-Distribution-dcat-compressFormat            |                              0 |                                3 |
      | dcat-Distribution-dcat-downloadURL               |                              2 |                                2 |
      | dcat-Distribution-dcat-packageFormat             |                              1 |                                6 |
      | dcat-Distribution-dcat-spatialResolutionInMeters |                              1 |                                2 |
      | dcat-Distribution-dcat-temporalResolution        |                              1 |                                2 |
      | dcat-Distribution-dcatap-applicableLegislation   |                              1 |                                3 |
      | dcat-Distribution-dct-conformsTo                 |                              0 |                                3 |
      | dcat-Distribution-dct-description                |                              0 |                                1 |
      | dcat-Distribution-dct-format                     |                              0 |                                6 |
      | dcat-Distribution-dct-issued                     |                              0 |                                3 |
      | dcat-Distribution-dct-language                   |                              0 |                                3 |
      | dcat-Distribution-dct-license                    |                              0 |                                8 |
      | dcat-Distribution-dct-modified                   |                              0 |                                2 |
      | dcat-Distribution-dct-rights                     |                              1 |                                5 |
      | dcat-Distribution-dct-title                      |                              0 |                                1 |
      | dcat-Distribution-foaf-page                      |                              0 |                                4 |
      | dcat-Distribution-odrl-hasPolicy                 |                              0 |                                4|
      | dcat-Distribution-spdx-checksum                  |                              0 |                                8|
      | dcat-Dataset-adms-identifier                     |                              0 |                                4 |
      | dcat-Dataset-adms-sample                         |                              0 |                                6 |
      | dcat-Dataset-adms-versionNotes                   |                              0 |                                1 |
      | dcat-Dataset-dcat-contactPoint                   |                              0 |                                3 |
      | dcat-Dataset-dcat-distribution                   |                              0 |                                3 |
      | dcat-Dataset-dcat-inSeries                       |                              0 |                                2 |
      | dcat-Dataset-dcat-keyword                        |                              0 |                                1 |
      | dcat-Dataset-dcat-landingPage                    |                              0 |                                2 |
      | dcat-Dataset-dcat-spatialResolutionInMeters      |                              0 |                                2 |
      | dcat-Dataset-dcat-temporalResolution             |                              0 |                                3 |
      | dcat-Dataset-dcat-theme                          |                              0 |                                3 |
      | dcat-Dataset-dcatap-applicableLegislation        |                              0 |                                4 |
      | dcat-Dataset-dct-rights                          |                              0 |                                4 |
      | dcat-Dataset-dct-accrualPeriodicity              |                              0 |                                5 |
      | dcat-Dataset-dct-conformsTo                      |                              0 |                                3 |
      | dcat-Dataset-dct-creator                         |                              0 |                                3 |
      | dcat-Dataset-dct-description                     |                              0 |                                2 |
      | dcat-Dataset-dcat-hasVersion                     |                              0 |                                4 |
      | dcat-Dataset-dct-identifier                      |                              0 |                                2 |
      | dcat-Dataset-dct-isReferencedBy                  |                              1 |                                2 |
      | dcat-Dataset-dct-issued                          |                              0 |                                1 |
      | dcat-Dataset-dct-language                        |                              0 |                                3 |
      | dcat-Dataset-dct-modified                        |                              0 |                                1|
      | dcat-Dataset-dct-provenance                      |                              0 |                                4 |
      | dcat-Dataset-dct-publisher                       |                              0 |                                5 |
      | dcat-Dataset-dct-relation                        |                              0  |                                2 |
      | dcat-Dataset-dct-source                          |                              0 |                                5 |
      | dcat-Dataset-dct-spatial                         |                              0 |                                3 |
      | dcat-Dataset-dct-temporal                        |                              0 |                                1 |
      | dcat-Dataset-dct-title                           |                              0 |                                2 |
      | dcat-Dataset-dct-type                            |                              0 |                                1 |
      | dcat-Dataset-dpv-hasData                         |                              0 |                                1 |
      | dcat-Dataset-foaf-page                           |                              0 |                                2 |
      | dcat-Dataset-prov-qualifiedAttribution           |                              0 |                                1 |
      | dcat-Dataset-dcat-qualifiedRelation              |                              0 |                                1 |
      | dcat-Dataset-prov-wasGeneratedBy                 |                              1 |                                4 |
      | dcat-DatasetSeries-dcat-contactPoint             |                              0 |                                2 |
      | dcat-DatasetSeries-dcatap-applicableLegislation  |                              0 |                                2 |
      | dcat-DatasetSeries-dct-publisher                 |                              0 |                                2 |
      | dcat-DatasetSeries-dct-spatial                   |                              0 |                                2 |
      | dct-LicenseDocument-dct-type                     |                              0 |                                2 |
      | dct-Location-locn-geometry                       |                              0 |                                3 |
      | dct-PeriodOfTime-dcat-endDate                    |                              0 |                                1 |
      | dct-PeriodOfTime-time-hasBeginning               |                              0 |                                3 |
      | dct-PeriodOfTime-time-hasEnd                     |                              0 |                                3 |
      | foaf-Agent-dct-type                              |                              0 |                                3 |
      | skos-Concept-skos-prefLabel                      |                              0 |                                1 |
      | dcat-Catalog-dcat-record                         |                              0 |                                2 |
      | dcat-CatalogRecord-foaf-primaryTopic             |                              0 |                                4 |
      | dcat-Catalog-dcat-service                        |                              0 |                                2 |
      | dcat-Catalog-dct-creator                         |                              0 |                                3 |
      | dcat-Catalog-dct-license                         |                              0 |                                3 |
      | dcat-Catalog-dct-publisher                       |                              0 |                                3 |
      | dct-PeriodOfTime-dcat-startDate                  |                              0 |                                1 |

