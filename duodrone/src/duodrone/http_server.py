import asyncio
import threading
from logging import getLogger

import hypercorn
from hypercorn.asyncio import serve as hypercorn_asyncio_serve
from loguru import logger
from quart import Quart, request, jsonify
from quart.logging import default_handler

from duodrone.config import DuodroneConfig
from duodrone.data import OuterEvent

SHUTDOWN_TRIGGER_ADVICE = '''Config hypercorn_shutdown_trigger must be set if you run the hypercorn in a non-main thread, or the http server won't start. A typical way to do this (in the main thread):

# please notice that it's not the threading.Event!
event = asyncio.Event()

def signal_handler(_, __):
    event.set()

# the default hypercorn shutdown trigger binds these three signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGBREAK, signal_handler)

duodrone.config.hypercorn_shutdown_trigger = event.wait

# Then start this module in a non-main thread
def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

loop = asyncio.new_event_loop()
loop.set_debug(True)
t = Thread(target=start_background_loop, args=(loop,), daemon=True)
t.start()

asyncio.run_coroutine_threadsafe(duodrone.get_duodrone_coroutine(), loop)
'''

duodrone_config = DuodroneConfig()

app = Quart(__name__)

# remove default logger handlers
# https://pgjones.gitlab.io/quart/how_to_guides/logging.html#disabling-removing-handlers
getLogger('quart.app').removeHandler(default_handler)
getLogger('quart.serving').removeHandler(default_handler)

# read the code of hypercorn.logging._create_logger
for logger in (getLogger('hypercorn.access'), getLogger('hypercorn.error')):
    for handler in logger.handlers:
        logger.removeHandler(handler)


@app.route('/', methods=['POST'])
async def receive_text():
    text = await request.get_data(as_text=True)
    logger.info(f'from http: {text}')
    duodrone_config.outer_event_handler(OuterEvent(text))
    return jsonify(success=True)


def check_shutdown_trigger_in_non_main_thread():
    not_in_main_thread = threading.current_thread().__class__.__name__ != '_MainThread'
    trigger_is_none = duodrone_config.hypercorn_shutdown_trigger is None
    if not_in_main_thread and trigger_is_none:
        logger.error('Config hypercorn_shutdown_trigger must be set if you run the hypercorn in a non-main thread.')
        logger.bind(o=True).error(SHUTDOWN_TRIGGER_ADVICE)
        raise NotImplementedError(SHUTDOWN_TRIGGER_ADVICE)


async def get_server_coroutine():
    if duodrone_config.debug:
        app.debug = True

    # TODO 目标，让这个子线程报错正常显示
    check_shutdown_trigger_in_non_main_thread()
    await hypercorn_asyncio_serve(app, duodrone_config.hypercorn_config,
                                  shutdown_trigger=duodrone_config.hypercorn_shutdown_trigger)


if __name__ == '__main__':
    asyncio.run(get_server_coroutine())
