// live.js
var player;
var isplay = false;
var lastRunTime=new Date().getTime();//初始化保护的时间
var protectTime=1000;//设置保护性延时 单位毫秒，不要小于50 建议100以上，1000是1s

function hide() {
    $("#tips_chip").hide();
}

//var isdanmu = true;

function danmu_submit() {
    send_danmu($('#danmu-sender-input').val(), "white", 0, 0);
    $('#danmu-sender-input').val("");
}
// 加载播放器
function load() {
    resize();
    player = videojs('video', {
        liveui: true,
        controls: true,
        preload: true, // 预加载
        poster: "/files/src/img/background/newintro.jpg", // 预览图
        fullscreen: { options: { navigationUI: 'show' } },
        },
        function onPlayerReady() {
            // videojs.log('Your player is ready!');
            //
            // this.on("loadstart", function () {
            //     console.log("开始请求数据 ");
            // })
            // this.on("progress", function () {
            //     console.log("正在请求数据 ");
            // })
            // this.on("loadedmetadata", function () {
            //     console.log("获取资源长度完成 ")
            // })
            // this.on("canplaythrough", function () {
            //     console.log("视频源数据加载完成")
            // })
            // this.on("waiting", function () {
            //     console.log("等待数据")
            // });
            this.on("play", function () {
                //console.log("视频开始播放")
                player.play();
                $('#play').css('background-image', "url('/files/src/img/control/pause.svg')");
                isplay = true;
            });
            // this.on("playing", function () {
            //     //console.log("视频播放中")
            // });
            this.on("pause", function () {
                // console.log("视频暂停播放")
                player.pause();
                $('#play').css('background-image', "url('/files/src/img/control/play.svg')");
                isplay = false;
            });
            // this.on("ended", function () {
            //     console.log("视频播放结束");
            // });
            this.on("error", function () {
                console.log("加载错误")
            });
            // this.on("seeking", function () {
            //     console.log("视频跳转中");
            // })
            // this.on("seeked", function () {
            //     console.log("视频跳转结束");
            // })
            // this.on("ratechange", function () {
            //     console.log("播放速率改变")
            // });
            // this.on("timeupdate", function () {
            //     console.log("播放时长改变");
            // })
            // this.on("volumechange", function () {
            //     console.log("音量改变");
            // });
            this.on("stalled", function () {
                console.log("网速异常");
            });
        });
    //地址 http://suit.ssersay.cn/AppName/StreamName.m3u8?auth_key={鉴权串}
    player.src("https://suit.ssersay.cn/SUIT/stream.m3u8");//直播地址
	//连接CCTV-1测试http://ivi.bupt.edu.cn/hls/cctv1.m3u8
    // 推流地址 rtmp://push.ssersay.cn/Live/Living
	document.onkeydown = function() {
	    //回车提交
	    if (event.keyCode == 32) {
	        $('#play').click();
	    }
	}
	$('#play').css('background-image', "url('/files/src/img/control/play.svg')");
    $('#play').click(function () {
		var currentTime=new Date().getTime();
		if((currentTime-lastRunTime)<protectTime){
			return;//两次执行太过频繁，直接退出
		}
		lastRunTime=new Date().getTime();
        if (isplay) {
            player.pause();
            $('#play').css('background-image', "url('/files/src/img/control/play.svg')");
            isplay = false;
        } else {
            player.play();
            $('#play').css('background-image', "url('/files/src/img/control/pause.svg')");
            isplay = true;
        }
    });
    /*$('#danmuswitch').click(function () {
        if (isdanmu) {
            $('#danmu').danmu("setOpacity", 0);
            $('#danmuswitch').css('background-image', "url('/files/src/img/danmu/off.svg')");
            isdanmu = false;
        } else {
            $('#danmu').danmu("setOpacity", 0.9);
            $('#danmuswitch').css('background-image', "url('/files/src/img/danmu/on.svg')");
            isdanmu = true;
        }
    })*/
    $('#fullscreen').click(function () {
        player.requestFullscreen();
    });
    /*$("#danmu-sender-input").bind("input propertychange", function (param) {
        if ($("#danmu-sender-input").val() != '') {
            $("#danmu-sender-button").unbind("click").click(danmu_submit).css("background-color", "#00a1d6")
        } else {
            $("#danmu-sender-button").unbind("click").css("background-color", "#005470");
        }
    });
    $("#danmu-sender-button").unbind("click").css("background-color", "#005470");
    growl.show({ text: "弹幕正在连接", type: "custom", imgsrc: "/files/src/img/growl/loading.gif" });
    // 在联通之后再展示弹幕发送组件
    $('#danmu-sender-container').css('display', 'none');
    // 建立websocket连接
    create_socket();
    // https://github.com/chiruom/jquery.danmu.js
    $("#danmu").danmu({
        //弹幕区宽度
        width: $("#video_html5_api").width(),
        //弹幕区高度
        height: $("#video_html5_api").height(),
        //弹幕区域z-index属性
        zindex: 10,
        //滚动弹幕的默认速度，这是数值指的是弹幕滚过每672像素所需要的时间（毫秒）
        speed: 7000 * (672 / 300),
        //小弹幕的字号大小
        fontSizeSmall: 1.5 * parseInt($('html').css('font-size')),
        //大弹幕的字号大小
        FontSizeBig: 2 * parseInt($('html').css('font-size')),
        //是否位置优化，位置优化是指像AB站那样弹幕主要漂浮于区域上半部分
        positionOptimize: true,
    });
    $('#danmu').danmu('danmuStart');*/
}

$('document').ready(load)
$(window).resize(resize)
