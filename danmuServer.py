import logging
import config
from flask import Flask
from flask_socketio import SocketIO, emit

socketApp = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
socketApp.config['SECRET_KEY'] = "SECKEY"
socketio = SocketIO(socketApp, cors_allowed_origins='*', async_mode="gevent")


@socketio.on('new_danmu')
def adding(data):
    r = data.get("text")
    if r == "null-999Null":
        return "fail"
    else:
        print("新建弹幕", r)
        socketio.emit("danmu", str(r), broadcast=True)


@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    print("连接成功")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketApp.route('/', methods=["GET"])
def index():
    return "SSLIVE弹幕模块"


def SocketStart():
    print("弹幕服务器启动在", config.ip, ':', config.Danmu_SocketPort)
    # https_server = WSGIServer((config.ip, config.Danmu_SocketPort), socketApp, certfile="SSL/4837013_www.ssersay.cn.pem",
    #                           keyfile="SSL/4837013_www.ssersay.cn.key", spawn=200)
    # https_server.serve_forever()
    # 直接面向外网
    socketio.run(app=socketApp, host="0.0.0.0", port=config.Danmu_SocketPort,
                 certfile="SSL/4837013_www.ssersay.cn.pem", keyfile="SSL/4837013_www.ssersay.cn.key")
