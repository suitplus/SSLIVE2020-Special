import threading
from Main import setup
import config
from flask import Flask, request

app = Flask(__name__)
inLive = 0


@app.route('/', methods=['POST'])
def Server():
    global inLive
    r = request.form.get("type", default="null")
    if r == "null":
        return "2"
    else:
        if r == "C":
            if inLive == 0:
                inLive = 1
                print("更改直播状态到", inLive)
                return str(inLive)
            elif inLive == 1:
                inLive = 0
                print("更改直播状态到", inLive)
                return str(inLive)
        elif r == "G":
            return str(inLive)
        else:
            return "4"


def start():
    print("协同服务端启动在127.0.0.1:", config.LiveStatePort)
    app.run(host="127.0.0.1", port=config.LiveStatePort)


if __name__ == "__main__":
    t = threading.Thread(target=start)
    t.start()
    t1 = threading.Thread(target=setup)
    t1.start()
