import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from fligt_service.api.models.flight import FlightResponse
from fligt_service.database.base import get_session
from fligt_service.database.models import Flight

router = APIRouter()


@router.get("/flight", response_model=list[FlightResponse])
def get_flights_for_date(
    date_flight: datetime.date | None = Query(alias="date", default=None),
    session: Session = Depends(get_session),
):
    """
    Принимаем дату за которую будем возвращать все рейсы,
    если дата не передана, получим весь массив данных

    :param date: дата за которую нам интересны рейсы
    :return: json
    """
    query = select(
        Flight.id, Flight.file_name, Flight.flt, Flight.dep, Flight.depdate
    ).select_from(Flight)

    if date_flight:
        query = query.where(Flight.depdate == date_flight)

    result = session.execute(query).mappings().all()

    return result
