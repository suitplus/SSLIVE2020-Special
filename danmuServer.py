import logging
import config
from flask import Flask
from flask_socketio import SocketIO, emit
import time


class SingleDanmu:
    def __init__(self, value):
        self.value = value
        self.time = int(round(time.time() * 1000))

    def verify(self):
        # todo 验证弹幕是否可发布
        return True


socketApp = Flask(__name__)
socketApp.config['SECRET_KEY'] = "SECKEY"
socketio = SocketIO(socketApp, cors_allowed_origins='*', async_mode="gevent")
danmuList = []
OnlineWatchers = 0


@socketio.on('new_danmu')
def adding(data):
    global OnlineWatchers
    r = data.get("text")
    if r == "null-999Null":
        return "fail"
    else:
        print("新建弹幕", r)
        # 加入历史弹幕集
        danmuList.append(SingleDanmu(str(r)))
        emit("danmu", str(r), broadcast=True)


def changingInwatcher():
    emit('watchersNum', str(OnlineWatchers))


@socketio.on('connect')
def test_connect():
    global OnlineWatchers
    # 连接成功，在线人数+1
    OnlineWatchers += 1
    changingInwatcher()


@socketio.on('disconnect')
def disconnect():
    global OnlineWatchers
    OnlineWatchers -= 1
    changingInwatcher()


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
