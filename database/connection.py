"""
database/connection.py
-----------------------
Creates the SQLAlchemy engine and a session factory used across the app.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.DATABASE_URL, future=True)

# One Session class, instantiated per unit-of-work (see services/importer.py)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session():
    """Return a new SQLAlchemy session."""
    return SessionLocal()
