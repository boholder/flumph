import asyncio
import threading

from hypercorn.asyncio import serve as hypercorn_asyncio_serve
from quart import Quart, request, jsonify

from duodrone.config import DuoDroneConfig
from duodrone.data import OuterEvent

duodrone_config = DuoDroneConfig()

app = Quart(__name__)
app.debug = False


@app.route('/', methods=['POST'])
async def receive_text():
    text = await request.get_data(as_text=True)
    print(f'from http: {text}')
    duodrone_config.outer_event_handler(OuterEvent(text))
    return jsonify(success=True)


async def check_shutdown_trigger_in_non_main_thread():
    not_in_main_thread = threading.current_thread().__class__.__name__ != '_MainThread'
    trigger_is_none = duodrone_config.hypercorn_shutdown_trigger is None
    if not_in_main_thread and trigger_is_none:
        raise NotImplementedError('''shutdown_trigger must be set if you run the hypercorn in a non-main thread.
Or the http server won't started properly. A typical way to do this (in the main thread):

# not the threading.Event!        
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
''')


async def get_server_coroutine():
    await check_shutdown_trigger_in_non_main_thread()
    await hypercorn_asyncio_serve(app, duodrone_config.hypercorn_config,
                                  shutdown_trigger=duodrone_config.hypercorn_shutdown_trigger)


if __name__ == '__main__':
    asyncio.run(get_server_coroutine())
