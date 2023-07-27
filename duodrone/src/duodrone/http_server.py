import asyncio

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


def get_server_coroutine():
    return hypercorn_asyncio_serve(app, duodrone_config.hypercorn_config)


if __name__ == '__main__':
    asyncio.run(get_server_coroutine())
