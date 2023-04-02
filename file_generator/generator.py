import csv
import random

from loguru import logger

from .mock_data import mock_passenger_data, mock_file_names
from services.amqp.producer import RabbitProducer


class FileGenerator:

    def __init__(self):
        self.folder_for_file = "reports/In/"
        self.producer = RabbitProducer(queue="files")

    def generate_mock_file(self):
        """
        Генерируем файл со случайным названием и случайным кол-вом записей
        """
        header_row = ["num", "surname", "firstname", "bdate"]
        filename = random.choice(mock_file_names)
        row_numbers = random.randint(1, 6)
        with open(self.folder_for_file + filename, "w") as file:
            logger.info("Start generate the file")
            writer = csv.writer(file, delimiter=';')
            writer.writerow(header_row)
            for i in range(row_numbers):
                writer.writerow(random.choice(mock_passenger_data).values())

        with self.producer as producer:
            producer.send_message(
                dict(filename=filename)
            )
