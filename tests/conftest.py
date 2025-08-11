import json
from types import SimpleNamespace
import pytest
from rdflib import Graph, Namespace
from tests import DEFAULT_RDF_FORMAT, TEST_DATA_FOLDER
from tests.unit.shacl import FULL_SHAPES_FILE


@pytest.fixture(scope="session")
def ns():
    with open(f"{TEST_DATA_FOLDER}/context.jsonld") as f:
        context = json.load(f)["@context"]
    return SimpleNamespace(**{k.upper(): Namespace(v) for k, v in context.items()})


@pytest.fixture(scope="session")
def full_shacl_shapes():
    if not FULL_SHAPES_FILE.exists():
        raise FileNotFoundError(f"SHACL shapes file not found: {FULL_SHAPES_FILE}")
    return Graph().parse(FULL_SHAPES_FILE, format=DEFAULT_RDF_FORMAT)
