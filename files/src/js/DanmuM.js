var socket;
$(document).ready(function() {
	//必须要wss
	socket = io('//' + document.domain + ':' + DanmuPort, {
		path: '/socket.io/Adm',
		transports: ['websocket']
	});
	socket.on('AdmDanmu', function(res) {
		//res表示接收的数据，这里做数据的处理
		var DL = document.getElementById("danmuList");
		var C = document.createElement("div");
		var b = document.createElement("br");
		C.innerText = "id: " + res["id"] + " 内容: " + res['data'] + " ip: " + res['ip'];
		DL.appendChild(C);
		DL.appendChild(b);
	});
	socket.on('connect', function() {
		console.info("连接弹幕服务器成功")
	});
});
