import eventlet
from eventlet import wsgi
from flask import Flask, request, jsonify

from duodrone.config import DuoDroneConfig
from duodrone.data import OuterEvent

app = Flask(__name__)
app.debug = False

config = DuoDroneConfig()


@app.route('/', methods=['POST'])
def receive_text():
    t = request.get_data(as_text=True)
    print(f'from http: {t}')
    config.outer_request_callback(OuterEvent(t))
    return jsonify(success=True)


def start_flask():
    print("Starting Flask server...")
    wsgi.server(eventlet.listen(('', 1414)), app)
