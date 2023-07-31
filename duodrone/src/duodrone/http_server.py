import asyncio
import threading
from logging import getLogger
from logging.config import dictConfig

from hypercorn.asyncio import serve as hypercorn_asyncio_serve
from loguru import logger
from quart import Quart, request, jsonify
from quart.logging import default_handler

from duodrone import config
from duodrone.config import DuodroneConfig
from duodrone.data import OuterEvent

SHUTDOWN_TRIGGER_ADVICE = '''Config `hypercorn_shutdown_trigger` must be set if you run the hypercorn in a non-main thread, or the http server won't start.
A typical way to do this (in the main thread):

loop = asyncio.new_event_loop()
t = Thread(target=start_background_loop, args=(loop,), daemon=True)
t.start()

# please notice that it's not the threading.Event!
event = asyncio.Event()

async def stop_async_http_server():
    SIGNAL_EVENT.set()
    loop.call_soon(loop.stop)


def signal_handler(_, __):
    logger.bind(o=True).info('Signal received, exiting...')
    asyncio.run_coroutine_threadsafe(stop_async_http_server(), loop)

    # waiting for event loop closing
    while True:
        if not loop.is_running():
            break
        time.sleep(0.1)

    # then exit this main thread, with daemon async thread
    exit(1)

# the default hypercorn shutdown trigger binds these three signals
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGBREAK, signal_handler)

duodrone.config.hypercorn_shutdown_trigger = event.wait

# Then start this module in a non-main thread
def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

asyncio.run_coroutine_threadsafe(duodrone.get_duodrone_coroutine(), loop)
'''

duodrone_config = DuodroneConfig()

app = Quart(__name__)


@app.before_serving
async def config_loggers():
    dictConfig({
        'version': 1,
        'loggers': {
            'quart.app': {
                'level': duodrone_config.logger_config.quart_level,
            },
            'quart.serving': {
                'level': duodrone_config.logger_config.quart_level
            },
            'hypercorn.access': {
                'level': duodrone_config.logger_config.quart_level
            },
            'hypercorn.error': {
                'level': duodrone_config.logger_config.quart_level
            }
        },
    })

    # https://pgjones.gitlab.io/quart/how_to_guides/logging.html#disabling-removing-handlers
    getLogger('quart.app').removeHandler(default_handler)
    getLogger('quart.serving').removeHandler(default_handler)

    # https://pgjones.gitlab.io/hypercorn/how_to_guides/logging.html
    # with reading the code of hypercorn.logging._create_logger
    for _logger in {getLogger('hypercorn.access'), getLogger('hypercorn.error')}:
        for handler in _logger.handlers:
            if not isinstance(handler, config.LoguruInterceptHandler):
                _logger.removeHandler(handler)


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
        logger.error('Config `hypercorn_shutdown_trigger` is None while in non-main thread.')
        raise ValueError(SHUTDOWN_TRIGGER_ADVICE)


@logger.catch
async def get_server_coroutine():
    if duodrone_config.debug:
        app.debug = True

    check_shutdown_trigger_in_non_main_thread()
    await hypercorn_asyncio_serve(app, duodrone_config.hypercorn_config,
                                  shutdown_trigger=duodrone_config.hypercorn_shutdown_trigger)


if __name__ == '__main__':
    asyncio.run(get_server_coroutine())
