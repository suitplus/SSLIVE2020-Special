# coding: utf-8
from flask import Flask, render_template, request, make_response
import hashlib
import random
import time

# Flask实例
app = Flask(__name__, template_folder="www", static_folder='files', static_url_path="/files")
# 直播状态
inLive = 0
# 账号密码字典
password = {"suit": "lovesuit", "a": "b"}
# 字符key
random_chars = "fsajfsjhs"


# 路径对应的执行函数，有路径就对应路径名，没路径就对应index
# 如@app.route('/login') 对应def login()
@app.route('/')
def index():
    # 首页判断
    global inLive
    if inLive == 0:
        return render_template('introduction.html', inLive=inLive)
    else:
        return live()


@app.route('/linence')
def linence():
    # 授权
    return render_template('linence.html')


@app.route('/robots.txt')
def robots():
    # 爬虫文件
    return render_template('robots.txt')


@app.route('/about')
def about():
    # 关于我们页面
    global inLive
    return render_template('about.html', inLive=inLive)


@app.route('/IE')
def IE():
    # IE提示页面
    return render_template('IE.html')


@app.route('/live')
def live():
    # 直播页面
    return render_template('live.html')


@app.route('/admin')
def console():
    # 管理路径
    global inLive
    if not Check():
        # 进入登录页面
        return render_template('login.html')
    return render_template('console.html', inLive=inLive)


@app.route('/livestart', methods=['POST'])
def livestart():
    global inLive
    if not Check():
        # 防止在没token的情况开启直播
        return "Cookies 失效"
    if inLive == 0:
        inLive = 1
    else:
        inLive = 0
    return "success"


@app.route('/login', methods=['POST'])
def login():
    # 取前端传值
    pw = request.form.get("PW", str)
    # 循环字典
    for b in password.keys():
        # 取密码
        c = password.get(b)
        # 验证字典
        if pw == md5(b + "#" + c):
            res = make_response("success") # cookies 实例
            timel = str(time.time()) # 取现在时间
            max_s = 60 * 60 * 60 * 24 * 7  # 有效期7天
            # 保存cookies
            res.set_cookie("user", b, max_age=max_s)
            res.set_cookie("token", Check(1, b, timel), max_age=max_s)
            res.set_cookie("time", timel, max_age=max_s)
            return "success"
    return "你来了不该来的地方"


def md5(a):
    # md5 加密
    return hashlib.md5(a.encode(encoding="UTF-8")).hexdigest()


def Check(a=0, user="", timel=""):
    # 验证token
    global password
    # 用户名不在集
    if user not in password.keys():
        return False
    if a == 0:
        user = request.cookies.get('user')
        timel = request.cookies.get('time')
        token = request.cookies.get('token')
        if int(time.time()) - int(timel) < 0:
            # 建立时间比现在还未来
            return False
        if (int(time.time()) - int(timel)) / 86400000 > 7:
            return False
        key = token[0:3]
        return key + md5(key + user + random_chars + password.get(user) + timel) == token
    elif a == 1:
        rkey = str(random.randint(100, 999))
        return rkey + md5(rkey + user + random_chars + password.get(user) + timel)
    else:
        # a不正常
        return False


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)  # 映射
