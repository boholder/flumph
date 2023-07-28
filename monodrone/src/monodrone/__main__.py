import asyncio
import signal
import sys
from threading import Thread

import duodrone
from duodrone import config as duodrone_config
from monodrone.interface.outer_event_handler import OuterEventHandler
from monodrone.ui.main_window import start_main_window


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


ASYNCIO_EVENT_LOOP = asyncio.new_event_loop()
ASYNCIO_EVENT_LOOP.set_debug(True)
ASYNCIO_THREAD = Thread(target=start_background_loop, args=(ASYNCIO_EVENT_LOOP,), daemon=True,
                        name="DUODRONE_ASYNCIO_THREAD")
ASYNCIO_THREAD.start()

SIGNAL_EVENT = asyncio.Event()


def signal_handler(_, __):
    print('Signal received, exiting...')
    SIGNAL_EVENT.set()
    exit(1)


def get_duodrone_coroutine():
    duodrone_config.outer_event_handler = OuterEventHandler().handle
    duodrone_config.hypercorn_shutdown_trigger = SIGNAL_EVENT.wait
    return duodrone.get_duodrone_coroutine()


def main():
    # signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGBREAK, signal_handler)

    # start http service in another thread
    asyncio.run_coroutine_threadsafe(get_duodrone_coroutine(), ASYNCIO_EVENT_LOOP)

    # keep gui stay in main thread
    sys.exit(start_main_window())


if __name__ == '__main__':
    main()
