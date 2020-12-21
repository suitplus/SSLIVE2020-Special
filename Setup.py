# -*- coding: utf-8 -*-
# @Time: 2020/12/20
# @Author: Eritque arcus
# @File: Setup.py
# 启动器-暂停使用
import os.path as ph
import threading
import time
import curl
import importlib

MainTs = []
Threads = []
WSGI = []
WSGIState = False
MainState = False
WSGILock = threading.RLock()
MainLock = threading.RLock()


def exitSystem(code=0, place=""):
    global threads

    if code != 0:
        print("\n --- \n 从", place, "退出 \n ---")
    exit(code)


def getStateServerAndDanmu():
    global threads
    print("[I]:获取协同服务器和弹幕服务器状态")
    print("[I]:协同服务器状态:", threads[1].isAlive())
    print("[I]:弹幕服务器状态:", threads[2].isAlive())
    print("[I]:结束")


def getServerPars(P):
    global WSGILock
    global WSGI
    WSGI.append(P)
    WSGILock.release()


def setupServerAndDanmu():
    global WSGILock
    global WSGIState
    global threads
    WSGIState = True
    WSGILock.acquire()
    print("[I]:启动协同服务器和弹幕服务器")
    for i in range(0, 2):
        threads[1 + i].start()
    print("[I]:结束")


def reopenServerAndDanmu():
    global WSGIState
    global WSGI
    if WSGIState:
        return "X"
    WSGIState = True
    for i in WSGI:
        i.start()
        return "Y"


def closeServerAndDanmu():
    global WSGIState
    global WSGI
    if not WSGIState:
        return "X"
    WSGIState = False
    for i in WSGI:
        i.stop()
        return "Y"


def reopenMain():
    global MainState
    global MainTs
    [a, b, c] = MainTs
    if MainState:
        return "X"
    MainState = True
    for i in c:
        i.start()
        return "Y"


def closeMain():
    global MainState
    global MainTs
    [a, b, c] = MainTs
    if not MainState:
        return "X"
    MainState = False
    for i in c:
        i.stop()
        return "Y"


def getStateMain():
    global MainTs
    global MainState
    print(MainTs)
    print("[I]:获取主后台状态")
    [f, s, g] = MainTs
    for i in range(len(s)):
        print("[I]:主后台在", s[i], "状态:", f[i].isAlive())
    MainState = True
    print("[I]:结束")


def setupMain():
    global threads
    print("[I]:启动主后台")
    threads[0].start()
    print("[I]:结束")
    threads[0].join(1)
    MainLock.acquire()


def getMainPars(P):
    global MainTs
    MainTs = P
    print(MainTs)
    MainLock.release()


def procession():
    while 1:
        print("菜单",
              "\n0. 退出",
              "\n1. 获取协同服务器和弹幕服务器线程状态",
              "\n2. 获取主后台服务器线程状态",
              "\n3. 开启协同服务器和弹幕服务器",
              "\n4. 开启主后台",
              "\n5. 关闭协同服务器和弹幕服务器",
              "\n6. 关闭主后台")
        c = str(input("输入数字序号:"))
        if c == "0":
            exitSystem()
        elif c == "1":
            getStateServerAndDanmu()
        elif c == "2":
            getStateMain()
        elif c == "3":
            if reopenServerAndDanmu() == "X":
                print("[W]: 弹幕和协同服务器已开启")
        elif c == "4":
            if reopenMain() == "X":
                print("[W]: 主后台服务器已开启")
        elif c == "5":
            if closeServerAndDanmu() == "X":
                print("[W]: 协同和弹幕服务器已关闭")
        elif c == "6":
            if closeMain() == "X":
                print("[W]: 主后台已关闭")
        elif c == "7":
            print(curl.Curl("127.0.0.1:99"))
        time.sleep(2)


if __name__ == '__main__':
    print("[I]:检查配置文件")
    p = "config.py"
    if not ph.exists(p):
        print("\n[E]: 配置文件:", p, "不存在")
        exitSystem(1, "检查配置文件")
    # 动态引入配置文件模块
    config = __import__("config")
    print("[I]:结束")
    start = time.perf_counter()
    scale = len(config.keyPaths)
    print("[I]:检查关键位置".center(scale // 2, "-"))
    for i in range(scale + 1):
        a = "*" * i
        b = "." * (scale - i)
        c = (i / scale) * 100
        dur = time.perf_counter() - start
        print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end="")
        if i < scale:
            if not ph.exists(config.keyPaths[i]):
                print("\n[E]: 目录或文件:", config.keyPaths[i], "不存在")
                exitSystem(1, "检测关键位置")
    print("\n[I]:结束")
    module = ["Main", "Server", "danmuServer"]
    start = time.perf_counter()
    scale = len(module)
    print("[I]:取关键线程".center(scale // 2, "-"))
    threads = []
    for i in module:
        t = threading.Thread(target=__import__(i).setup)
        t.setDaemon(True)
        threads.append(t)
    print("[I]:结束")
    setupServerAndDanmu()
    WSGILock.acquire()
    WSGILock.release()
    getStateServerAndDanmu()
    setupMain()
    MainLock.acquire()
    MainLock.release()
    getStateMain()
    threading.Thread(target=procession).start()
