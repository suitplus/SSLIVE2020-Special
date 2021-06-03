# -*-coding: utf-8 -*-
# 弹幕服务器
# scoketio(wss)官方文档 https://flask-socketio.readthedocs.io/en/latest/
import Main
import config
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import time
import WordsSearch


# 每一个被禁言的ip
class ban:
    # 目标ip
    ip = ""
    # 禁言开始时间
    time = 0

    def isIp(self, ip):
        # Is Same
        return self.ip == ip

    def __init__(self, ip):
        # 创建一个被禁言ip
        self.ip = ip
        self.time = int(round(time.time() * 1000))

    def isOut(self):
        # 是否超时(即是否失效
        return ((int(round(time.time() * 1000)) - self.time) / 60000.00) >= config.banTime


class SingleDanmu:
    # 内容
    value = ""
    # 创建时间
    time = 0
    # 弹幕编号
    id = 0
    # 发送者ip(用于禁言
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
# 初始化替换 https://github.com/toolgood/ToolGood.Words/tree/master/python
search = WordsSearch.WordsSearch()
search.SetKeywords(config.sensitive_words.split('|'))


# 刷新禁言名单
@socketio.on("reFreshBanList")
def refresh():
    global blackList
    for a in blackList:
        # 如果到时间就从黑名单去除
        if a.isOut():
            emit("AdmDanmuD", a.ip)
            blackList.remove(a)


@socketio.on('new_danmu')
def adding(data):
    global search
    global OnlineWatchers
    global blackList
    # 从post请求取弹幕内容
    r = data.get("text")
    # 从请求头获取nginx转发的时候增加的X-Real_IP字段(为该用户ip
    ip = request.headers['X-Real-IP']
    for bip in blackList:
        if bip.isIp(ip):
            # 是否在黑名单
            if bip.isOut():
                # 是否超出封禁时间
                emit("AdmDanmuD", bip)
                blackList.remove(bip)
            else:
                return "ban"
    # 禁发网址
    # pattern = re.compile(r'[a-zA-z]+:[^\s]*/[^\s]*/[^\s]*')
    # if pattern.search(r) is not None:
    #    return 301
    print("新建弹幕", r)
    # 执行替换
    r = search.Replace(r, "*")
    print("替换后", r)
    # 加入历史弹幕集
    danmu = SingleDanmu(str(r), str(ip))
    danmuList.append(danmu)
    emit("danmu", {'id': danmu.id, 'data': danmu.value}, broadcast=True)
    # 通知管理员
    emit("AdmDanmu", {'id': str(danmu.id), 'data': danmu.value, 'ip': danmu.senderIp}, room="Adm", broadcast=True)
    return 200


@socketio.on('ban')
def newban(data):
    # 从cookie判断token合法,即管理员权限
    if Main.Check():
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


# 广播以同步blacklist
def banListChange(ip):
    timeStamp = time.localtime(float(ip.time / 1000))
    startTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStamp)
    timeStamp = time.localtime(float((ip.time + 10 * 60000) / 1000))
    endTime = time.strftime("%Y-%m-%d %H:%M:%S", timeStamp)
    emit("banListChange", {"ip": ip.ip,
                           "startTime": startTime,
                           "endTime": endTime
                           }, room="Adm", broadcast=True)


# 当前在看人数
def changingInwatcher():
    emit('watchersNum', str(OnlineWatchers), broadcast=True)


# 连接弹幕系统事件
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


# 管理员连接
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
                 certfile=config.ssl_crt, keyfile=config.ssl_key)
