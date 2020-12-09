var barrageWidth;
var barrageHeight;
$(window).resize(function() {
	barrageWidth = $(".barrage-container-wrap").width();
	barrageHeight = $(".barrage-container-wrap").height();
});
// 参考 https://blog.csdn.net/qq_32849999/article/details/81031234
var barrageColorArray = [
	'#fff'
];
var barrageTipWidth = 50; //提示语的长度
var videoHeigh = ~~window.getComputedStyle(document.querySelector("#video-container")).width.replace('px', '');
var barrageBoxWrap = document.querySelector('.barrage-container-wrap');
var barrageBox = document.querySelector('.barrage-container');
var inputBox = document.querySelector('.input');
var sendBtn = document.querySelector('.send-btn');

//容器的宽高度
barrageWidth = $(".barrage-container-wrap").width();
barrageHeight = $(".barrage-container-wrap").height();

//发送
function sendMsg() {
	var inputValue = inputBox.value;
	inputValue.replace(/\ +/g, "");

	if (inputValue.length <= 0) {
		alert('请输入');
		return "Nullandnull";
	}

	return inputValue;
}


//创建弹幕
function createBarrage(msg, isSendMsg) {
	var divNode = document.createElement('div');
	var spanNode = document.createElement('span');

	divNode.innerHTML = msg;
	divNode.classList.add('barrage-item');
	barrageBox.appendChild(divNode);

	spanNode.innerHTML = '举报';
	spanNode.classList.add('barrage-tip');
	divNode.appendChild(spanNode);

	var barrageOffsetLeft = getRandom(barrageWidth, barrageWidth * 2);
	barrageOffsetLeft = isSendMsg ? barrageWidth : barrageOffsetLeft
	var barrageOffsetTop = (getRandom(0, barrageHeight) - 10) / 4;
	var barrageColor = barrageColorArray[Math.floor(Math.random() * (barrageColorArray.length))];

	//执行初始化滚动
	initBarrage.call(divNode, {
		left: barrageOffsetLeft,
		top: barrageOffsetTop,
		color: barrageColor
	});
}

//初始化弹幕移动(速度，延迟)
function initBarrage(obj) {
	//初始化
	obj.top = obj.top || 0;
	obj.class = obj.color || '#fff';
	this.style.left = obj.left + 'px';
	this.style.top = obj.top + 'px';
	this.style.color = obj.color;

	//添加属性
	this.distance = 0;
	this.width = ~~window.getComputedStyle(this).width.replace('px', '');
	this.offsetLeft = obj.left;
	this.timer = null;

	//弹幕子节点
	var barrageChileNode = this.children[0];
	barrageChileNode.style.left = (this.width - barrageTipWidth) / 2 + 'px';

	//运动
	barrageAnimate(this);

	//停止
	this.onmouseenter = function() {
		barrageChileNode.style.display = 'block';
		cancelAnimationFrame(this.timer);
	};

	this.onmouseleave = function() {
		barrageChileNode.style.display = 'none';
		barrageAnimate(this);
	};

	//举报
	barrageChileNode.onclick = function() {
		alert('举报成功');
	}
}

//弹幕动画
function barrageAnimate(obj) {
	move(obj);

	if (Math.abs(obj.distance) < obj.width + obj.offsetLeft) {
		obj.timer = requestAnimationFrame(function() {
			barrageAnimate(obj);
		});
	} else {
		cancelAnimationFrame(obj.timer);
		//删除节点
		obj.parentNode.removeChild(obj);
	}
}

//移动
function move(obj) {
	obj.distance--;
	obj.style.transform = 'translateX(' + obj.distance + 'px)';
	obj.style.webkitTransform = 'translateX(' + obj.distance + 'px)';
}

//随机获取高度
function getRandom(start, end) {
	return (Math.random() * (end - start + 1) + start);
}


/*******初始化事件**********/
//点击发送
sendBtn.onclick = newDanmu; //点击发送

//回车
inputBox.onkeydown = function(e) {
	e = e || window.event;
	if (e.keyCode == 13) {
		newDanmu();
	}
}

function newDanmu() {
	r = sendMsg();
	if (r != "nullandnull") {
		inputBox.value = '';
		socket.emit("new_danmu", {
			"text": r
		});
	}
}

//兼容写法
(function() {
	var lastTime = 0;
	var vendors = ['webkit', 'moz'];
	for (var x = 0; x < vendors.length && !window.requestAnimationFrame; ++x) {
		window.requestAnimationFrame = window[vendors[x] + 'RequestAnimationFrame'];
		window.cancelAnimationFrame = window[vendors[x] + 'CancelAnimationFrame'] || // Webkit中此取消方法的名字变了
			window[vendors[x] + 'CancelRequestAnimationFrame'];
	}

	if (!window.requestAnimationFrame) {
		window.requestAnimationFrame = function(callback, element) {
			var currTime = new Date().getTime();
			var timeToCall = Math.max(0, 16.7 - (currTime - lastTime));
			var id = window.setTimeout(function() {
				callback(currTime + timeToCall);
			}, timeToCall);
			lastTime = currTime + timeToCall;
			return id;
		};
	}
	if (!window.cancelAnimationFrame) {
		window.cancelAnimationFrame = function(id) {
			clearTimeout(id);
		};
	}

}());
// 结束
var socket;
$(document).ready(function() {
	//必须要wss
	socket = io('//' + document.domain + ':' + DanmuPort, {
		// path: '/socket.io/new_danmu',
		transports: ['websocket']
	});
	socket.on('watchersNum', function (res) {
			// res是在线人数
	})
	socket.on('connect', function() {
		console.info("连接弹幕服务器成功")
	});
	socket.on('danmu', function(res) {
		//res表示接收的数据，这里做数据的处理
		createBarrage(res, true);
		//生成弹幕
	});

});
