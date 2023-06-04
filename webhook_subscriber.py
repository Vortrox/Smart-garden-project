import json
import logging

from flask import Flask, request

from events import publish_observation
from model import GardenObservation
from persistence import write_observation

app = Flask(__name__)


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

        # Trigger hooks
        publish_observation(observation)

        return {}, 201
    return {"error": "Request must be JSON"}, 415


logging.info("Ready")
