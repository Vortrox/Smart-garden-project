import logging
from typing import Callable, Any
from time import time, strftime
import pandas as pd
import matplotlib.pyplot as plt
from dateutil.tz import gettz
from matplotlib.dates import DateFormatter

from constants import USER_EMAIL, DESTINATION_EMAIL, MINIMUM_DELAY_BETWEEN_NOTIFICATIONS
from emails import send_email
from model import GardenObservation
from persistence import get_last_24h


def register_garden_event(condition: Callable[[GardenObservation], bool], action: Callable[[GardenObservation], Any]):
    garden_events.append((condition, action))


def publish_observation(data: GardenObservation):
    for condition, action in garden_events:
        if condition(data):
            action(data)


def low_soil_moisture_event(observation: GardenObservation):
    logging.info("Low soil moisture event detected")
    send_email(USER_EMAIL, DESTINATION_EMAIL,
               "Smart garden: Low soil moisture detected",
               f"Low soil moisture has been detected, please water your plant! The current soil moisture is {observation.moisture}")
    last_run_timestamp["low_soil_moisture_event"] = time()


def high_temperature_event(observation: GardenObservation):
    logging.info("High temperature event detected")
    send_email(USER_EMAIL, DESTINATION_EMAIL,
               "Smart garden: High air temperature detected",
               f"Your plant is in a hot area, please move it to somewhere colder! The current temperature is {observation.temperature}")
    last_run_timestamp["high_temperature_event"] = time()


def low_humidity_event(observation: GardenObservation):
    logging.info("High temperature event detected")
    send_email(USER_EMAIL, DESTINATION_EMAIL,
               "Smart garden: High air temperature detected",
               f"Your plant is in a very dry area, please move it somewhere that is less dry! The current humidity is {observation.humidity}")
    last_run_timestamp["high_temperature_event"] = time()


def daily_report(_):
    # Read data from database from last 24h
    df = get_last_24h()

    # Summarize statistics for each variable
    sensor_variables = ["temperature", "humidity", "lux", "moisture"]
    summary_df = pd.DataFrame(columns=["Min", "Max", "Mean"], index=sensor_variables)
    df.loc[:, "timestamp"] /= 86400
    for variable in sensor_variables:
        data = df.loc[:, variable]
        summary_df.loc[variable] = [data.min(), data.max(), data.mean()]

        # Make scatter plots for each variable against time
        fig, ax = plt.subplots()
        fig.set_figwidth(15)
        ax.scatter(df.loc[:, "timestamp"], data)
        ax.set_xlabel("Time")
        ax.xaxis.set_major_formatter(DateFormatter("%Y-%b-%d %H:%M:%S", tz=gettz()))
        plt.xticks(rotation=10)
        ax.set_ylabel(variable.capitalize())
        plt.savefig(f"report_figures/{variable}.png", format="png")

    # Send email to user with all this information
    send_email(USER_EMAIL, DESTINATION_EMAIL,
               "Smart garden: Daily report",
               f"Sensor readings in the last 24h:\n{summary_df.to_markdown()}",
               [f"report_figures/{v}.png" for v in sensor_variables])
    last_run_timestamp["daily_report"] = time()


garden_events = []
last_run_timestamp = {
    "low_soil_moisture_event": 0.0,
    "high_temperature_event": 0.0,
    "low_humidity_event": 0.0,
    "daily_report": 0.0
}

# Register event hooks
register_garden_event(lambda observation: observation.moisture < 800 and last_run_timestamp["low_soil_moisture_event"] - time() < MINIMUM_DELAY_BETWEEN_NOTIFICATIONS, low_soil_moisture_event)
register_garden_event(lambda observation: observation.temperature > 30 and last_run_timestamp["high_temperature_event"] - time() < MINIMUM_DELAY_BETWEEN_NOTIFICATIONS, high_temperature_event)
register_garden_event(lambda observation: observation.humidity < 40 and last_run_timestamp["low_humidity_event"] - time() < MINIMUM_DELAY_BETWEEN_NOTIFICATIONS, low_humidity_event)
register_garden_event(lambda observation: last_run_timestamp["daily_report"] - time() < 86400, daily_report)
