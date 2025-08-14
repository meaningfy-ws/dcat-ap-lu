import os
import sys
import json
import csv
from pathlib import Path
from rdflib import RDF, Graph
from rdflib.namespace import SH

def guess_format(file_path):
    ext = file_path.suffix.lower()
    return {
        '.ttl': 'turtle',
        '.rdf': 'xml',
        '.nt': 'nt',
        '.n3': 'n3',
        '.jsonld': 'json-ld'
    }.get(ext, 'xml')

def load_graph_from_path(path):
    graph = Graph()
    path = Path(path)

    if path.is_file():
        graph.parse(path, format=guess_format(path))
    elif path.is_dir():
        for file in path.rglob("*"):
            if file.is_file():
                try:
                    graph.parse(file, format=guess_format(file))
                except Exception as e:
                    print(f"⚠️ Failed to parse {file}: {e}")
    else:
        raise ValueError("Invalid path: must be a file or directory")

    return graph

def get_all_properties(graph, use_prefixes=False):
    query = """
    SELECT DISTINCT ?property WHERE {
      ?subject ?property ?object .
    }
    """
    results = []
    for row in graph.query(query):
        uri = str(row["property"])
        if use_prefixes:
            try:
                prefix, _, local = graph.compute_qname(uri)
                results.append(f"{prefix}:{local}")
            except Exception:
                results.append(uri)
        else:
            results.append(uri)
    return sorted(set(results))

def get_all_classes(graph, use_prefixes=False):
    query = """
    SELECT DISTINCT ?class WHERE {
      ?instance a ?class .
    }
    """
    results = []
    for row in graph.query(query):
        uri = str(row["class"])
        if use_prefixes:
            try:
                prefix, _, local = graph.compute_qname(uri)
                results.append(f"{prefix}:{local}")
            except Exception:
                results.append(uri)
        else:
            results.append(uri)
    return sorted(set(results))

def get_shacl_classes(graph, use_prefixes=False):
    results = []
    for shape in graph.subjects(RDF.type, SH.NodeShape):
        for target_class in graph.objects(shape, SH.targetClass):
            uri = str(target_class)
            if use_prefixes:
                try:
                    prefix, _, local = graph.compute_qname(uri)
                    results.append(f"{prefix}:{local}")
                except Exception:
                    results.append(uri)
            else:
                results.append(uri)
    return sorted(set(results))

def get_shacl_properties(graph, use_prefixes=False):
    results = []
    for shape in graph.subjects(RDF.type, SH.PropertyShape):
        path = graph.value(shape, SH.path)
        if path:
            uri = str(path)
            if use_prefixes:
                try:
                    prefix, _, local = graph.compute_qname(uri)
                    results.append(f"{prefix}:{local}")
                except Exception:
                    results.append(uri)
            else:
                results.append(uri)
    return sorted(set(results))

def export_to_csv(classes, properties, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'value'])
        for cls in classes:
            writer.writerow(['Class', cls])
        for prop in properties:
            writer.writerow(['Property', prop])
    # print(f"✅ CSV saved to {output_file}")

def export_to_json(classes, properties, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'classes': classes, 'properties': properties}, f, indent=2)
    # print(f"✅ JSON saved to {output_file}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Extract RDF classes and properties")
    parser.add_argument("input", help="Path to RDF file or folder")
    parser.add_argument("--prefixed", action="store_true", help="Use prefixed URIs")
    parser.add_argument("--csv", help="Export results to CSV file")
    parser.add_argument("--json", help="Export results to JSON file")
    parser.add_argument("--shacl", action="store_true", help="Extract SHACL shapes")
    args = parser.parse_args()

    graph = load_graph_from_path(args.input)

    if args.shacl:
        classes = get_shacl_classes(graph, use_prefixes=args.prefixed)
        properties = get_shacl_properties(graph, use_prefixes=args.prefixed)
    else:
        classes = get_all_classes(graph, use_prefixes=args.prefixed)
        properties = get_all_properties(graph, use_prefixes=args.prefixed)

    for cls in classes:
        print(cls)
    for prop in properties:
        print(prop)

    if args.csv:
        export_to_csv(classes, properties, args.csv)
    if args.json:
        export_to_json(classes, properties, args.json)

if __name__ == "__main__":
    main()
