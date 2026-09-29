import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

dbconfig = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "mental_wellness_db"),
}

# Connection pool avoids opening a fresh connection on every request
pool = pooling.MySQLConnectionPool(
    pool_name="wellness_pool",
    pool_size=5,
    **dbconfig
)


def get_connection():
    """Grab a connection from the pool. Always close() it when done (use try/finally)."""
    return pool.get_connection()
