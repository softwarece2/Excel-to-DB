# Excel to PostgreSQL - ATE Spec Importer

Imports the supplied ATE Excel workbook into the existing PostgreSQL table `ate.spec`.

## Fixed Values

The following values are configured for the current product:

- `prod_id = 134`
- `fixed_test_id = 1201` (fallback when the Excel workbook does not contain a `Test ID` column)
- `active = true`

> **Note:** When importing specifications for a new product, update the `prod_id` and `test_id`/`fixed_test_id` in both `services/importer.py` and `mappings/column_mapping.json`. If the workbook contains a `Test ID` column, the Excel value is used per row.

## Excel → `ate.spec`

The Excel columns are mapped to the PostgreSQL `ate.spec` table as follows:

- `Test ID` → `test_id` (when present; the value is used for each row)
- `Sl. No.` → `sl_no`
- `Param code` → `param_code`
- `Main type` → `main_type_id`
  - `Pre Inspection` = `1`
  - `Environmental Inspection` = `2`
  - `Final Inspection` = `3`
- `Parameter type` → `param_type` via `ate.param_type.param_type` → `ate.param_type.id`
- `Parameter description` → `spec_val`
- `TY clause no` → `ty_clause_no`
- `Minimum value` → `min`
- `maximum value` → `max`
- `Unit` → `unit` via `ate.units.units` → `ate.units.id`

The Excel columns `Test Type`, `Test by`, and `Duration in Minutes` are parsed but are not inserted into `ate.spec` because no mapping for them to a database column/FK was supplied. `test_type_id` remains `NULL` unless an explicit lookup mapping is added.

The importer does not modify or create the database schema.

## Adding a New Product

Whenever importing specifications for a new product:

1. Add the new product's Excel workbook to the `data/` folder.

2. Run the importer by providing the Excel file path:

```bash
python main.py --file "data/New Product QA 4.0.xlsx"
```

3. Update the **Product ID (`prod_id`)** and **Test ID (`test_id`)** in both of the following files:

```text
services/importer.py
mappings/column_mapping.json
```

For the current product, the configured values are:

```text
prod_id = 134
test_id = 1201
```

Replace these with the appropriate `prod_id` and `test_id` for the new product/test.

4. Make sure the new Excel workbook contains the required columns and follows the supported ATE specification format.

5. Verify the following Excel data before importing:

- `Sl. No.`
- `Param code`
- `Main type`
- `Parameter type`
- `Parameter description`
- `TY clause no`
- `Minimum value`
- `maximum value`
- `Unit`

6. Make sure the `Main type` values match the configured values:

```text
Pre Inspection
Environmental Inspection
Final Inspection
```

7. Make sure the corresponding product and test records already exist in the PostgreSQL database.

8. Run the importer and verify that the records have been inserted into `ate.spec` with the correct `prod_id` and `test_id`.

> **Important:** For every new product, update `prod_id` and `test_id` in **both** `services/importer.py` and `mappings/column_mapping.json`.

## Run

For the current Protocol 1A43 workbook:

```bash
python main.py --file "data/Protocol 1A43 QA 4.0.xlsx"
```

For another workbook, specify its filename:

```bash
python main.py --file "data/1G 46 QA 4.0.xlsx"
```

## PostgreSQL Configuration

Set the PostgreSQL connection variables if required:

```bash
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME="olf_aug_2026_client_dated_25-12-26"
export DB_SCHEMA=ate
```

## Database Requirements

The importer expects the following database objects to already exist:

- `ate.spec`
- `ate.param_type`
- `ate.units`
- `ate.main_type`
- The corresponding product record for `prod_id`
- The corresponding test record for `test_id`

The importer does **not** create, alter, or modify the PostgreSQL database schema.