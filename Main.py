# coding: utf-8
from flask import Flask, render_template

app = Flask(__name__, template_folder="www", static_folder='files', static_url_path="/files")
inLive = 0
startlive = "{\
    \"year\": 2020,\
    \"month\": 12,\
    \"day\": 3,\
    \"hour\": 0,\
    \"minute\": 0}"


# 路径对应的执行函数，有路径就对应路径名，没路径就对应index
# 如@app.route('/login') 对应def login()
@app.route('/')
def index():
    if not inLive:
        return render_template('introduction.html',inLive=inLive,startLive=startlive)
    else:
        return render_template('live.html')

@app.route('/about')
def about():
    return render_template('about.html', inLive=inLive,startLive=startlive)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)  # 映射
