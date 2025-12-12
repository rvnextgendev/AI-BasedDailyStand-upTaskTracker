import psycopg2
from contextlib import contextmanager
from ...config import get_settings


@contextmanager
def get_connection():
    settings = get_settings()
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
    )
    try:
        yield conn
    finally:
        conn.close()
