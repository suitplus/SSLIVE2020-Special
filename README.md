# SSLIVE2020-Special
Use the python flask instead of PHP

使用(html + javascript + css)前端 + (flask + gevent)python后端 + (nginx)负载均衡和反向代理，替换单一的php做后端

原仓库(origin url): https://github.com/suitplus/SSLIVE2019/

---

The source code of SSLIVE website
Website Address: (http://ssersay.cn/) or (http://106.15.93.200/)

All the source code in this repository (EXCEPT FOR the code in mdl, src/lib/ and console/lib/ folder) is written by The Students Union Information Technology Section of Guangdong Experimental High School.

---

网站地址： (http://ssersay.cn/) 或 (http://106.15.93.200/)

所有的代码（除了 src/lib/, console/lib/以及mdl 文件夹里的代码）都由广东实验中学学生会信息部编写。

---

**Windows 启动方式**

`Win+R`进入cmd，在里面用cd进入/Win路径，然后`start nginx`

然后点开`/Win`下的`启动脚本.bat`，不要关掉这个窗口

如果报错说python没有什么库，比如`no module name xxx`，就用在cmd`pip install xxx`命令安装

**linux 启动方式**

先用搜索引擎上的教程装好nginx

然后把\Win\nginx-1.18.0\conf\nginx.conf里的配置复制到新的nginx里的nginx.conf里

然后装python,并用screen这个组件？打开一个新窗口

在里面先用cd进入到根目录，然后用python Server.py启动(就是`启动脚本.bat`里的代码)

如果报错说python没有什么库，比如`no module name xxx`，就用在cmd`pip install xxx`命令安装

然后退出screen的窗口，关于为什么用screen是因为我们要让这个窗口一直运行，而开始的窗口一旦退出就不会运行了


---

**可能的bugs的解决方法**

flask_cache cannot import 'import_string' -  https://www.cnblogs.com/gavinclc/p/9622095.html

flask_socketio 报错 unsupport client - 把前端js引用的socket.io.js从3.* 改成2.* 的版本

---

**contributor list:**

本项目贡献者名单:

1. Lin Sixing ([@LSX-s-Software](https://github.com/LSX-s-Software))
2. Zeng Wenyi ([@vincenttsang](https://github.com/vincenttsang))
3. Zeng Chengzhi
4. Wu Kai ([@wk2003](https://github.com/wk2003))
5. Jia Boyi ([@ap0stader](https://github.com/ap0stader))
6. Qiu Yiran ([@Nambers](https://github.com/Nambers))
7. Chen Qixuan ([@Asiimoviet](https://github.com/Asiimoviet))

---

**TODO**

 - [ ] 更换vue.js + go的解决方案，react JSX的可读性和易上手度可能会低一点，后端用node.js或ktor也可以，不过go比较轻便
 - [ ] 用bulma可以解决css适配
 - [ ] 后台管理页面优化
   - [x] 在弹幕管理后端显示黑名单解禁时间
   - [ ] 主后台页面管理优化(样式优化和下面的功能优化)
   - [ ] 增加仪表盘，比如在线人数，可以让管理员动态决定买流量，监控有没有人在爆破api接口，及时ban掉非法用户
   - [ ] 主后台增加Config.py里的变量管理控制
   - [ ] 优化实现弹幕管理后台页面
 - [ ] ~~体育节直播失败的原因~~
 - [ ] 直播页面优化
   - [x] 在live界面添加推荐使用chrome浏览器提示和b站跳转提示
   - [ ] 用户自定义显示的弹幕样式
   - [x] 直播页面弹幕右侧边栏
   - [ ] 直播页面控件优化
 - [ ] 弹幕系统优化
   - [ ] 优化前端弹幕css和js文件里不必要的代码
   - [x] 后端或前端筛选不规范（黄暴|敏感）弹幕，~~不予通过~~用*替换，以及不能发网址
   - [ ] 填充config.py下的sensitive_words变量
   - [ ] 用户自定义发送的弹幕样式
 - [ ] BBS?
 - [x] 弹幕功能(使用flask-socketio + socket.io.js)
   - [x] 统一的弹幕服务器
   - [x] 高逼格的简单小东西(在线用户数)
   - [x] 管理员禁言发送非法弹幕的用户(黑名单)
 - [x] 全部把php后端转到flask后端
   - [x] nginx + gevent 通过反向代理做"伪"负载均衡(多端口监听)
   - [x] 为解决负载均衡的多服务器做的协同服务器(主要协同直播状态)
 - [x] windows和linux适配
 - [ ] ~~统一的启动器及监控线程是否在运行以及随时管理~~(取消，因为本来想做个和宝塔差不多的后端服务器管理页面，但是python的thread多线程难搞，残留代码在根目录下的废弃的启动器源码，如果有谁愿意继续做也可~hhh)
 
---

项目树状目录
2020/12

```
│  config.py flask一部分配置文件
│  danmuServer.py 弹幕服务器文件
│  Main.py 主要flask启动文件
│  README.md
│  Server.py 协同服务器启动文件，也是整个项目启动文件
│  
│        
├─files 静态文件目录，url访问网址是'/files/'，在flask中设置
│  ├─config
│  │  └─coding
│  │          livestart.json 直播开始时间
│  │          livestop.json 直播停止时间
│  │          
│  ├─console
│  │  │  console.css 后端控制台主要css
│  │  │  console.js 后端控制台主要js
│  │  │  jquery.cookie.js jq的cookie库
│  │  │  
│  │  └─login
│  │      │  jquery.md5.js jq的md5加密库
│  │      │  
│  │      ├─css
│  │      │      loading.css 加载中动画css
│  │      │      main.css 登录页面主要css
│  │      │      
│  │      └─js 登录页面的js
│  │              
│  ├─mdl 应该是google的模块
│  │      
│  └─src
│      ├─css
│      │  ├─module 模块的css文件
│      │  │      
│      │  └─pages 每个页面独立的css文件
│      │          
│      ├─img
│      │  ├─about 关于我们页面里的图片
│      │  │      
│      │  ├─background 背景图
│      │  │      
│      │  ├─control 视频控制按钮图
│      │  │      
│      │  ├─growl
│      │  │      
│      │  ├─linence 授权页面里的商标图
│      │  │      
│      │  ├─logo logo图片
│      │  │      
│      │  └─textture
│      │          
│      ├─js 每个页面独立的js文件
│      │      
│      ├─lib 一些引用的第三方js文件
│      │      
│      └─util 一些杂七杂八的js文件
│              
├─SSL SSL证书
│      
├─Win
│  │  启动nginx.bat
│  │  启动脚本.bat
│  │  
│  └─nginx-1.18.0
│      │  nginx.exe nginx启动文件，常用命令(start nginx, nginx -s reload, nginx -s quit)
│      │  
│      ├─conf nginx配置文件
│      │      
│      ├─contrib nginx资源
│      │              
│      ├─docs nginx文档
│      │      
│      ├─html 默认文件
│      │      
│      ├─logs 日志
│      │      
│      └─temp 缓存
│              
├─www
│  │  about.html 关于我们html文件
│  │  console.html 后端控制台html 文件
│  │  DanmuManager.html 弹幕的控制台文件
│  │  IE.html IE用户引流文件
│  │  introduction.html 非直播状态下首页
│  │  license.html 授权文件
│  │  live.html 直播页面
│  │  login.html 登录页面
│  │  robots.txt 给机器人爬的
│  │  
│  └─module 模组html文件，flask用
│          Baidu.html  百度统计
│          footer.html 页脚
│          guiding.html 头部
│          guiding_intro.html 头部2，透明
│          review.html 以前的直播内容卡
│          
└─__pycache__ flask页面缓存文件夹
```
