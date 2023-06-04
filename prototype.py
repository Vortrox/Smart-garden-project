from flask import Flask, request, jsonify
import json
import sqlite3
import os
import logging

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(PROJECT_ROOT, "smart_garden_data.db")
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "debug.log")

# Logging config
logging.basicConfig(
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ],
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
db_connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

class GardenObservation:
    def __init__(self, timestamp, temperature, humidity, lux, moisture, device_id):
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.lux = lux
        self.moisture = moisture
        self.device_id = device_id

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "lux": self.lux,
            "moisture": self.moisture,
            "device_id": self.device_id
        }

    def to_sql_row(self):
        return (
            self.timestamp,
            self.temperature,
            self.humidity,
            self.lux,
            self.moisture,
            self.device_id
        )


def write_observation(data: GardenObservation):
    sql = """
    INSERT INTO Garden(timestamp, temperature, humidity, lux, moisture, device_id)
    VALUES(?, ?, ?, ?, ?, ?)
    """
    cur = db_connection.cursor()
    cur.execute(sql, data.to_sql_row())
    db_connection.commit()


@app.post("/")
def receive_sensor_data():
    if request.is_json:
        # Read data from webhook
        webhook_json = request.get_json()
        smart_garden_data = json.loads(webhook_json["data"])
        smart_garden_data["device_id"] = webhook_json["coreid"]
        logging.debug(smart_garden_data)

        # Save data to database
        observation = GardenObservation(**smart_garden_data)
        write_observation(observation)

        return {}, 201
    return {"error": "Request must be JSON"}, 415


logging.info("Ready")
