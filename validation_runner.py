import argparse
from pyshacl import validate
from rdflib import Graph
import glob
import os


def find_test_file(search_str, test_type="valid"):
    """Search for a test file matching the pattern in tests/test_data"""
    pattern = f"tests/test_data/**/*{search_str}*_{test_type}.ttl"
    matches = glob.glob(pattern, recursive=True)
    if not matches:
        raise FileNotFoundError(
            f"No {test_type} test file found matching '{search_str}'"
        )
    return matches[0]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Validate RDF data against SHACL shapes."
    )

    # Create mutually exclusive group for -d and -f
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-d",
        "--data",
        type=str,
        help="Path to the RDF data file to validate",
    )
    input_group.add_argument(
        "-f",
        "--find",
        type=str,
        help="Search string to find test file under tests/test_data",
    )

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["valid", "invalid"],
        default="valid",
        help="Type of test file to find (valid or invalid)",
    )

    parser.add_argument(
        "-s",
        "--shapes",
        type=str,
        default="implementation/dcat_ap_lu/shacl_shapes/dcat_ap_lu_CM_shapes.ttl",
        help="Path to the SHACL shapes file",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Determine input file path
    if args.find:
        try:
            input_path = find_test_file(args.find, args.type)
            print(f"Using test file: {input_path}")
        except FileNotFoundError as e:
            print(e)
            return
    else:
        input_path = args.data

    input_data = Graph().parse(input_path)
    shacl_data = Graph().parse(args.shapes)
    _, _, text = validate(input_data, shacl_graph=shacl_data)
    print(text)


if __name__ == "__main__":
    main()
