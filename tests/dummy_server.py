import eventlet
from eventlet import wsgi
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['POST'])
def slow_response():
    t = request.get_data(as_text=True)
    print(f'from http: {t}')
    eventlet.sleep(5)
    print('slow response')
    return jsonify("from slow server: hi!")


def start_flask():
    print("Starting Flask server...")
    wsgi.server(eventlet.listen(('', 1415)), app)


if __name__ == '__main__':
    start_flask()
