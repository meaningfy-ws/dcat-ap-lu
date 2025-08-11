import pathlib

PROJECT_FOLDER = pathlib.Path(__file__).parent.parent
IMPLEMENTATION_FOLDER = PROJECT_FOLDER / "implementation" / "dcat_ap_lu"
TEST_DATA_FOLDER = pathlib.Path(__file__).parent / "test_data"
DEFAULT_RDF_FORMAT = "ttl"
