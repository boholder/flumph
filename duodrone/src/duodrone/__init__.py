from typing import Callable

from duodrone import config
from duodrone.data import *
from duodrone.flask_server import start_flask


def start_duodrone(outer_request_callback: Callable[[OuterEvent], None] = None):
    if outer_request_callback is not None:
        config.outer_request_callback = outer_request_callback

    start_flask()
