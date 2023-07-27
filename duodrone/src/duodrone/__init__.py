from duodrone.config import DuoDroneConfig
from duodrone.data import *
from duodrone.http_server import get_server_coroutine

config = DuoDroneConfig()


def get_duodrone_coroutine():
    return get_server_coroutine()
