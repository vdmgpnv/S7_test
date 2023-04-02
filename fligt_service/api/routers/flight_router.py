import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from fligt_service.api.models.flight import FlightResponse
from fligt_service.database.base import get_session
from fligt_service.database.models import Flight

router = APIRouter()


@router.get("/flight", response_model=list[FlightResponse])
def get_flights_for_date(date: datetime.date, session: Session = Depends(get_session)):
    query = (
        select(Flight.id, Flight.file_name, Flight.flt, Flight.dep, Flight.depdate)
        .select_from(Flight)
        .where(Flight.depdate == date)
    )

    result = session.execute(query).mappings().all()

    return result
