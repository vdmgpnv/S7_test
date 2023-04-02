import datetime

from pydantic import BaseModel


class FlightResponse(BaseModel):
    id: int
    id: int
    file_name: str
    depdate: datetime.date
    dep: str
