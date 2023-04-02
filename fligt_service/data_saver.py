from typing import Any, Type

from fligt_service.database.base import Base, DBSession


class DataSaver:
    def __init__(self, model: Type["Base"]):
        self.model = model
        self.session = DBSession

    def save_one_row(self, data: dict):
        flight = self.model(**data)
        with self.session() as session:
            session.add(flight)
            session.commit()

    def save_multiple_rows(self, data: list[dict[str, Any]]):
        """
        Может использоваться для вставки нескольких строк в таблицу,
        так как по ТЗ этого не нужно, оставлю его абстрактным
        :param data: data for saving
        :return: None
        """
        raise NotImplementedError