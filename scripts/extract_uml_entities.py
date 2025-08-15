import xml.etree.ElementTree as ET
import csv
import argparse
import os
import re

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Extract entities from an XMI file')
    parser.add_argument('xmi_file', help='Path to the XMI file')
    parser.add_argument('-o', '--output', default='uml_entities.csv',
                      help='Output CSV file (default: uml_entities.csv)')
    args = parser.parse_args()
    
    # Check if the input file exists
    if not os.path.isfile(args.xmi_file):
        print(f"Error: XMI file '{args.xmi_file}' not found")
        return
    
    try:
        # Parse the XML file
        tree = ET.parse(args.xmi_file)
        root = tree.getroot()

        # Define namespaces
        namespaces = {
            'xmi': 'http://www.omg.org/spec/XMI/20131001',
            'uml': 'http://www.omg.org/spec/UML/20131001'
        }

        # List to store all attribute and relationship data
        result_data = []
        
        # Extract attributes
        print("Extracting attributes...")
        for class_elem in root.findall('./xmi:Extension/elements/element', namespaces):
            class_name = class_elem.get('name')
            
            # Skip if not a class or no name
            if class_name is None:
                continue
                
            # Find attributes for this class
            for attr in class_elem.findall('./attributes/attribute', namespaces):
                attr_name = attr.get('name')
                
                # Skip if no attribute name
                if attr_name is None:
                    continue
                
                # Get stereotype
                stereotype_elem = attr.find('./stereotype', namespaces)
                stereotype = 'None'
                if stereotype_elem is not None:
                    stereotype = stereotype_elem.get('stereotype', 'None')
                
                # Get cardinality
                bounds_elem = attr.find('./bounds', namespaces)
                min_cardinality = '0'  # Default
                max_cardinality = '1'  # Default
                
                if bounds_elem is not None:
                    min_cardinality = bounds_elem.get('lower', '0')
                    max_cardinality = bounds_elem.get('upper', '1')
                    if max_cardinality == '*':
                        max_cardinality = 'n'
                
                cardinality = f"{min_cardinality}..{max_cardinality}"
                
                # Add to results
                result_data.append({
                    'parent': class_name,
                    'entity': attr_name,
                    'qualifier': stereotype,
                    'cardinality': cardinality,
                    'type': 'attribute'
                })

        # Extract relationships (connectors)
        print("Extracting relationships...")
        for connector in root.findall('./xmi:Extension/connectors/connector', namespaces):
            # Get source class (parent)
            source = connector.find('./source', namespaces)
            if source is None:
                continue
                
            source_model = source.find('./model', namespaces)
            if source_model is None:
                continue
                
            parent_class = source_model.get('name')
            if parent_class is None:
                continue
            
            # Get target role (relationship name)
            target = connector.find('./target', namespaces)
            if target is None:
                continue
                
            role = target.find('./role', namespaces)
            if role is None:
                continue
                
            relationship_name = role.get('name')
            if relationship_name is None:
                continue
            
            # Get cardinality
            target_type = target.find('./type', namespaces)
            cardinality = "0..1"  # Default
            if target_type is not None:
                multiplicity = target_type.get('multiplicity')
                if multiplicity:
                    if multiplicity == "0..*":
                        cardinality = "0..n"
                    elif multiplicity == "1..*":
                        cardinality = "1..n"
                    else:
                        cardinality = multiplicity.replace("*", "n")
            
            # Get stereotype/qualifier from labels
            qualifier = "None"
            labels = connector.find('./labels', namespaces)
            if labels is not None:
                mb_value = labels.get('mb')
                if mb_value:
                    # Extract text between � characters
                    match = re.search(r'�(\w+)�', mb_value)
                    if match:
                        qualifier = match.group(1)
            
            # Also check properties for stereotype
            if qualifier == "None":
                properties = connector.find('./properties', namespaces)
                if properties is not None:
                    qualifier = properties.get('stereotype', 'None')
            
            # Add to results
            result_data.append({
                'parent': parent_class,
                'entity': relationship_name,
                'qualifier': qualifier,
                'cardinality': cardinality,
                'type': 'relationship'
            })
        
        # Write results to a CSV file
        with open(args.output, 'w', newline='') as csvfile:
            fieldnames = ['parent', 'entity', 'qualifier', 'cardinality', 'type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for data in result_data:
                writer.writerow(data)

        print(f"Extraction complete. Found {len(result_data)} entities ({sum(1 for d in result_data if d['type'] == 'attribute')} attributes, {sum(1 for d in result_data if d['type'] == 'relationship')} relationships). Results saved to {args.output}")
    
    except Exception as e:
        print(f"Error processing the XMI file: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()