from typing import Callable, Any

from model import GardenObservation

garden_events = []


def register_garden_event(condition: Callable[[GardenObservation], bool], action: Callable[[GardenObservation], Any]):
    garden_events.append((condition, action))


def publish_observation(data: GardenObservation):
    for condition, action in garden_events:
        if condition(data):
            action(data)
