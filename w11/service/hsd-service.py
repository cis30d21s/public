# upgrade flask, install flask-cors
from typing import Any, Generator
import flask
from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler
from MessageAnnouncer import MessageAnnouncer
from ArmSwitch import ArmSwitch
from MotionDistance import MotionDistanceMonitor
from TamperAlert import TamperAlert
import logging
import time

app = flask.Flask(__name__)
CORS(app)
announcer = MessageAnnouncer()
armSwitch = ArmSwitch(
    18, 23, lambda v: announcer.announce(flask.json.dumps({'armed': v}), 'status'))
motionDistanceMonitor = MotionDistanceMonitor(
    24, 25, 12,
    lambda d: announcer.announce(flask.json.dumps(
        {'motion': True, 'distance': d}), 'motion'),
    lambda d: announcer.announce(flask.json.dumps(
        {'motion': False, 'distance': d}), 'motion'),
    lambda: armSwitch.armed)
tamperAlert = TamperAlert()
tamperAlert.when_moved = lambda: announcer.announce(flask.json.dumps(
    {'tampered': True}), 'tamper') if armSwitch.armed else None


@app.route('/status')
def get_status() -> Any:
    return {'armed': armSwitch.armed}


@app.route('/status', methods=['PATCH'])
def update_status() -> Any:
    body = flask.request.get_json()
    if 'armed' in body:
        logging.debug(f"Updating `armed` to: {body['armed']}")
        armSwitch.armed = body['armed']
        return {}, 200
    else:
        return {'error': 'invalid request'}, 400


@app.route('/ping')
def ping() -> Any:
    '''For testing only'''
    announcer.announce(flask.json.dumps({'armed': True}), 'status')
    return {}, 200


@app.route('/listen')
def listen() -> flask.Response:
    def stream() -> Generator[str, None, None]:
        listener_id, messages = announcer.listen()  # returns a queue.Queue
        while True:
            message = messages.get()  # blocks until a new message arrives
            logging.debug(
                f'Sending message to listener #{listener_id}: {message}')
            yield message
            time.sleep(0.05)  # throttle messages
    return flask.Response(stream(), mimetype='text/event-stream')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(threadName)s] %(message)s')
    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    app.run(host='0.0.0.0', debug=True)
