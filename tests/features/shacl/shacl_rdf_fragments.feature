Feature: Validate RDF data fragments against SHACL shapes

  Scenario Outline: Valid and invalid RDF data fragments should conform accordingly
    Given the RDF data fragments of the SHACL test case <test_case>
    And the full SHACL shapes graph
    When I validate the valid and invalid data against the shapes
    Then the valid data validation result should conform to <expected_valid_violation_count>
    And the invalid data validation result should conform to <expected_invalid_violation_count>

    Examples:
      | test_case                                        | expected_valid_violation_count | expected_invalid_violation_count |

      | dcat-Distribution-dcat-accessURL                 |                              0 |                                1 |
      | dcat-Dataset-dcat-distribution                   |                              0 |                                3 |
      | dcat-Dataset-dcat-keyword                        |                              0 |                                1 |
      | dcat-Dataset-dct-description                     |                              0 |                                2 |
      | dcat-Dataset-dct-title                           |                              0 |                                2 |
