from __future__ import annotations
from enum import Enum
from datetime import datetime, timezone, timedelta

NAME = 'tickerdax'
URL = f'https://{NAME}.com'
GLOBAL_INSTANCE_NAME = f'global_{NAME}_client_instance'
REDS_CONFIG_FILE = '/var/tickerdax/redis.conf'


class BaseEnum(str, Enum):
    value: str
    description: str

    def __new__(
            cls, value: str, description: str = ""
    ) -> BaseEnum:
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def list(cls):
        return list(map(lambda e: (e.value, e.description), cls))


class ConfigFormats(Enum):
    YAML = 'yaml'
    JSON = 'json'


class Default:
    ROUTES = ['order-book/predictions/v1/10']
    SYMBOLS = ['BTC']
    TIMEFRAME = '1h'


class KeyTypes:
    REST = 'REST'
    WEBSOCKET = 'WEBSOCKET'


class Envs(BaseEnum):
    DEV = (f'{NAME.upper()}_DEV', '')
    OFFICIAL_DOCKER_IMAGE = (f'{NAME.upper()}_OFFICIAL_DOCKER_IMAGE', '')

    CONFIG = (
        f'{NAME.upper()}_CONFIG',
        'A file path to the config file for the CLI.'
    )
    LOGS_FOLDER = (
        f'{NAME.upper()}_LOGS_FOLDER',
        'A folder path where the logs will be saved.'
    )
    EMAIL = (
        f'{NAME.upper()}_EMAIL',
        'Your email linked to your tickerdax.com account.'
    )
    REST_API_KEY = (
        f'{NAME.upper()}_REST_API_KEY',
        'Your REST API created with your tickerdax.com account.'
    )
    WEBSOCKET_API_KEY = (
        f'{NAME.upper()}_WEBSOCKET_API_KEY',
        'Your websocket API created with your tickerdax.com account. '
    )
    CACHE_ROOT = (
        f'{NAME.upper()}_CACHE_ROOT',
        "An alternative persistent cache location on disk. By default this is written into a `tickerdax_cache` folder "
        "in your system's temp folder."
    )
    REDIS_SERVER_ADDRESS = (
        f'{NAME.upper()}_REDIS_SERVER_ADDRESS',
        'An alternative redis server address. Can be useful if redis is on another address besides localhost.'
    )
    REDIS_SERVER_PORT = (
        f'{NAME.upper()}_REDIS_SERVER_PORT',
        'An alternative redis server port. Can be useful if redis needs to user another port besides `6379`.'
    )


EXAMPLE_CONFIG_DATA = {
    NAME: {
        "routes": {route: Default.SYMBOLS for route in Default.ROUTES},
        "start": (datetime.now(tz=timezone.utc) - timedelta(hours=6)).strftime('%Y-%m-%dT%H:00:00'),
        "timeframe": Default.TIMEFRAME,
        "fill_to_now": True
    }
}
