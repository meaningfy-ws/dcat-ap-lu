import pytest
from pyshacl import validate
from rdflib import Graph

from tests.unit.shacl import TEST_DATA_FOLDER, DEFAULT_RDF_FORMAT

TEST_FILE_NAME = "dcat-Distribution-dcat-mediaType"
TEST_DATA_FOLDER = TEST_DATA_FOLDER / TEST_FILE_NAME


@pytest.fixture(scope="module")
def valid_data():
    return Graph().parse(
        TEST_DATA_FOLDER / f"{TEST_FILE_NAME}_valid.{DEFAULT_RDF_FORMAT}",
        format="turtle",
    )


@pytest.fixture(scope="module")
def invalid_data():
    return Graph().parse(
        TEST_DATA_FOLDER / f"{TEST_FILE_NAME}_invalid.{DEFAULT_RDF_FORMAT}",
        format="turtle",
    )


@pytest.mark.parametrize(
    "test_data, should_conform, expected_result_count",
    [("valid_data", True, 0), ("invalid_data", False, 3)],
)
def test_shacl_validation(
    ns, request, full_shacl_shapes, test_data, should_conform, expected_result_count
):
    data_graph = request.getfixturevalue(test_data)
    conforms, report_graph, _ = validate(data_graph, shacl_graph=full_shacl_shapes)

    assert (
        conforms == should_conform
    ), f"SHACL validation failed:\n{report_graph.serialize()}"

    result_count = sum(
        1 for _ in report_graph.subjects(ns.RDF.type, ns.SH.ValidationResult)
    )

    assert (
        result_count == expected_result_count
    ), f"SHACL validation failed:\n{report_graph.serialize()}"


if __name__ == "__main__":
    pytest.main()
