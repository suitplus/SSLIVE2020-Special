# 官方文档 https://flask-socketio.readthedocs.io/en/latest/
import datetime

import Main
import config
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
import time


class ban:
    ip = ""
    time = 0

    def isIp(self, ip):
        return self.ip == ip

    def __init__(self, ip):
        self.ip = ip
        self.time = int(round(time.time() * 1000))

    def isOut(self):
        # 是否超
        return ((int(round(time.time() * 1000))-self.time)/60000.00) >= config.banTime


class SingleDanmu:
    value = ""
    time = 0
    id = 0
    senderIp = ""

    def __init__(self, value, ip):
        global idIndex
        idIndex += 1
        self.senderIp = ip
        self.id = idIndex
        self.value = value
        self.time = int(round(time.time() * 1000))


idIndex = 0
socketApp = Flask(__name__)
socketApp.config['SECRET_KEY'] = "SECKEY"
socketio = SocketIO(socketApp, cors_allowed_origins='*', async_mode="gevent")
# 弹幕名单
danmuList = []
# 封禁ip名单
blackList = []
OnlineWatchers = 0


@socketio.on('new_danmu')
def adding(data):
    global OnlineWatchers
    global blackList
    r = data.get("text")
    ip = data.get("ip")
    for bip in blackList:
        if bip.isIp(ip):
            # 是否在黑名单
            if bip.isOut():
                # 是否超出封禁时间
                blackList.remove(bip)
            else:
                return "ban"
    print("新建弹幕", r)
    # 加入历史弹幕集
    danmu = SingleDanmu(str(r), str(ip))
    danmuList.append(danmu)
    emit("danmu", {'id': danmu.id, 'data': danmu.value}, broadcast=True)
    # 通知管理员
    emit("AdmDanmu", {'id': str(danmu.id), 'data': danmu.value, 'ip': danmu.senderIp}, room="Adm", broadcast=True)
    return 200


@socketio.on('ban')
def newban(data):
    if Main.Check():
        # toekn合法即有权限
        if type(data) == dict:
            print("封禁ip", data['ip'])
            b = ban(data['ip'])
            blackList.append(b)
            banListChange(b)
            return 200
        else:
            for mess in danmuList:
                if mess.id == data:
                    print("封禁ip", mess.senderIp)
                    b = ban(mess.senderIp)
                    blackList.append(b)
                    banListChange(b)
                    return 200
    return 404


def banListChange(ip):
    timeStamp = time.localtime(float(ip.time / 1000))
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStamp)
    # timeStamp = time.localtime(float(ip.time / 1000)) + datetime.timedelta(minutes=10)
    # endTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStamp)
    emit("banListChange", {"ip": ip.ip,
                           "startTime": startTime,
                           "endTime":  str(config.banTime) + "分钟后"
                           }, room="Adm", broadcast=True)


def changingInwatcher():
    emit('watchersNum', str(OnlineWatchers), broadcast=True)


@socketio.on('connect')
def connect():
    global OnlineWatchers
    # 连接成功，在线人数+1
    OnlineWatchers += 1
    changingInwatcher()


@socketio.on('disconnect')
def disconnect():
    global OnlineWatchers
    # 连接断开
    OnlineWatchers -= 1
    changingInwatcher()


@socketio.on("Adm")
def Adm(res):
    global OnlineWatchers
    if Main.Check(user=res["user"], timel=res["time"], token=res["token"]):
        OnlineWatchers -= 1
        changingInwatcher()
        # 加入管理组
        join_room("Adm")
        print("新管理员登录")
        return 200
    else:
        return 2333


@socketio.on('disconnect', namespace="Adm")
def Mdisconnect():
    # leave_room("Administer")
    print("管理员退出")


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
