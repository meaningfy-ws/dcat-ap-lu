Feature: Validate RDF fragments against SHACL shapes

  Scenario Outline: Valid and invalid RDF fragments should conform accordingly
    Given the valid RDF data fragment of <data_shape>
    And the invalid RDF data fragment of <data_shape>
    And the full shapes graph
    When I validate the valid data against the shapes
    And I validate the invalid data against the shapes
    Then the valid result should conform to <expected_valid_result>
    And the invalid result should conform to <expected_invalid_result>
    And the valid result count should be <expected_valid_count>
    And the invalid result count should be <expected_invalid_count>

    Examples:
      | data_shape                       | expected_valid_result | expected_invalid_result | expected_valid_count | expected_invalid_count |
      | dcat-Distribution-dcat-mediaType | True                  | False                   |                    0 |                      3 |
