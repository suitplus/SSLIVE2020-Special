# coding: utf-8
from datetime import timedelta
import config
from flask_cache import Cache
from flask import Flask, render_template, request, make_response
import random
import time

# flask可参考: https://blog.csdn.net/qq_40832960/article/details/107132488
cache = Cache()
# Flask实例
app = Flask(__name__, template_folder=config.root, static_folder=config.static_root,
            static_url_path=config.static_url_root)
# 缓存初始化
cache.init_app(app, config={'CACHE_TYPE': config.cache_type, 'CACHE_DEFAULT_TIMEOUT': config.cache_out_time})
# 设置静态文件缓存时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(days=config.cache_time[0], hours=config.cache_time[1],
                                                    minutes=config.cache_time[2])


# 路径对应的执行函数，有路径就对应路径名，没路径就对应index
# 如@app.route('/login') 对应def login()
@app.route('/')
@cache.cached()
def index():
    # 首页判断
    if config.inLive == 0:
        return render_template('introduction.html', inLive=config.inLive)
    else:
        # 跳转到直播
        return live()


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
    return render_template('about.html', inLive=config.inLive)


@app.route('/IE')
@cache.cached()
def IE():
    # IE提示页面
    return render_template('IE.html')


@app.route('/live')
@cache.cached()
def live():
    # 直播页面
    return render_template('live.html')


@app.route('/admin')
@cache.cached()
def console():
    # 管理路径
    if not Check():
        # 进入登录页面
        return render_template('login.html')
    else:
        return render_template('console.html', inLive=config.inLive)


@app.route('/introduction')
@cache.cached()
def introduction():
    return render_template("introduction.html", inLive=config.inLive)


# 开启直播路径，接受post
@app.route('/livestart', methods=['POST'])
@cache.cached()
def liveStart():
    if not Check():
        # 防止在没token的情况开启直播
        return "Cookies 失效"
    # 更改直播状态
    if config.inLive == 0:
        config.inLive = 1
    else:
        config.inLive = 0
    return "success"


@app.route('/login', methods=['POST'])
@cache.cached()
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


def Check(a=0, user="", timel=""):
    # 验证token
    if a == 0:
        user = request.cookies.get('user')
        timel = request.cookies.get('time')
        token = request.cookies.get('token')
        # 用户名不在集
        if user not in config.password.keys():
            return False
        if (float(time.time()) - float(timel)) < 0:
            # 建立时间比现在还未来
            return False
        if (float(time.time()) - float(timel)) / 86400000 > config.cookies_time:
            # 过期
            return False
        # 随机数key
        key = token[0:3]
        return config.encryption(key, user, timel) == token
    elif a == 1:
        rkey = str(random.randint(100, 999))
        return config.encryption(rkey, user, timel)
    else:
        # a不正常
        return False


if __name__ == '__main__':
    app.run(host=config.ip, port=config.port, debug=True)  # 映射
