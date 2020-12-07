# coding: utf-8

# gevent
from gevent import monkey

monkey.patch_all()
from gevent.pywsgi import WSGIServer

from datetime import timedelta
import config
from flask_cache import Cache
from flask import Flask, render_template, request, make_response, redirect
import random
import time
import requests

from flask_cors import CORS, cross_origin

# flask可参考: https://blog.csdn.net/qq_40832960/article/details/107132488
cache = Cache()
# Flask实例
app = Flask(__name__, template_folder=config.root, static_folder=config.static_root,
            static_url_path=config.static_url_root)
CORS(app, resources={r"/*": {"origins": "*"}})  # 如果要解决跨域就用这个
# 缓存初始化
cache.init_app(app, config={'CACHE_TYPE': config.cache_type, 'CACHE_DEFAULT_TIMEOUT': config.cache_out_time})
# 设置静态文件缓存时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(days=config.cache_time[0], hours=config.cache_time[1],
                                                    minutes=config.cache_time[2])
app.config['threaded'] = True
app.config['SECRET_KEY'] = "SECKEY"


# 路径对应的执行函数，有路径就对应路径名，没路径就对应index
# 如@app.route('/login') 对应def login()
@app.route('/')
# @cache.cached()
def index():
    # 首页判断
    if GetLiveState() == 1:
        # 跳转到直播
        return live()
    else:
        return render_template('introduction.html', inLive=GetLiveState())


@app.route('/license')
@cache.cached()
def license_page():
    # 授权
    return render_template('license.html')


@app.route('/robots.txt')
@cache.cached()
def robots():
    # 爬虫文件
    return render_template('robots.txt')


@app.route('/about')
@cache.cached()
def about():
    # 关于我们页面
    return render_template('about.html', inLive=GetLiveState())


@app.route('/IE')
@cache.cached()
def IE():
    # IE提示页面
    return render_template('IE.html')


# 下面两行调试的时候加，非调试在正式情况下最好去掉
@app.route('/live')
@cross_origin()
@cache.cached()
def live():
    # 直播页面
    return render_template('live.html', port=config.LiveStatePort)


@app.route('/admin')
# @cache.cached()
def admin():
    # 管理路径
    if not Check():
        # 进入登录页面
        return render_template('login.html')
    else:
        return render_template('console.html', inLive=GetLiveState())


@app.route('/introduction')
@cache.cached()
def introduction():
    return render_template("introduction.html", inLive=GetLiveState())


# 开启直播路径，接受post
@app.route('/livestart', methods=['POST'])
# @cache.cached()
def liveStart():
    if not Check():
        # 防止在没token的情况开启直播
        return "Cookies 失效"
    ChangeLiveState()
    return "success"


@app.route('/cache_clear')
def cacheclear():
    # 清楚缓存
    cache.clear()
    return "finish"


@app.before_request
def before_request():
    # return redirect(bilbil直播间网址,code=301) # 紧急跳转，或在nginx加301跳转
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)


@app.route('/login', methods=['POST'])
# @cache.cached()
def login():
    # 取前端传值
    pw = request.form.get("PW", "null", str)
    if pw == "null":
        return False
    # 循环字典
    for b in config.password.keys():
        # 取密码
        c = config.password.get(b)
        # 验证字典
        if pw == config.md5(b + "#" + c):
            res = make_response("success")  # cookies 实例
            timel = str(time.time())  # 取现在时间
            max_s = 60 * 60 * 24 * config.cookies_time  # 设置有效期，秒为单位
            # 保存cookies
            res.set_cookie("user", b, max_age=max_s)
            res.set_cookie("token", Check(1, b, timel), max_age=max_s)
            res.set_cookie("time", timel, max_age=max_s)
            return res
    return "你来了不该来的地方"


def Check(a=0, user="Fnull", timel="Fnull"):
    # 验证token
    if a == 0:
        token = ""
        if (user == "Fnull") and (timel == "Fnull"):
            user = request.cookies.get("user", default="null", type=str)
            timel = request.cookies.get("time", default="null", type=str)
            token = request.cookies.get('token', default="null", type=str)
            # 参数为空
            if user == "null" or timel == "null" or token == "null":
                return False
        # 用户名不在集
        if user not in config.password.keys():
            print("用户名非法")
            return False
        if (float(time.time()) - float(timel)) < 0:
            # 建立时间比现在还未来
            print("时间戳非法")
            return False
        if (float(time.time()) - float(timel)) / 86400000 > config.cookies_time:
            # 过期
            print("时间戳非法")
            return False
        # 随机数key
        key = token[0:3]
        v = config.encryption(key, user, timel) == token
        if not v:
            print("token非法")
        return v
    elif a == 1:
        rkey = str(random.randint(100, 999))
        return config.encryption(rkey, user, timel)
    else:
        # a不正常
        print("a参数非法")
        return False


# 同時支持httph和https方案
import threading


def startEach(ip, port):
    https_server = WSGIServer((ip, port), app, certfile="SSL/4837013_www.ssersay.cn.pem",
                              keyfile="SSL/4837013_www.ssersay.cn.key", spawn=200)
    print("https server start")
    https_server.serve_forever()


def GetLiveState():
    url = "http://127.0.0.1:" + str(config.LiveStatePort)
    data = {"type": "G"}
    res = requests.post(url=url, data=data)
    return int(res.text)


def ChangeLiveState():
    url = "http://127.0.0.1:" + str(config.LiveStatePort)
    data = {"type": "C"}
    requests.post(url=url, data=data)
    return ""


def setup():
    # app.run(host=config.ip, port=config.port, debug=True, ssl_context=("SSL/4837013_www.ssersay.cn.pem",
    #                                                                    "SSL/4837013_www.ssersay.cn.key"))  # 映射
    # 同時支持httph和https方案
    # t1 = threading.Thread(target=start, args=(config.ip, config.http_port, False)) # 80也就是http端口監聽
    # t2 = threading.Thread(target=start, args=(config.ip, config.https_port, True))
    # t1.start()
    # t2.start()
    # print("Start servers")
    # http_server = WSGIServer((config.ip, 80), dapp)
    # http_server.serve_forever()
    for port in config.port:
        t = threading.Thread(target=startEach, args=(config.ip, port))
        t.start()
        print("Server start in ", config.ip, ":", port)
    print("all server start")
