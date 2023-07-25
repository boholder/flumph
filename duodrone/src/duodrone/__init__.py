from duodrone.config import DuoDroneConfig
from duodrone.data import *
from duodrone.flask_server import start_flask

config = DuoDroneConfig()


def start_duodrone():
    start_flask()
