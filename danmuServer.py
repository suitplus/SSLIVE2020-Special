# 官方文档 https://flask-socketio.readthedocs.io/en/latest/
import Main
import config
from flask import Flask
from flask_socketio import SocketIO, emit
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
    return 200


@socketio.on('ban')
def ban(data):
    if Main.Check():
        # toekn合法即有权限
        for mess in danmuList:
            if mess.id == data:
                print("封禁ip", mess.senderIp)
                b = ban(mess.senderIp)
                blackList.append(b)
        return 200
    else:
        return 404


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


@socketio.on('connect', namespace="Adm")
def Mconnect():
    if Main.Check():
        print("管理员登录")
    else:
        ConnectionRefusedError('authentication failed')


@socketio.on('ban', namespace="Adm")
def Mban(data):
    # toekn合法即有权限
    # data 应该是 {'data': ip或弹幕id, 'type': '1'=弹幕id '2'=ip}
    d = data.get("data")
    t = data.get("ip")
    if t == "1":
        for mess in danmuList:
            if mess.id == d:
                print("封禁ip", mess.senderIp)
                b = ban(mess.senderIp)
                blackList.append(b)
    if t == "2":
        b = ban(d)
        blackList.append(b)


@socketio.on('disconnect', namespace="Adm")
def Mdisconnect():
    print("管理员接入")


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
