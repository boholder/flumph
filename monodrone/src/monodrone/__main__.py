import asyncio
import signal
import sys
import time
from threading import Thread

from loguru import logger

import duodrone
from duodrone import config as duodrone_config
from monodrone.core.config import ASYNCIO_EVENT_LOOP
from monodrone.core.outer_event_handler import OuterEventHandler
from monodrone.ui.main_window import start_main_window


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()


# ASYNCIO_EVENT_LOOP.set_debug(True)
ASYNCIO_THREAD = Thread(target=start_background_loop, args=(ASYNCIO_EVENT_LOOP,), daemon=True,
                        name="DUODRONE_ASYNCIO_THREAD")
ASYNCIO_THREAD.start()

SIGNAL_EVENT = asyncio.Event()


async def stop_async_http_server():
    SIGNAL_EVENT.set()
    ASYNCIO_EVENT_LOOP.call_soon(ASYNCIO_EVENT_LOOP.stop)


def signal_handler(sig_num: int, __):
    logger.bind(o=True).info(f'Signal [{signal.Signals(sig_num).name}] received, exiting...')
    asyncio.run_coroutine_threadsafe(stop_async_http_server(), ASYNCIO_EVENT_LOOP)

    # waiting for event loop closing
    while True:
        if not ASYNCIO_EVENT_LOOP.is_running():
            logger.bind(o=True).info('Async http server closed.')
            break
        time.sleep(0.1)

    # then exit this main thread, with daemon async thread
    logger.bind(o=True).info('Main thread closed.')
    exit(1)


def config_duodrone():
    duodrone_config.debug = True
    duodrone_config.logger_config.duodrone_level = 'DEBUG'
    duodrone_config.logger_config.quart_level = 'INFO'
    duodrone_config.logger_config.hypercorn_level = 'INFO'
    duodrone_config.logger_config.httpx_level = 'INFO'
    duodrone_config.outer_event_handler = OuterEventHandler().handle
    duodrone_config.hypercorn_shutdown_trigger = SIGNAL_EVENT.wait
    duodrone_config.event_loop = ASYNCIO_EVENT_LOOP


@logger.catch
def main():
    # signal handling
    for sig in {signal.SIGINT, signal.SIGTERM, signal.SIGBREAK}:
        signal.signal(sig, signal_handler)

    # start http service in another thread
    config_duodrone()
    asyncio.run_coroutine_threadsafe(duodrone.get_duodrone_coroutine(), ASYNCIO_EVENT_LOOP)

    # keep gui stay in main thread
    sys.exit(start_main_window())


if __name__ == '__main__':
    main()
