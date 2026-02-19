import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://inventory:inventory@127.0.0.1:5432/inventory_db",
)
