#include "Adafruit_DHT.h"
#include "BH1750Lib.h"

#define DHTPIN 6
#define DHTTYPE DHT11
#define UARTDEBUG 1

DHT dht(DHTPIN, DHTTYPE);
BH1750Lib lightSensor;

const int soilMoisturePin = A2;

void setup() {
    lightSensor.begin(BH1750LIB_MODE_CONTINUOUSHIGHRES);
	dht.begin();
	Serial.begin(9600);
}

void loop() {
	float temperature = dht.getTempCelcius();
    float humidity = dht.getHumidity();
	uint16_t lux = lightSensor.lightLevel();
	int moisture = analogRead(soilMoisturePin);
	int timestamp = (int) Time.now();
	
	delay(2000);
	
	if (!isnan(temperature) && !isnan(humidity) && !isnan(lux) && !isnan(moisture)) {
	    Particle.publish("sensor_data", String::format("{\"timestamp\": %i, \"temperature\": %.1f, \"humidity\": %.1f, \"lux\": %i, \"moisture\": %i}", timestamp, temperature, humidity, lux, moisture), PRIVATE);
	}
	
	Serial.print(String::format("Timestamp: %i", timestamp));
	Serial.print(String::format(" Temperature: %.1f", temperature));
	Serial.print(String::format(" Humidity: %.1f", humidity));
	Serial.print(String::format(" Lux: %i", lux));
	Serial.println(String::format(" Moisture: %i", moisture));
	Serial.println(String::format("{\"timestamp\": %i, \"temperature\": %.1f, \"humidity\": %.1f, \"lux\": %i, \"moisture\": %i}", timestamp, temperature, humidity, lux, moisture));
}