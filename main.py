"""
main.py
-------
Entry point for importing the current ATE specification workbook.
"""

import argparse

import config
from services.importer import run_import


def main():
    parser = argparse.ArgumentParser(
        description="Import ATE Excel specifications into PostgreSQL ate.spec."
    )
    parser.add_argument(
        "--file",
        default=config.DEFAULT_EXCEL_PATH,
        help="Path to the Excel workbook.",
    )
    parser.add_argument(
        "--mapping",
        default=config.MAPPING_FILE_PATH,
        help="Path to column_mapping.json.",
    )
    args = parser.parse_args()

    run_import(excel_path=args.file, mapping_path=args.mapping)


if __name__ == "__main__":
    main()
