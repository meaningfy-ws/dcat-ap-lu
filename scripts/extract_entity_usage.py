import os
import sys
import json
import csv
from pathlib import Path
from rdflib import RDF, Graph
from rdflib.namespace import SH

# TODO: Extend support with an option to take a prefix normalization table from a configuration file
# This would allow for more flexible prefix normalization across different datasets
def normalize_prefix(uri):
    """Normalize common prefixes for better matching with lookup tables"""
    # Replace dcterms: with dct:
    if uri.startswith('dcterms:'):
        return 'dct:' + uri[len('dcterms:'):]
    # Replace ns1: with dpv: 
    elif uri.startswith('ns1:'):
        return 'dpv:' + uri[len('ns1:'):]
    # Add more prefix normalizations as needed
    return uri

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

def load_filter_entities(filter_file, filter_column, filter_value, parent_column='parent'):
    """
    Load entities from a CSV filter file that match the specified column and value.
    If parent_column is provided, also track parent-property relationships.
    """
    filtered_entities = set()
    property_parents = {}
    
    with open(filter_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # TODO: make this join column also a parameter
            # Skip rows that don't match filter criteria or don't have entity
            if not row.get(filter_column) or not row.get('entity') or row.get(filter_column).strip() != filter_value:
                continue
                
            entity = row['entity'].strip()
            filtered_entities.add(entity)
            
            # If parent column is specified and has a value, record parent-property relationship
            if parent_column and row.get(parent_column) and row[parent_column].strip():
                parent = row[parent_column].strip()
                if entity not in property_parents:
                    property_parents[entity] = set()
                property_parents[entity].add(parent)
    
    return filtered_entities, property_parents

def get_all_properties(graph, use_prefixes=False, filter_entities=None, property_parents=None):
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
                    # Normalize parent prefix
                    parent = normalize_prefix(parent)
                except Exception:
                    pass
        
        # Format the property URI with prefix if needed
        prop_uri = uri
        if use_prefixes:
            try:
                prefix, _, local = graph.compute_qname(uri)
                prop_uri = f"{prefix}:{local}"
                # Normalize property prefix
                prop_uri = normalize_prefix(prop_uri)
            except Exception:
                pass
        
        # Filter entities based on the property name
        if filter_entities is not None and prop_uri not in filter_entities:
            continue
            
        # Filter property-parent combinations if property_parents is provided
        if property_parents is not None and prop_uri in property_parents:
            # Only include this combination if parent matches expected parents
            if parent not in property_parents[prop_uri]:
                continue
            
        # Add the combination if we haven't seen it before
        combination = (prop_uri, parent)
        if combination not in seen_combinations:
            results.append(combination)
            seen_combinations.add(combination)
    
    return sorted(results)

def get_all_classes(graph, use_prefixes=False, filter_entities=None):
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
                class_uri = f"{prefix}:{local}"
                # Normalize class prefix
                class_uri = normalize_prefix(class_uri)
            except Exception:
                class_uri = uri
        else:
            class_uri = uri
            
        # If filter is active, skip non-matching entities
        if filter_entities is not None and class_uri not in filter_entities:
            continue
            
        results.append(class_uri)
    return sorted(set(results))

def get_shacl_classes(graph, use_prefixes=False, filter_entities=None):
    results = []
    for shape in graph.subjects(RDF.type, SH.NodeShape):
        for target_class in graph.objects(shape, SH.targetClass):
            uri = str(target_class)
            if use_prefixes:
                try:
                    prefix, _, local = graph.compute_qname(uri)
                    class_uri = f"{prefix}:{local}"
                    # Normalize class prefix
                    class_uri = normalize_prefix(class_uri)
                except Exception:
                    class_uri = uri
            else:
                class_uri = uri
                
            # If filter is active, skip non-matching entities
            if filter_entities is not None and class_uri not in filter_entities:
                continue
                
            results.append(class_uri)
    return sorted(set(results))

def get_shacl_properties(graph, use_prefixes=False, filter_entities=None, property_parents=None):
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
            
            # Format the property URI with prefix if needed
            prop_uri = uri
            if use_prefixes:
                try:
                    prefix, _, local = graph.compute_qname(uri)
                    prop_uri = f"{prefix}:{local}"
                    # Normalize property prefix
                    prop_uri = normalize_prefix(prop_uri)
                except Exception:
                    prop_uri = uri
                    
            # If filter is active, skip non-matching entities
            if filter_entities is not None and prop_uri not in filter_entities:
                continue
            
            # Find parent NodeShape that refers to this PropertyShape
            for node_shape, props in graph.subject_objects(SH.property):
                if props == shape and str(node_shape) in node_shapes:
                    parent = node_shapes[str(node_shape)]
                    if use_prefixes:
                        try:
                            prefix, _, local = graph.compute_qname(parent)
                            parent = f"{prefix}:{local}"
                            # Normalize parent prefix
                            parent = normalize_prefix(parent)
                        except Exception:
                            pass
                    
                    # Filter property-parent combinations if property_parents is provided
                    if property_parents is not None and prop_uri in property_parents:
                        # Only include this combination if parent matches expected parents
                        if parent not in property_parents[prop_uri]:
                            continue
                    
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
                    # Normalize property prefix
                    prop_uri = normalize_prefix(prop_uri)
                except Exception:
                    pass
                    
            # If filter is active, skip non-matching entities
            if filter_entities is not None and prop_uri not in filter_entities:
                continue
                
            # If property_parents is specified and this property has expected parents,
            # don't include it without a parent
            if property_parents is not None and prop_uri in property_parents:
                continue
            
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
    parser.add_argument("--filter-csv", help="Path to CSV file with entities to filter by")
    parser.add_argument("--filter-column", help="Name of the column to filter by")
    parser.add_argument("--filter-value", help="Value in the filter column to match")
    parser.add_argument("--parent-column", default="parent", help="Name of the column containing parent class information (default: parent)")
    args = parser.parse_args()

    # Load filter entities if specified
    filter_entities = None
    property_parents = None
    if args.filter_csv:
        if not args.filter_column or not args.filter_value:
            print("Error: When using --filter-csv, both --filter-column and --filter-value must be specified")
            sys.exit(1)
            
        filter_entities, property_parents = load_filter_entities(
            args.filter_csv, 
            filter_column=args.filter_column, 
            filter_value=args.filter_value,
            parent_column=args.parent_column
        )
        
        filter_msg = f"Filtering results to {len(filter_entities)} entities where {args.filter_column}={args.filter_value}"
        if args.parent_column:
            filter_msg += f" with parent matching column '{args.parent_column}'"
        filter_msg += f" from {args.filter_csv}"
        # print(filter_msg)

    graph = load_graph_from_path(args.input)

    if args.shacl:
        classes = get_shacl_classes(graph, use_prefixes=args.prefixed, filter_entities=filter_entities)
        properties = get_shacl_properties(graph, use_prefixes=args.prefixed, 
                                         filter_entities=filter_entities, 
                                         property_parents=property_parents)
    else:
        classes = get_all_classes(graph, use_prefixes=args.prefixed, filter_entities=filter_entities)
        properties = get_all_properties(graph, use_prefixes=args.prefixed, 
                                       filter_entities=filter_entities,
                                       property_parents=property_parents)

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