from typing import Callable, Optional, Awaitable

from hypercorn.config import Config as HyperCornConfig

from duodrone.data import OuterEvent


class DuoDroneConfig:
    """
    Various configurations for duodrone.

    :param outer_event_handler: Handler for outer events
    :param hypercorn_config: Hypercorn configuration
    :param hypercorn_shutdown_trigger: Shutdown trigger
    """

    __instance: 'DuoDroneConfig' = None
    outer_event_handler: Callable[[OuterEvent], None] = lambda self, resp: print(f'Dummy get outer response: {resp}')
    hypercorn_config = HyperCornConfig()
    hypercorn_shutdown_trigger: Optional[Callable[..., Awaitable[None]]] = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DuoDroneConfig, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.hypercorn_config.bind = 'localhost:1414'
        self.hypercorn_config.accesslog = '-'
