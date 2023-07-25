from typing import Callable

from duodrone.data import OuterEvent


class DuoDroneConfig:
    __instance: 'DuoDroneConfig' = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DuoDroneConfig, cls).__new__(cls)
        return cls.__instance

    outer_request_callback: Callable[[OuterEvent], None] = lambda resp: print(f'Dummy get outer response: {resp}')
