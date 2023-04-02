from fligt_service.database.models import Flight
from fligt_service.file_processor.csv_processor import CSVFileProcessor

if __name__ == '__main__':
    csv_processor = CSVFileProcessor("files", Flight)

    csv_processor.start_processing()

