import sqlite3

from constants import DATABASE_PATH
from model import GardenObservation

db_connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)


def write_observation(data: GardenObservation):
    sql = """
    INSERT INTO Garden(timestamp, temperature, humidity, lux, moisture, device_id)
    VALUES(?, ?, ?, ?, ?, ?)
    """
    cur = db_connection.cursor()
    cur.execute(sql, data.to_sql_row())
    db_connection.commit()