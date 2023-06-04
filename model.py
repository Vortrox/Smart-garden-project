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