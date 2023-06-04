from flask import Flask, request, jsonify
import json

app = Flask(__name__)


@app.post("/")
def receive_sensor_data():
    if request.is_json:
        smart_garden_data = request.get_json()
        smart_garden_data["data"] = json.loads(smart_garden_data["data"])
        print(smart_garden_data)
        return {}, 201
    return {"error": "Request must be JSON"}, 415

