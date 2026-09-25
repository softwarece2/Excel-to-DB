"""
database/crud.py
-----------------
Data-access helpers for the current ATE spec import.

Parameter-type and unit IDs are resolved from their lookup tables rather than
hard-coded. The lookup text column is configurable in column_mapping.json.
"""

from typing import Optional

from sqlalchemy import MetaData, String, Table, func, select

from database.models import Spec
import config


def _reflect_lookup_table(session, table_name: str) -> Table:
    metadata = MetaData()
    return Table(table_name, metadata, schema=config.DB_SCHEMA, autoload_with=session.bind)


def resolve_lookup_id(
    session,
    table_name: str,
    value,
    preferred_columns=None,
) -> Optional[int]:
    """
    Resolve a lookup-table ID from the Excel text.

    If value is blank, NULL is returned. Otherwise the configured/preferred
    text column is searched case-insensitively. A numeric value is accepted
    directly only if it exists as the lookup table's id.
    """
    if value is None or str(value).strip() == "":
        return None

    table = _reflect_lookup_table(session, table_name)
    text = str(value).strip()

    # Allow numeric Excel values to already represent an FK id.
    try:
        numeric_id = int(float(text))
        if str(numeric_id) == text or text.replace(".0", "") == str(numeric_id):
            hit = session.execute(
                select(table.c.id).where(table.c.id == numeric_id)
            ).scalar_one_or_none()
            if hit is not None:
                return int(hit)
    except (TypeError, ValueError):
        pass

    preferred_columns = preferred_columns or []
    candidates = [
        c for c in preferred_columns
        if c in table.c and c != "id"
    ]

    # If none of the configured names exists, fall back to textual columns.
    if not candidates:
        candidates = [
            c.name
            for c in table.columns
            if c.name != "id"
            and getattr(c.type, "python_type", None) is str
        ]

    for column_name in candidates:
        column = table.c[column_name]
        hit = session.execute(
            select(table.c.id).where(
                func.lower(func.trim(column.cast(String))) == text.lower()
            )
        ).scalar_one_or_none()

        if hit is not None:
            return int(hit)

    available = ", ".join(c.name for c in table.columns)
    raise ValueError(
        f"Could not resolve '{text}' in ate.{table_name}. "
        f"Available columns: {available}"
    )


def create_spec(
    session,
    *,
    prod_id: int,
    test_id: int,
    spec_val: Optional[str],
    param_code: Optional[str],
    param_type_id: Optional[int],
    main_type_id: Optional[int],
    ty_clause_no: Optional[str],
    min_val=None,
    max_val=None,
    unit_id: Optional[int] = None,
    obs_type_id: Optional[int] = None,
    obs_value: Optional[str] = None,
    sl_no: Optional[int] = None,
    active: bool = True,
) -> Spec:
    """Create one row in ate.spec using the current Excel-to-DB mapping."""
    spec = Spec(
        prod_id=prod_id,
        test_id=test_id,
        spec_val=spec_val,
        param_code=param_code,
        param_type=param_type_id,
        main_type_id=main_type_id,
        ty_clause_no=ty_clause_no,
        min=min_val,
        max=max_val,
        unit=unit_id,
        obs_type_id=obs_type_id,
        obs_value=obs_value,
        sl_no=sl_no,
        active=active,
    )
    session.add(spec)
    return spec
