import threading
import config
from Main import setup
from flask import Flask, request
from flask_socketio import SocketIO, emit
from gevent.pywsgi import WSGIServer
from flask_cors import CORS, cross_origin

from danmuServer import SocketStart

app = Flask(__name__)
inLive = 0
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = "SECKEY"


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


if __name__ == '__main__':
    threading.Thread(target=setup).start()
    threading.Thread(target=SocketStart).start()
    print("协同服务端启动在", config.LiveStatePort)
    http_server = WSGIServer(('127.0.0.1', config.LiveStatePort), app)
    http_server.serve_forever()
    # socketio.run(app, host=config.ip, port=config.LiveStatePort)
