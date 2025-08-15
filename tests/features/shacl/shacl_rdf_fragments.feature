Feature: Validate RDF data fragments against SHACL shapes

  Scenario Outline: Valid and invalid RDF data fragments should conform accordingly
    Given the RDF data fragments of the SHACL test case <test_case>
    And the full SHACL shapes graph
    When I validate the valid and invalid data against the shapes
    Then the valid data validation result should conform to <expected_valid_violation_count>
    And the invalid data validation result should conform to <expected_invalid_violation_count>

    Examples:
      | test_case                             | expected_valid_violation_count | expected_invalid_violation_count |
      | dcat-Distribution-dcat-mediaType      |                              0 |                                3 |
      | dcat-Distribution-dcatap-availability |                              0 |                                3 |
      | dcat-Distribution-adms-status         |                              0 |                                4 |
      | dcat-Distribution-dcat-accessService  |                              0 |                                2 |
      | dcat-Distribution-dcat-accessURL      |                              0 |                                1 |
      | dcat-Distribution-dcat-byteSize       |                              0 |                                3 |
      | dcat-Distribution-dcat-compressFormat |                              0 |                                3 |
      | dcat-Distribution-dcat-downloadURL    |                              0 |                                0 |
      | dcat-Distribution-dcat-packageFormat  |                              0 |                                 3|
      | dcat-Distribution-dcat-spatialResolutionInMeters  |                  0 |                                 1|
      | dcat-Distribution-dcat-temporalResolution  |                         0 |                                 0|
      | dcat-Distribution-dcatap-applicablelegislation  |                    0 |                                 2|
      | dcat-Distribution-dct-conformsTo       |                             0 |                                 2|
      | dcat-Distribution-dct-description      |                             0 |                                 0|
      | dcat-Distribution-dct-format           |                             0 |                                 3|
      | dcat-Distribution-dct-issued           |                             0 |                                 3|
      | dcat-Distribution-dct-language         |                             0 |                                 3|
      | dcat-Distribution-dct-license          |                             0 |                                 4|
      | dcat-Distribution-dct-modified         |                             0 |                                 2|
      | dcat-Distribution-dct-rights           |                             0 |                                 3|
      |dcat-Distribution-dct-title             |                              0|                                  0|
      |dcat-Distribution-foaf-page             |                              0|                                  3|
      |dcat-Distribution-odrl-hasPolicy        |                              0|                                  3|
      |dcat-Distribution-spdx-checksum         |                              0|                                  3|
      |adms-Identifier-skos-notation           |                              0|                                  1|
      |dcat-Dataset-adms-identifier            |                              0|                                 2|
      |dcat-Dataset-adms-sample                |                              0|                                 3|
      |dcat-Dataset-adms-versionNotes          |                              0|                                 0|
      |dcat-Dataset-dcat-contactPoint          |                              0|                                 2|
      |dcat-Dataset-dcat-distribution          |                              0|                                 2|
      |dcat-Dataset-dcat-inSeries              |                              0|                                 4|
      |dcat-Dataset-dcat-keyword               |                              0|                                 4|
      |dcat-Dataset-dcat-landingPage           |                              0|                                 2|
      |dcat-Dataset-dcat-spatialResolutionInMeters       |                    0|                                 2|
      |dcat-Dataset-dcat-temporalResolution              |                    0|                                 1|
      |dcat-Dataset-dcat-theme              |                0|                              2|
      |dcat-Dataset-dcatap-applicablelegislation             |                0|                              2|
      |dcat-Dataset-dct-accessRights             |                0|                              2|
      |dcat-Dataset-dct-accrualPeriodicity             |                       0|                              3|
      |dcat-Dataset-dct-conformsTo             |                               0|                              2|
      |dcat-Dataset-dct-creator             |                               0|                             3|
      |dcat-Dataset-dct-description             |                               0|                             3|
      |dcat-Dataset-dct-hasVersion             |                               0|                             2|


