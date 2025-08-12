from pyshacl import validate
from rdflib import Graph
from tests.unit.shacl import TEST_DATA_FOLDER, DEFAULT_RDF_FORMAT

from pytest_bdd import given, scenarios, then, when, parsers


scenarios("../../features/shacl/rdf_fragments.feature")


@given(
    parsers.parse("the valid RDF data fragment of {data_shape}"),
    target_fixture="valid_data_graph",
)
def get_valid_data_graph(data_shape):
    return Graph().parse(
        TEST_DATA_FOLDER / data_shape / f"{data_shape}_valid.{DEFAULT_RDF_FORMAT}",
        format=DEFAULT_RDF_FORMAT,
    )


@given(
    parsers.parse("the invalid RDF data fragment of {data_shape}"),
    target_fixture="invalid_data_graph",
)
def get_invalid_data_graph(data_shape):
    return Graph().parse(
        TEST_DATA_FOLDER / data_shape / f"{data_shape}_invalid.{DEFAULT_RDF_FORMAT}",
        format=DEFAULT_RDF_FORMAT,
    )


@given("the full shapes graph", target_fixture="shapes_graph")
def get_shapes_graph(full_shacl_shapes):
    return full_shacl_shapes


@when(
    "I validate the valid data against the shapes", target_fixture="valid_result_graph"
)
def get_valid_result_graph(valid_data_graph, shapes_graph):
    conforms, report_graph, _ = validate(valid_data_graph, shacl_graph=shapes_graph)
    return conforms, report_graph


@when(
    "I validate the invalid data against the shapes",
    target_fixture="invalid_result_graph",
)
def get_invalid_result_graph(invalid_data_graph, shapes_graph):
    conforms, report_graph, _ = validate(invalid_data_graph, shacl_graph=shapes_graph)
    return conforms, report_graph


@then(parsers.parse("the valid result should conform to {expected_valid_result}"))
def assert_valid_result(valid_result_graph, expected_valid_result):
    valid_result, report_graph = valid_result_graph
    expected_result = expected_valid_result.lower() == "true"
    assert (
        valid_result == expected_result
    ), f"SHACL validation failed:\n{report_graph.serialize()}"


@then(parsers.parse("the invalid result should conform to {expected_invalid_result}"))
def assert_invalid_result(invalid_result_graph, expected_invalid_result):
    invalid_result, report_graph = invalid_result_graph
    expected_result = expected_invalid_result.lower() == "true"
    assert (
        invalid_result == expected_result
    ), f"SHACL validation failed:\n{report_graph.serialize()}"


@then(parsers.parse("the valid result count should be {expected_valid_count:d}"))
def assert_valid_result_count(ns, valid_result_graph, expected_valid_count):
    _, report_graph = valid_result_graph

    result_count = sum(
        1 for _ in report_graph.subjects(ns.RDF.type, ns.SH.ValidationResult)
    )

    assert (
        result_count == expected_valid_count
    ), f"SHACL validation failed:\n{report_graph.serialize()}"


@then(parsers.parse("the invalid result count should be {expected_invalid_count:d}"))
def assert_invalid_result_count(ns, invalid_result_graph, expected_invalid_count):
    _, report_graph = invalid_result_graph

    result_count = sum(
        1 for _ in report_graph.subjects(ns.RDF.type, ns.SH.ValidationResult)
    )

    assert (
        result_count == expected_invalid_count
    ), f"SHACL validation failed:\n{report_graph.serialize()}"
