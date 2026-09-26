"""
config.py
---------
Database connection and file paths.
"""

import os

DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "olf_aug_2026_client_dated_26-09-26")
DB_SCHEMA = os.environ.get("DB_SCHEMA", "ate")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_EXCEL_PATH = os.path.join(BASE_DIR, "data", "Protocol 1A43 QA 4.0.xlsx")
MAPPING_FILE_PATH = os.path.join(BASE_DIR, "mappings", "column_mapping.json")
LOG_FILE_PATH = os.path.join(BASE_DIR, "logs", "import.log")
