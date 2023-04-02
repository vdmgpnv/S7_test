import datetime
from typing import Any

import pandas as pd
from dateutil import parser

from fligt_service.file_processor.base import BaseFileProcessor


class CSVFileProcessor(BaseFileProcessor):

    def process_csv_file(self, filename: str) -> dict[str, Any]:
        """
        Метод обработчик csv файла, загружаем с помощью pandas
        так как самая удобная либа для работы с такими файлами,
        а далее в пару строк формируем необходимый нам json
        """
        base_file = pd.read_csv(self.full_path, delimiter=";")
        base_file["bdate"] = base_file.apply(lambda row: str(parser.parse(row["bdate"]).date()), axis=1)
        flight = filename.split("_")
        flight_info = dict(
            flt=int(flight[1]),
            date=str(datetime.datetime.strptime(flight[0], "%Y%m%d").date()),
            dep=flight[2],
            prl=base_file.to_dict("records")
        )

        return flight_info

