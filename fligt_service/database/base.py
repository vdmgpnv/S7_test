from typing import Any, Union

from sqlalchemy import Column, MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

from config import db_url, debug_mode


engine: Engine = create_engine(
    db_url, echo=debug_mode, pool_pre_ping=True
)

DBSession = sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
