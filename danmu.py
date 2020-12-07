from gevent.pywsgi import WSGIServer
from flask import Flask
import config
import socketio
from flask_cors import CORS
sio = socketio.Server(cors_allowed_origins='*', logger=True, engineio_logger=True, async_mode='gevent')
app = Flask(__name__)
CORS(app)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


@sio.event(namespace="/new_danmu")
def connect(sid, environ):
    print('connect ', sid)


@sio.event(namespace="/new_danmu")
def my_message(sid, data):
    print('message ', data)


@sio.event(namespace="/new_danmu")
def disconnect(sid):
    print('disconnect ', sid)


def socket():
    print(config.ip, ":", config.Danmu_SocketPort)
    https_server = WSGIServer((config.ip, config.Danmu_SocketPort), app)
    print("https server start")
    https_server.serve_forever()

