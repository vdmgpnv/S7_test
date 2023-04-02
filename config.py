import os

db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "postgres")
db_name = os.getenv("DB_NAME", "S7")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")
redis_url = os.getenv("REDIS", "redis://redis:6379/0")


db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

debug_mode = False

rabbit_user = "admin"
rabbit_password = "password"
rabbit_host = "localhost"