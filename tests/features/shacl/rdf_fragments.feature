Feature: Validate RDF data fragments against SHACL shapes

  Scenario Outline: Valid and invalid RDF data fragments should conform accordingly
    Given the RDF data fragments of the SHACL test case <test_case>
    And the full SHACL shapes graph
    When I validate the valid and invalid data against the shapes
    Then the valid data validation result should conform to <expected_valid_violation_count>
    And the invalid data validation result should conform to <expected_invalid_violation_count>

    Examples:
      | test_case                        | expected_valid_violation_count | expected_invalid_violation_count |
      | dcat-Distribution-dcat-mediaType |                              0 |                                3 |
