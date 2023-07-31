import asyncio

import hypercorn.config
from hypercorn.asyncio import serve as hypercorn_asyncio_serve
from quart import Quart, request, jsonify

app = Quart(__name__)


@app.route('/', methods=['POST'])
async def slow_response():
    t = await request.get_data(as_text=True)
    print(f'from http: {t}')
    # await sleep(5)
    print('slow response')
    return jsonify('{"from_slow_server": "' + t + '"}')


async def start_http_server():
    c = hypercorn.config.Config()
    c.bind = 'localhost:1512'
    await hypercorn_asyncio_serve(app, c)


if __name__ == '__main__':
    asyncio.run(start_http_server())
