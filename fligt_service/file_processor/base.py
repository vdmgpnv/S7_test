import json
import os
import shutil
from operator import methodcaller
from dateutil.parser import ParserError
from typing import Type

from loguru import logger

from fligt_service.data_saver import DataSaver
from fligt_service.database.base import Base
from services.amqp.consumer import RabbitConsumer
from services.amqp.producer import RabbitProducer


class BaseFileProcessor:
    def __init__(self, queue: str, model: Type["Base"]):
        self.consumer = RabbitConsumer(queue=queue)
        self.producer = RabbitProducer(queue="database")
        self.base_folder = "reports/"
        self.files_in_folder = "In/"
        self.errors_folder = "Err/"
        self.ok_folder = "Ok/"
        self.files_out_folder = "Out/"
        self.model = model
        self.full_path = None
        self.ok_files_folder = self.get_file_destination_folder("Ok")
        self.error_files_folder = self.get_file_destination_folder("Err")

    def start_processing(self):
        self.consumer.consume(self.callback)

    def callback(self, ch, method, properties, body: bytes) -> None:
        """
        Принимаем сообщения из кролика с именем файла
        и начинаем его обрабатывать
        """
        message = json.loads(body)
        try:
            file_name, file_type = message.get("filename").split(".")
            logger.info(f"Start process file {file_name}")
            self.full_path = self.get_file_destination_folder("In", file_name, file_type)
            json_data = methodcaller(f"process_{file_type}_file", file_name)(
                self
            )
            out_file = self.get_file_destination_folder("Out", file_name, "json")
            logger.info(f"Processing is finished, start write to json file {out_file}")
            with open(out_file, "w") as file:
                json.dump(json_data, file)
            self.__move_file(self.full_path, self.ok_files_folder)
            body_to_safe_in_database = self.get_saving_data(
                message.get("filename"),
                json_data.get("flt"),
                json_data.get("date"),
                json_data.get("dep"),
            )
            data_saver = DataSaver(self.model)
            data_saver.save_one_row(body_to_safe_in_database)
            logger.success("All process finished correctly")
        except KeyError as key_error:
            logger.error(f"An key error, moving file {key_error}")
            self.__move_file(self.full_path, self.error_files_folder)
        except ParserError as parser_error:
            logger.error(f"Bad date was come in file {parser_error}")
            self.__move_file(self.full_path, self.error_files_folder)
        except ValueError as value_error:
            logger.error(f"Key error {value_error}")
            self.__move_file(self.full_path, self.error_files_folder)



    def get_file_destination_folder(
        self, type: str, filename: str | None = None, file_type: str | None = None
    ) -> str:
        """
        Функция для получения пути, куда сохранять файлы при разных сценариях
        :param type:
        :param filename:
        :param file_type:
        :return:
        """
        match type:
            case "Ok":
                return self.base_folder + self.ok_folder
            case "Err":
                return self.base_folder + self.errors_folder
            case "Out":
                return (
                    self.base_folder
                    + self.files_out_folder
                    + filename
                    + "."
                    + file_type
                )
            case "In":
                return (
                    self.base_folder + self.files_in_folder + filename + "." + file_type
                )

    def get_saving_data(
        self, file_name: str, flt: int, depdate: str, dep: str
    ) -> dict[str, str | int]:
        return dict(file_name=file_name, flt=flt, depdate=depdate, dep=dep)

    def __move_file(self, file: str, destination: str):
        try:
            shutil.move(file, destination)
        except shutil.Error:
            pass
