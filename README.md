# Excel to PostgreSQL - ATE Spec Importer

Imports the supplied ATE Excel workbook into the existing PostgreSQL table `ate.spec`.

## Fixed values

- `prod_id = 134`
- `test_id = 1201`
- `active = true`

## Excel -> ate.spec

- `Sl. No.` -> `sl_no`
- `Param code` -> `param_code`
- `Main type` -> `main_type_id`
  - Pre Inspection = 1
  - Environmental Inspection = 2
  - Final Inspection = 3
- `Parameter type` -> `param_type` via `ate.param_type.param_type` -> `ate.param_type.id`
- `Parameter description` -> `spec_val`
- `TY clause no` -> `ty_clause_no`
- `Minimum value` -> `min`
- `maximum value` -> `max`
- `Unit` -> `unit` via `ate.units.units` -> `ate.units.id`

The Excel columns `Test Type`, `Test by`, and `Duration in Minutes` are parsed but are not inserted into `ate.spec` because no mapping for them to a database column/FK was supplied. `test_type_id` remains NULL unless an explicit lookup mapping is added.

The importer does not modify or create the database schema.

## Run

```bash
python main.py --file "data/Protocol 1A43 QA 4.0.xlsx"
```

Set the PostgreSQL connection variables if required:

```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME="olf_aug_2026_client_dated_25-12-26"
export DB_SCHEMA=ate
```
