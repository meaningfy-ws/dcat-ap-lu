#!/usr/bin/env python3
"""
Compares SHACL-defined entities against RDF-used entities. Calculates usage
coverage and exports results. Supports filtering with a lookup table.
"""

import argparse
import json
import csv


def load_list(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return sorted(set(line.strip() for line in f if line.strip()))


def compare_lists(shacl_list, rdf_list):
    used = [item for item in shacl_list if item in rdf_list]
    unused = [item for item in shacl_list if item not in rdf_list]
    total = len(shacl_list)
    coverage = round((len(used) / total * 100), 2) if total > 0 else 0.0
    return {
        "defined": shacl_list,
        "used": used,
        "unused": unused,
        "coverage_percent": coverage,
    }


def print_report(results, label):
    for item in results["unused"]:
        print(f"  ❌ {item}")
    print(f"\n📦 {label} Coverage")
    print(f"Defined in SHACL: {len(results['defined'])}")
    print(f"Used in RDF: {len(results['used'])}")
    print(f"Unused: {len(results['unused'])}")
    print(f"Coverage: {results['coverage_percent']}%")


def export_to_csv(results, output_file, label):
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "value", "status"])
        for item in results["used"]:
            writer.writerow([label, item, "used"])
        for item in results["unused"]:
            writer.writerow([label, item, "unused"])
    print(f"✅ CSV saved to {output_file}")


def export_to_json(results, output_file, label):
    data = {
        label.lower(): {
            "defined": results["defined"],
            "used": results["used"],
            "coverage_percent": results["coverage_percent"],
        }
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"✅ JSON saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Compare SHACL usage against RDF data")
    parser.add_argument(
        "shacl_file", help="File with SHACL-defined entities (one per line)"
    )
    parser.add_argument("rdf_file", help="File with RDF-used entities (one per line)")
    parser.add_argument(
        "--label",
        default="Entity",
        help="Label for the type of entity (e.g., Class, Property)",
    )
    parser.add_argument("--csv", help="Export results to CSV file")
    parser.add_argument("--json", help="Export results to JSON file")
    args = parser.parse_args()

    shacl_list = load_list(args.shacl_file)
    rdf_list = load_list(args.rdf_file)

    results = compare_lists(shacl_list, rdf_list)
    print_report(results, args.label)

    if args.csv:
        export_to_csv(results, args.csv, args.label)
    if args.json:
        export_to_json(results, args.json, args.label)


if __name__ == "__main__":
    main()
