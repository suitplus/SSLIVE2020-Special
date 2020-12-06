import logging

import config
from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

socketApp = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
CORS(socketApp, resources={r"/*": {"origins": "*"}})
socketApp.config['SECRET_KEY'] = "SECKEY"
socketio = SocketIO(socketApp, cors_allowed_origins='*')


@socketio.on('connect', namespace='/new_danmu')
def danmu_connect():
    # return false # 不予连接
    emit('feedback', {'data': 'Connected'})


# 断开连接事件
# @socketio.on('disconnect', namespace='/new_damu')
# def danmu_disconnect():
#     print('Client disconnected')


@socketio.on('my event', namespace="/new_danmu")
def send_danmu(text):
    emit('danmu', text, broadcast=True)


@socketApp.route("/addingdanmu", methods=["POST"])
def adding():
    r = request.args.get("danmutext", default="null-999Null")
    if r == "null-999Null":
        return "fail"
    else:
        send_danmu(r)


def SocketStart():
    print("弹幕服务器启动在", config.ip, ':', config.Danmu_SocketPort)
    socketio.run(socketApp, config.ip, config.Danmu_SocketPort)

