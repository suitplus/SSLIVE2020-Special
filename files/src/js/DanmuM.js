var socket;
$(document).ready(function() {
	//必须要wss
	socket = io('//' + document.domain + ':' + DanmuPort, {
		path: '/socket.io/Adm',
		transports: ['websocket']
	});
	socket.on('connect', function() {
		console.info("连接弹幕服务器成功")
	});
});
