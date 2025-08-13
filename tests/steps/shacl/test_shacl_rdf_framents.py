from types import SimpleNamespace
from pyshacl import validate
from rdflib import Graph
from tests.unit.shacl import TEST_DATA_FOLDER, DEFAULT_RDF_FORMAT

from pytest_bdd import given, scenarios, then, when, parsers


scenarios("../../features/shacl/shacl_rdf_fragments.feature")


@given(
    parsers.parse("the RDF data fragments of the SHACL test case {shacl_test_case}"),
    target_fixture="test_data_graphs",
)
def get_test_data_graphs(shacl_test_case: str) -> tuple[Graph, Graph]:
    valid_data_graph = Graph().parse(
        TEST_DATA_FOLDER
        / shacl_test_case
        / f"{shacl_test_case}_valid.{DEFAULT_RDF_FORMAT}",
        format=DEFAULT_RDF_FORMAT,
    )
    invalid_data_graph = Graph().parse(
        TEST_DATA_FOLDER
        / shacl_test_case
        / f"{shacl_test_case}_invalid.{DEFAULT_RDF_FORMAT}",
        format=DEFAULT_RDF_FORMAT,
    )
    return valid_data_graph, invalid_data_graph


@given("the full SHACL shapes graph", target_fixture="shapes_graph")
def get_shapes_graph(full_shacl_shapes: Graph) -> Graph:
    return full_shacl_shapes


@when(
    "I validate the valid and invalid data against the shapes",
    target_fixture="validation_result_graphs",
)
def get_validation_result_graphs(
    test_data_graphs: tuple[Graph, Graph], shapes_graph: Graph
) -> tuple[Graph, Graph]:
    valid_data_graph, invalid_data_graph = test_data_graphs
    _, valid_report_graph, _ = validate(valid_data_graph, shacl_graph=shapes_graph)
    _, invalid_report_graph, _ = validate(invalid_data_graph, shacl_graph=shapes_graph)
    return valid_report_graph, invalid_report_graph


@then(
    parsers.parse(
        "the valid data validation result should conform to {expected_valid_violation_count:d}"
    )
)
def assert_valid_result_count(
    ns: SimpleNamespace,
    validation_result_graphs: tuple[Graph, Graph],
    expected_valid_violation_count: int,
) -> None:
    valid_report_graph, _ = validation_result_graphs

    result_count = sum(
        1 for _ in valid_report_graph.subjects(ns.RDF.type, ns.SH.ValidationResult)
    )

    assert (
        result_count == expected_valid_violation_count
    ), f"SHACL validation failed:\n{valid_report_graph.serialize()}"


@then(
    parsers.parse(
        "the invalid data validation result should conform to {expected_invalid_violation_count:d}"
    )
)
def assert_invalid_result_count(
    ns: SimpleNamespace,
    validation_result_graphs: tuple[Graph, Graph],
    expected_invalid_violation_count: int,
) -> None:
    _, invalid_report_graph = validation_result_graphs

    result_count = sum(
        1 for _ in invalid_report_graph.subjects(ns.RDF.type, ns.SH.ValidationResult)
    )

    assert (
        result_count == expected_invalid_violation_count
    ), f"SHACL validation failed:\n{invalid_report_graph.serialize()}"
