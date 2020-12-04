var box;
var i;
var barrageWidth;
var defaultColor = "#000";
window.onload = function() {
	box = $("#box")[0];
	i = $("#input")[0];
	barrageWidth = box.clientWidth;
	barrageHeight = box.clientHeight;
}

function process(text) {
	var divNode = document.createElement('div');
	divNode.innerHTML = text;
	var barrageOffsetTop = getRandom(10, barrageHeight - 10);
	var barrageOffsetLeft = barrageWidth;
	divNode.classList.add("barrage-item");
	divNode.style.color = defaultColor;
	divNode.left = barrageOffsetLeft + 'px';
	divNode.top = barrageOffsetTop + 'px';
	box.append(divNode);
	//执行初始化滚动
	initBarrage(divNode);
}

//初始化弹幕移动
function initBarrage(obj) {
	//添加属性
	this.distance = 0;
	this.offset = barrageWidth;
	this.timer = null;

	//运动
	barrageAnimate(this, obj);

	//停止
	this.onmouseenter = function() {
		cancelAnimationFrame(this.timer);
	};

	this.onmouseleave = function() {
		barrageAnimate(this, obj);
	};
}

//弹幕动画
function barrageAnimate(obj, obj2) {

	move(obj, obj2);

	if (Math.abs(obj.distance) < obj.offset) {
		obj.timer = requestAnimationFrame(function() {
			barrageAnimate(obj, obj2);
		});
	} else {
		cancelAnimationFrame(obj.timer);
		//删除节点
		obj2.parentNode.removeChild(obj2);
	}
}

function send() {
	var temp = i.innerHTML;
	i.innerHTML = "";
	process(temp);
}

//随机
function getRandom(start, end) {
	return start + (Math.random() * (end - start));
}

//移动
function move(obj, obj2) {
	obj.distance = obj.distance - 1;
	obj2.style.transform = 'translateX(' + obj.distance + 'px)';
	obj2.style.webkitTransform = 'translateX(' + obj.distance + 'px)';
}
//兼容性
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
