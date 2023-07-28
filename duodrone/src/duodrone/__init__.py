from duodrone.config import DuodroneConfig
from duodrone.data import *
from duodrone.http_server import get_server_coroutine

config = DuodroneConfig()


def get_duodrone_coroutine():
    config.config_behaviors()
    return get_server_coroutine()
