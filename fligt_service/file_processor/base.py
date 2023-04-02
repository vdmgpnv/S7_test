import json
import shutil
from operator import methodcaller
from typing import Type

from fligt_service.data_saver import DataSaver
from fligt_service.database.base import Base, DBSession
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
            json_data, in_file = methodcaller(f"process_{file_type}_file", file_name)(
                self
            )
            out_file = self.get_file_destination_folder("Out", file_name, "json")
            with open(out_file, "w") as file:
                json.dump(json_data, file)
            ok_files_folder = self.get_file_destination_folder("Ok")
            shutil.move(in_file, ok_files_folder)
            body_to_safe_in_database = self.get_saving_data(
                message.get("filename"),
                json_data.get("flt"),
                json_data.get("date"),
                json_data.get("dep"),
            )
            data_saver = DataSaver(self.model)
            data_saver.save_one_row(body_to_safe_in_database)
        except Exception as e:
            print(e)

    def get_file_destination_folder(
        self, type: str, filename: str | None = None, file_type: str | None = None
    ) -> str:
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
