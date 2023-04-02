from celery import Celery

import config
from file_generator.generator import FileGenerator

client = Celery(__name__, broker=config.redis_url)


@client.task
def generate_file():
    """Просто таска для Celery"""
    file_generator = FileGenerator()
    file_generator.generate_mock_file()
