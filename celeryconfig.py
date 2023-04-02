import os

import config

broker_url = os.getenv("REDIS", config.redis_url)
imports = ("tasks", )
worker_disable_rate_limits = True
timezone = 'Asia/Novosibirsk'
enable_utc = False
task_routes = {'tasks': {'queue': 'fetch_queue'}}

beat_schedule = {
    'parsing': {
        'task': 'tasks.tasks.parse_news',
        'schedule': 120.0
    }
}