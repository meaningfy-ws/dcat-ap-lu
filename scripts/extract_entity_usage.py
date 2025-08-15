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
    SELECT DISTINCT ?property ?subject ?type WHERE {
      ?subject ?property ?object .
      FILTER(?property != <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>)
      OPTIONAL { ?subject a ?type }
    }
    """
    results = []
    
    # Track combinations we've already seen
    seen_combinations = set()
    
    for row in graph.query(query):
        uri = str(row["property"])
        
        parent = None
        if row["type"]:
            parent = str(row["type"])
            if use_prefixes:
                try:
                    prefix, _, local = graph.compute_qname(parent)
                    parent = f"{prefix}:{local}"
                except Exception:
                    pass
        
        # Format the property URI with prefix if needed
        prop_uri = uri
        if use_prefixes:
            try:
                prefix, _, local = graph.compute_qname(uri)
                prop_uri = f"{prefix}:{local}"
            except Exception:
                pass
        
        # Add the combination if we haven't seen it before
        combination = (prop_uri, parent)
        if combination not in seen_combinations:
            results.append(combination)
            seen_combinations.add(combination)
    
    return sorted(results)

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
    
    # Get all NodeShapes and their targetClasses for reference
    node_shapes = {}
    for shape in graph.subjects(RDF.type, SH.NodeShape):
        for target_class in graph.objects(shape, SH.targetClass):
            node_shapes[str(shape)] = str(target_class)
    
    # Track combinations we've already seen
    seen_combinations = set()
    
    for shape in graph.subjects(RDF.type, SH.PropertyShape):
        path = graph.value(shape, SH.path)
        if path:
            uri = str(path)
            
            # Find parent NodeShape that refers to this PropertyShape
            for node_shape, props in graph.subject_objects(SH.property):
                if props == shape and str(node_shape) in node_shapes:
                    parent = node_shapes[str(node_shape)]
                    if use_prefixes:
                        try:
                            prefix, _, local = graph.compute_qname(parent)
                            parent = f"{prefix}:{local}"
                        except Exception:
                            pass
                    
                    # Format the property URI with prefix if needed
                    prop_uri = uri
                    if use_prefixes:
                        try:
                            prefix, _, local = graph.compute_qname(uri)
                            prop_uri = f"{prefix}:{local}"
                        except Exception:
                            pass
                    
                    # Add the combination if we haven't seen it before
                    combination = (prop_uri, parent)
                    if combination not in seen_combinations:
                        results.append(combination)
                        seen_combinations.add(combination)
    
    # Also include properties without parents
    for shape in graph.subjects(RDF.type, SH.PropertyShape):
        path = graph.value(shape, SH.path)
        if path:
            uri = str(path)
            prop_uri = uri
            if use_prefixes:
                try:
                    prefix, _, local = graph.compute_qname(uri)
                    prop_uri = f"{prefix}:{local}"
                except Exception:
                    pass
            
            # Check if we have this property without a parent
            combination = (prop_uri, None)
            if combination not in seen_combinations:
                # Check if this property has any combination with a parent
                has_parent = any(prop == prop_uri for prop, parent in seen_combinations if parent is not None)
                # Only add properties without parents if they don't have any parent combination
                if not has_parent:
                    results.append(combination)
                    seen_combinations.add(combination)
    
    return sorted(results)

def export_to_csv(classes, properties, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['type', 'name', 'parent'])
        for cls in classes:
            writer.writerow(['class', cls, ''])
        for prop, parent in properties:
            writer.writerow(['property', prop, parent or ''])

def export_to_json(classes, properties, output_file):
    classes_with_structure = []
    for cls in classes:
        classes_with_structure.append({
            "name": cls
        })
    
    props_with_structure = []
    for prop, parent in properties:
        props_with_structure.append({
            "name": prop,
            "parent": parent
        })
        
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'classes': classes_with_structure, 'properties': props_with_structure}, f, indent=2)

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
    for prop, parent in properties:
        if parent:
            print(f"{parent} {prop}")
        else:
            print(f"- {prop}")

    if args.csv:
        export_to_csv(classes, properties, args.csv)
    if args.json:
        export_to_json(classes, properties, args.json)

if __name__ == "__main__":
    main()
