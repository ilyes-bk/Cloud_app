from psycopg_pool import ConnectionPool
import os
connection_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
}

pool = ConnectionPool(
    conninfo=os.environ["DATABASE_URL"] ,
    max_size=5,
    kwargs=connection_kwargs,
)
