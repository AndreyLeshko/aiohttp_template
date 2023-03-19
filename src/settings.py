import json
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

# -------------------------------------------------- CONFIG ------------------------------------------------------------

DEFAULT_CONFIG_PATH = 'config.json'

_config = None


def read_config(path=DEFAULT_CONFIG_PATH) -> dict:
    global _config
    if _config is not None:
        return _config
    try:
        with open(path, "r") as file:
            _config = json.load(file)
        return _config
    except FileNotFoundError:
        print(f'Config file not found, \"config.json\" must be in {path}')
        sys.exit(1)


# -------------------------------------------------- LOGGER ------------------------------------------------------------


LOG_FILE_PATH = 'api.log'

logger = logging.getLogger('aiohttp.access')
logger.setLevel('DEBUG')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = TimedRotatingFileHandler(LOG_FILE_PATH, encoding='UTF-8', when='midnight', backupCount=10)
file_handler.setLevel(read_config()['api']['logger_level'])
file_handler.setFormatter(formatter)
file_handler.suffix = '%Y%m%d'
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel('DEBUG')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

logger.warning('--------------------------------------START APPLICATION---------------------------------------')
