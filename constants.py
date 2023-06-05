import logging
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE_PATH = os.path.join(PROJECT_ROOT, "smart_garden_data.db")
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "debug.log")
MINIMUM_DELAY_BETWEEN_NOTIFICATIONS = 21600  # seconds
USER_EMAIL = "vortrox117@gmail.com"
DESTINATION_EMAIL = USER_EMAIL

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