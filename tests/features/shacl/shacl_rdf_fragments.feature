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
