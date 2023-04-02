from typing import Any, Type

from sqlalchemy.exc import IntegrityError
from loguru import logger

from fligt_service.database.base import Base, DBSession


class DataSaver:
    def __init__(self, model: Type["Base"]):
        self.model = model
        self.session = DBSession

    def save_one_row(self, data: dict):
        """
        Принимаем строку для записи и пишем в бд
        :param data:
        :return:
        """
        logger.info("Saving data...")
        try:
            flight = self.model(**data)
            with self.session() as session:
                session.add(flight)
                session.commit()
        except IntegrityError as e:
            logger.error("Failed to save data...")

    def save_multiple_rows(self, data: list[dict[str, Any]]):
        """
        Может использоваться для вставки нескольких строк в таблицу,
        так как по ТЗ этого не нужно, оставлю его абстрактным
        :param data: data for saving
        :return: None
        """
        raise NotImplementedError