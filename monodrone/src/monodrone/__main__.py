import signal
import sys
from threading import Thread

from duodrone import config as duodrone_config
from duodrone import start_duodrone
from monodrone.interface.outer_event_handler import OuterEventHandler
from monodrone.ui.main_window import start_main_window


def config_and_start_duodrone():
    duodrone_config.outer_request_callback = OuterEventHandler().handle
    start_duodrone()


FLASK_THREAD = Thread(target=config_and_start_duodrone)
FLASK_THREAD.daemon = True


def signal_handler(_, __):
    print('CTRL + C detected, exiting ...')
    exit(1)


def main():
    # CTRL+C signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # start flask in another thread
    FLASK_THREAD.start()

    # keep gui stay in main thread
    sys.exit(start_main_window())


if __name__ == '__main__':
    main()
