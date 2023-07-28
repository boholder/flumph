from typing import Callable, Optional, Awaitable

from hypercorn.config import Config as HyperCornConfig

from duodrone.data import OuterEvent


class DuoDroneConfig:
    """
    Configurations for duodrone module.
    """

    __instance: 'DuoDroneConfig' = None

    outer_event_handler: Callable[[OuterEvent], None] = lambda self, resp: print(f'Dummy get outer response: {resp}')
    """outer event handler"""

    hypercorn_config = HyperCornConfig()
    """hypercorn config"""

    hypercorn_shutdown_trigger: Optional[Callable[..., Awaitable[None]]] = None
    """hypercorn shutdown trigger"""

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DuoDroneConfig, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        # default configs
        self.hypercorn_config.bind = 'localhost:1414'
        self.hypercorn_config.accesslog = '-'
