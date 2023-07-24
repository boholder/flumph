import eventlet
from eventlet import wsgi
from flask import Flask, request, jsonify

from monodrone.outer_event_handler import OuterEventHandler, Priority

app = Flask(__name__)
app.debug = False

outer_event_handler = OuterEventHandler()


@app.route('/', methods=['POST'])
def receive_text():
    t = request.get_data(as_text=True)
    print(f'from http: {t}')
    outer_event_handler.put(Priority.LOW, t + '-l')
    outer_event_handler.put(Priority.MIDDLE, t + '-m')
    outer_event_handler.put(Priority.HIGH, t + '-h')
    return jsonify(success=True)


def start_flask():
    print("Starting Flask server...")
    wsgi.server(eventlet.listen(('', 1414)), app)
