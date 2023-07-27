from typing import Callable

from hypercorn.config import Config as HyperCornConfig

from duodrone.data import OuterEvent


class DuoDroneConfig:
    __instance: 'DuoDroneConfig' = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DuoDroneConfig, cls).__new__(cls)
        return cls.__instance

    outer_event_handler: Callable[[OuterEvent], None] = lambda self, resp: print(f'Dummy get outer response: {resp}')
    hypercorn_config = HyperCornConfig()

    def __init__(self):
        self.hypercorn_config.bind = 'localhost:1414'
        self.hypercorn_config.accesslog = '-'
