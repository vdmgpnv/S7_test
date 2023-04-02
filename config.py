import os

db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "123321105qQ")
db_name = os.getenv("DB_NAME", "S7")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

debug_mode = True

rabbit_user = "admin"

rabbit_password = "password"
rabbit_host = "localhost"