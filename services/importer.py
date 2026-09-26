"""
services/importer.py
---------------------
Imports the current ATE specification workbook directly into `ate.spec`.

Fixed values supplied for this project:
  prod_id = 134
  test_id = 1201

Main Type mapping supplied for this project:
  Pre Inspection          -> 1
  Environmental Inspection -> 2
  Final Inspection        -> 3

Parameter Type and Unit are foreign keys. Their IDs are resolved from
ate.param_type and ate.units using configurable text columns.
"""

import json

from database import crud
from database.connection import get_session
from excel.parser import parse_parameter_rows
from excel.reader import iter_product_sheets
from utils.logger import get_logger

logger = get_logger(__name__)

MAIN_TYPE_IDS = {
    "pre inspection": 1,
    "environmental inspection": 2,
    "final inspection": 3,
}


def load_mapping(mapping_path: str) -> dict:
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _main_type_id(value: str) -> int:
    key = " ".join(str(value).split()).strip().lower()
    try:
        return MAIN_TYPE_IDS[key]
    except KeyError:
        raise ValueError(
            f"Unknown Main type '{value}'. Expected one of: "
            + ", ".join(MAIN_TYPE_IDS.keys())
        )


def run_import(excel_path: str, mapping_path: str) -> None:
    mapping = load_mapping(mapping_path)

    header_row = mapping["header_row"]
    data_start_row = mapping["data_start_row"]
    columns_map = mapping["columns"]

    prod_id = int(mapping.get("fixed_prod_id", 134))
    test_id = int(mapping.get("fixed_test_id", 1201))

    param_type_columns = mapping.get(
        "param_type_lookup_columns",
        ["param_type", "name", "description", "type"],
    )
    unit_columns = mapping.get(
        "unit_lookup_columns",
        ["unit", "unit_name", "name", "description", "symbol", "code"],
    )

    total_sheets = 0
    total_specs = 0

    for sheet_name, ws in iter_product_sheets(excel_path):
        total_sheets += 1
        session = get_session()

        try:
            rows = parse_parameter_rows(
                ws,
                header_row=header_row,
                data_start_row=data_start_row,
                columns_map=columns_map,
            )
            logger.info("Sheet '%s': %d parameter rows found", sheet_name, len(rows))

            for row in rows:
                if not row.main_type:
                    raise ValueError(
                        f"Sheet '{sheet_name}', Sl. No. {row.sl_no}: Main type is blank."
                    )

                if not row.param_type:
                    raise ValueError(
                        f"Sheet '{sheet_name}', Sl. No. {row.sl_no}: Parameter type is blank."
                    )

                main_type_id = _main_type_id(row.main_type)

                param_type_id = crud.resolve_lookup_id(
                    session,
                    "param_type",
                    row.param_type,
                    param_type_columns,
                )

                # Observation rules:
                # - Unit present: resolve unit FK, obs_type_id = 2, obs_value = NULL
                # - Unit blank/NULL/whitespace: unit = NULL, obs_type_id = 4, obs_value = "ok_notok"
                if row.unit_raw is not None and str(row.unit_raw).strip() != "":
                    unit_id = crud.resolve_lookup_id(
                        session,
                        "units",
                        row.unit_raw,
                        unit_columns,
                    )
                    obs_type_id = 2
                    obs_value = None
                else:
                    unit_id = None
                    obs_type_id = 4
                    obs_value = "ok_notok"

                crud.create_spec(
                    session,
                    prod_id=prod_id,
                    test_id=test_id,
                    spec_val=row.spec_val,
                    param_code=row.param_code,
                    param_type_id=param_type_id,
                    main_type_id=main_type_id,
                    ty_clause_no=row.ty_clause_no,
                    min_val=row.min_raw,
                    max_val=row.max_raw,
                    unit_id=unit_id,
                    obs_type_id=obs_type_id,
                    obs_value=obs_value,
                    sl_no=row.sl_no,
                    active=True,
                )
                total_specs += 1

            session.commit()
            logger.info("Sheet '%s' committed successfully.", sheet_name)

        except Exception:
            session.rollback()
            logger.exception("Sheet '%s' failed, rolled back.", sheet_name)
            raise
        finally:
            session.close()

    logger.info(
        "Import finished: %d sheet(s) processed, %d spec row(s) inserted.",
        total_sheets,
        total_specs,
    )
