import sqlite3
from time import time

from constants import DATABASE_PATH
from model import GardenObservation
import pandas as pd

db_connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)


def write_observation(data: GardenObservation):
    """Writes a single observation to the database"""
    sql = """
    INSERT INTO Garden(timestamp, temperature, humidity, lux, moisture, device_id)
    VALUES(?, ?, ?, ?, ?, ?)
    """
    cur = db_connection.cursor()
    cur.execute(sql, data.to_sql_row())
    db_connection.commit()


def get_last_24h() -> pd.DataFrame:
    """Retrieves the garden data from the last 24 hours"""
    sql = """
    SELECT timestamp, temperature, humidity, lux, moisture FROM Garden
    WHERE timestamp > ?
    """
    timestamp_24h_ago = int(time()) - 86400
    return pd.read_sql(sql, db_connection, params=(timestamp_24h_ago, ))


if __name__ == "__main__":
    data = get_last_24h()
    pass
