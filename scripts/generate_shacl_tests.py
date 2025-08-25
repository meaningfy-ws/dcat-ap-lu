#!/usr/bin/env python3
"""
Generate valid and invalid test cases from SHACL shapes (experimental)

This script analyzes SHACL shapes and generates corresponding test cases that
can be used with any test framework that can take the invalid and valid pairs as
fixtures or examples. Output is currently a list of Gherkin scenario outline
examples.

EACH TEST CASE MAY NOT VALIDATE AS EXPECTED SO MANUAL CURATION IS NEEDED
"""

import argparse
import logging
from pathlib import Path
from typing import Dict, List, Tuple
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, SH, XSD

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common namespaces used in your shapes
DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCT = Namespace("http://purl.org/dc/terms/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
ADMS = Namespace("http://www.w3.org/ns/adms#")
DCATAP = Namespace("http://data.europa.eu/r5r/")


class SHACLTestGenerator:
    def __init__(self, shapes_file: str):
        self.shapes_graph = Graph()
        self.shapes_graph.parse(shapes_file, format="turtle")
        self.node_shapes = self._get_node_shapes()
        self.property_shapes = self._get_property_shapes()

    def _get_node_shapes(self) -> List[URIRef]:
        """Get all node shapes from the shapes graph."""
        return [s for s in self.shapes_graph.subjects(RDF.type, SH.NodeShape)]

    def _get_property_shapes(self) -> List[URIRef]:
        """Get all property shapes from the shapes graph."""
        return [s for s in self.shapes_graph.subjects(RDF.type, SH.PropertyShape)]

    def _get_shape_name(self, shape: URIRef) -> str:
        """Generate a standardized name for the shape."""
        # Try to get the parent shape and property path for property shapes
        parent_shape = None
        for s, p, o in self.shapes_graph.triples((None, SH.property, shape)):
            parent_shape = s
            break

        if parent_shape:
            parent_name = self._get_shape_name(parent_shape)
            path = self.shapes_graph.value(shape, SH.path)
            if path:
                # Convert URI to prefixed form
                path_str = str(path)
                if "#" in path_str:
                    prefix, local = path_str.split("#")[-2:]
                    prefix = prefix.split("/")[-1]
                    return f"{parent_name}-{prefix}-{local}"
                return f"{parent_name}-{path_str.split('/')[-1]}"

        # For node shapes or if no parent found
        label = self.shapes_graph.value(shape, RDFS.label)
        if label:
            return str(label).replace(" ", "-")

        # Fall back to URI local name
        uri = str(shape)
        return uri.split("#")[-1] if "#" in uri else uri.split("/")[-1]

    def _get_shape_constraints(self, shape: URIRef) -> Dict:
        """Extract all constraints for a given shape."""
        constraints = {
            "targetClass": None,
            "properties": [],
            "minCount": self.shapes_graph.value(shape, SH.minCount),
            "maxCount": self.shapes_graph.value(shape, SH.maxCount),
            "datatype": self.shapes_graph.value(shape, SH.datatype),
            "class": self.shapes_graph.value(shape, SH["class"]),
            "pattern": self.shapes_graph.value(shape, SH.pattern),
            "nodeKind": self.shapes_graph.value(shape, SH.nodeKind),
            "path": self.shapes_graph.value(shape, SH.path),
        }

        # Get target class for node shapes
        target_class = self.shapes_graph.value(shape, SH.targetClass)
        if target_class:
            constraints["targetClass"] = target_class

        # Get nested property shapes for node shapes
        for prop in self.shapes_graph.objects(shape, SH.property):
            prop_constraints = self._get_shape_constraints(prop)
            if prop_constraints["path"]:
                constraints["properties"].append(prop_constraints)

        return constraints

    def generate_valid_instance(self, shape: URIRef, constraints: Dict) -> Graph:
        """Generate a valid instance for the given shape."""
        g = Graph()
        instance = BNode()

        # For node shapes
        if constraints["targetClass"]:
            g.add((instance, RDF.type, constraints["targetClass"]))

        # For property shapes
        if constraints["path"]:
            parent = BNode()
            if constraints["datatype"]:
                value = self._generate_valid_value(constraints["datatype"])
                g.add((parent, constraints["path"], value))
            elif constraints["class"]:
                obj = BNode()
                g.add((obj, RDF.type, constraints["class"]))
                g.add((parent, constraints["path"], obj))
            else:
                g.add((parent, constraints["path"], Literal("Valid value")))
            return g, parent

        # Handle nested properties
        for prop in constraints["properties"]:
            path = prop["path"]
            min_count = int(prop["minCount"].value) if prop["minCount"] else 1

            for _ in range(min_count):
                if prop["datatype"]:
                    value = self._generate_valid_value(prop["datatype"])
                    g.add((instance, path, value))
                elif prop["class"]:
                    obj = BNode()
                    g.add((obj, RDF.type, prop["class"]))
                    g.add((instance, path, obj))
                else:
                    g.add((instance, path, Literal(f"Valid value for {path}")))

        return g, instance

    def _generate_valid_value(self, datatype: URIRef) -> Literal:
        """Generate a valid value for the given datatype."""
        if datatype == XSD.string:
            return Literal("Valid string", datatype=XSD.string)
        elif datatype == XSD.dateTime:
            return Literal("2024-03-20T12:00:00", datatype=XSD.dateTime)
        elif datatype == XSD.date:
            return Literal("2024-03-20", datatype=XSD.date)
        elif datatype == XSD.integer:
            return Literal("42", datatype=XSD.integer)
        elif datatype == XSD.decimal:
            return Literal("42.0", datatype=XSD.decimal)
        elif datatype == XSD.boolean:
            return Literal("true", datatype=XSD.boolean)
        return Literal("Default value", datatype=datatype)

    def _get_shape_name(self, shape: URIRef) -> str:
        """Get the standardized name for a shape from the SHACL file."""
        # First try to get the shape name from the URI
        uri = str(shape)
        if "#" in uri:
            # Handle URIs like http://data.europa.eu/a4g/data-shape#dcat-Distribution-dcat-accessURL
            return uri.split("#")[-1]

        # Fallback to label if URI doesn't follow the pattern
        label = self.shapes_graph.value(shape, RDFS.label)
        if label:
            return str(label)

        # Last resort: use the last part of the URI
        return uri.split("/")[-1]

    def generate_invalid_instances(
        self, shape: URIRef, constraints: Dict
    ) -> List[Tuple[str, Graph]]:
        """Generate invalid instances with descriptions for each violation."""
        invalid_cases = []

        # For node shapes
        if constraints["targetClass"]:
            # Missing type
            g = Graph()
            instance = BNode()
            g.add((instance, RDF.type, BNode()))  # Wrong type
            invalid_cases.append(("Missing required type", g))

        # For property shapes
        if constraints["path"]:
            parent_class = None
            # Find the parent class
            for s in self.node_shapes:
                for prop in self.shapes_graph.objects(s, SH.property):
                    if prop == shape:
                        parent_class = self.shapes_graph.value(s, SH.targetClass)
                        break
                if parent_class:
                    break

            # Wrong datatype
            if constraints["datatype"]:
                g = Graph()
                parent = BNode()
                if parent_class:
                    g.add((parent, RDF.type, parent_class))
                wrong_value = Literal(
                    "wrong type",
                    datatype=XSD.string
                    if constraints["datatype"] != XSD.string
                    else XSD.integer,
                )
                g.add((parent, constraints["path"], wrong_value))
                invalid_cases.append(
                    (
                        f"Wrong datatype: using {wrong_value.datatype} instead of {constraints['datatype']}",
                        g,
                    )
                )

            # Wrong class
            if constraints["class"]:
                g = Graph()
                parent = BNode()
                if parent_class:
                    g.add((parent, RDF.type, parent_class))
                wrong_obj = BNode()
                g.add((wrong_obj, RDF.type, DCAT.Dataset))  # Wrong class
                g.add((parent, constraints["path"], wrong_obj))
                invalid_cases.append(
                    (
                        f"Wrong class: using dcat:Dataset instead of {constraints['class']}",
                        g,
                    )
                )

            # Cardinality violations
            if constraints["minCount"]:
                g = Graph()
                parent = BNode()
                if parent_class:
                    g.add((parent, RDF.type, parent_class))
                # Don't add the property at all
                invalid_cases.append(
                    (
                        f"Missing required property with minCount={constraints['minCount']}",
                        g,
                    )
                )

            if constraints["maxCount"]:
                g = Graph()
                parent = BNode()
                if parent_class:
                    g.add((parent, RDF.type, parent_class))
                max_count = int(constraints["maxCount"].value)
                for i in range(max_count + 1):
                    g.add((parent, constraints["path"], Literal(f"Value {i}")))
                invalid_cases.append(
                    (f"Exceeding maxCount={max_count} with {max_count + 1} values", g)
                )

        return invalid_cases

    def generate_test_cases(
        self, output_dir: str = "tests/test_data/shacl"
    ) -> List[Dict]:
        """Generate test cases and return Gherkin examples."""
        output_path = Path(output_dir)
        examples = []

        # Process both node and property shapes
        all_shapes = self.node_shapes + self.property_shapes

        for shape in all_shapes:
            shape_name = self._get_shape_name(shape)
            logger.info(f"Generating test cases for shape: {shape_name}")

            # Create shape directory
            shape_dir = output_path / shape_name
            shape_dir.mkdir(parents=True, exist_ok=True)

            constraints = self._get_shape_constraints(shape)

            # Generate valid instance
            valid_graph, _ = self.generate_valid_instance(shape, constraints)
            valid_file = shape_dir / f"{shape_name}_valid.ttl"

            # Add prefixes to the valid graph
            self._add_prefixes(valid_graph)
            valid_graph.serialize(valid_file, format="turtle")

            # Generate invalid instances
            invalid_cases = self.generate_invalid_instances(shape, constraints)

            # Combine all violations into one file with comments
            invalid_ttl = "# Combined invalid cases for shape: " + shape_name + "\n\n"

            for desc, g in invalid_cases:
                invalid_ttl += f"### Invalid case: {desc}\n"
                self._add_prefixes(g)
                invalid_ttl += g.serialize(format="turtle") + "\n\n"

            invalid_file = shape_dir / f"{shape_name}_invalid.ttl"
            with open(invalid_file, "w") as f:
                f.write(invalid_ttl)

            example = {
                "test_case": shape_name,
                "expected_valid_violation_count": 0,
                "expected_invalid_violation_count": len(invalid_cases),
            }
            examples.append(example)

        return examples

    def _add_prefixes(self, graph: Graph):
        """Add common prefixes to a graph."""
        graph.bind("dcat", DCAT)
        graph.bind("dct", DCT)
        graph.bind("foaf", FOAF)
        graph.bind("skos", SKOS)
        graph.bind("adms", ADMS)
        graph.bind("dcatap", DCATAP)
        graph.bind("xsd", XSD)
        graph.bind("rdf", RDF)


def main():
    parser = argparse.ArgumentParser(description="Generate SHACL test cases")
    parser.add_argument(
        "--shapes",
        type=str,
        default="implementation/dcat_ap_lu/shacl_shapes/dcat_ap_lu_CM_shapes.ttl",
        help="Path to SHACL shapes file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="tests/test_data/shacl",
        help="Output directory for generated test cases",
    )

    args = parser.parse_args()

    generator = SHACLTestGenerator(args.shapes)
    examples = generator.generate_test_cases(args.output)

    # Print Gherkin examples
    print("\nGherkin Examples:")
    print(
        "| test_case | expected_valid_violation_count | expected_invalid_violation_count |"
    )
    print(
        "|-----------|------------------------------|----------------------------------|"
    )
    for example in examples:
        print(
            f"| {example['test_case']} | {example['expected_valid_violation_count']} | {example['expected_invalid_violation_count']} |"
        )


if __name__ == "__main__":
    main()
