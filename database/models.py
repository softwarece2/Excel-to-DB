"""
database/models.py
-------------------
SQLAlchemy models matching the existing ATE database schema.
"""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Identity, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base

import config

Base = declarative_base()
SCHEMA = config.DB_SCHEMA


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, Identity(always=True), primary_key=True)


class Test(Base):
    __tablename__ = "test"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, Identity(always=True), primary_key=True)


class Spec(Base):
    __tablename__ = "spec"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, Identity(always=True), primary_key=True)
    spec_val = Column(String, nullable=True)
    min = Column(Float, nullable=True)
    max = Column(Float, nullable=True)
    prod_id = Column(Integer, ForeignKey(f"{SCHEMA}.product.id"), nullable=False)
    test_id = Column(Integer, ForeignKey(f"{SCHEMA}.test.id"), nullable=False)
    param_code = Column(String, nullable=True)
    param_type = Column(Integer, ForeignKey(f"{SCHEMA}.param_type.id"), nullable=True)
    ty_clause_no = Column(String, nullable=True)
    unit = Column(Integer, ForeignKey(f"{SCHEMA}.units.id"), nullable=True)
    obs_type_id = Column(Integer, ForeignKey(f"{SCHEMA}.obs_type.id"), nullable=True)
    obs_value = Column(String, nullable=True)
    sl_no = Column(Integer, nullable=True)
    active = Column(Boolean, default=True, nullable=True)
    custom_bool_obs_value = Column(ARRAY(Integer), nullable=True)
    test_type_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.spec_test_type.id"), nullable=True
    )
    main_type_id = Column(
        Integer, ForeignKey(f"{SCHEMA}.main_type.id"), nullable=True
    )


class MainType(Base):
    __tablename__ = "main_type"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True)


class ParamType(Base):
    __tablename__ = "param_type"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True)
    param_type = Column(String)


class Unit(Base):
    __tablename__ = "units"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True)
    units = Column(String)


class ObsType(Base):
    __tablename__ = "obs_type"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True)


class SpecTestType(Base):
    __tablename__ = "spec_test_type"
    __table_args__ = {"schema": SCHEMA}
    id = Column(Integer, primary_key=True)
