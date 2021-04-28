# 网站配置文件
import hashlib

# 账号密码字典集
import os

password = {"suit": "lovesuit"}
# cookie加密用，字符key，更改会使之前用这个key加密的cookies失效
random_chars = "fsajfsjhs"
# 静态文件缓存时间，[day,hour,minutes] 12
cache_time = [0, 12, 0]
# 缓存过期时间，秒为单位 300
cache_out_time = 300
# root folder网址根目录文件夹名称
root = "../fontend/www"
# static_folder静态文件(css,js,img...)文件夹名称
static_root = "../fontend/files"
# static url root静态文件网页引用地址
static_url_root = "/files"
# cookies有效期，天为单位
cookies_time = 7
# flask_cache缓存类型
cache_type = "simple"
# 映射ip，如果放在服务器给外网要填0.0.0.0(局域网)，本地调试127.0.0.1即可，或者搭配nginx用，nginx监听外网，反向代理到127.0.0.1(现在就是这种模式)
ip = "127.0.0.1"
# 映射端口,和nginx的反向代理相同
port = [8080, 9090, 888, 99, 999, 8899, 8889, 9999]
Authorities = [True, True, True]
# 协同服务器端口s
LiveStatePort = 555
# 弹幕服务器启动端口
Danmu_SocketPort = 90
# 弹幕服务器外显端口
Danmu_showPort = 91
# 分钟为单位
banTime = 5
# 弹幕中需替换词，用|分割
sensitive_words = "sb|cnm|nmsl"
ssl_crt = os.path.split(os.path.realpath(__file__))[0] + "\\SSL\\ssersay.cn_chain.crt"
ssl_key = os.path.split(os.path.realpath(__file__))[0] + "\\SSL\\ssersay.cn_key.key"


def md5(a):
    # md5 加密
    return hashlib.md5(a.encode(encoding="UTF-8")).hexdigest()


# cookies中token加密算法
# rkey - 随机数key
# user - 用户名
# rchar - 管理员自定义字符key
# pw - 密码
# timel - 时间戳
def encryption(rkey, user, timel):
    rchar = random_chars
    pw = password.get(user)
    return rkey + md5(rkey + user + rchar + pw + timel)
