import datetime

from sqlalchemy import Column, Integer, TEXT, Date

from fligt_service.database.base import Base


class Flight(Base):

    __tablename__ = "flight"

    id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    file_name: str = Column("file_name", TEXT, nullable=False)
    flt: int = Column("flt", Integer, nullable=False)
    depdate: datetime.date = Column("depdate", Date, nullable=False, index=True)
    dep: str = Column("dep", TEXT, nullable=False)


