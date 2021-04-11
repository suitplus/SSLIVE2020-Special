var socket;
$(document).ready(function() {
	//必须要wss
	socket = io('//' + document.domain + ':' + DanmuPort, {
		path: '/socket.io',
		transports: ['websocket']
	});
	socket.emit("Adm",{'token': $.cookie("token"), 'user': $.cookie("user"), 'time': $.cookie("time")}, function(res){
		if(res == 2333){
			// token无效
		}else{
			console.info("进入管理员组");
		}
	});
	socket.on('banListChange', function (res) {
		$("#blackList").prepend("<div>ip: " + res['ip'] + " 开始时间: " + res['startTime'] + " 结束时间: " + res['endTime'] + " </div><br/>")
	})
	socket.on('AdmDanmu', function(res) {
		//res表示接收的数据，这里做数据的处理
		if($("#" + res["id"]).length > 0){
			document.getElementById(res["ip"]).parentNode.removeChild(document.getElementById(res["ip"]));
		}
		$("#danmuList").prepend("<div id='" + res["id"] + "'>"+"id: " + res["id"] + " 内容: " + res['data'] + " ip: " + res['ip']+"<div><br/>" +
			"<button onclick=\"ban('" + res["ip"] + "')\">封禁</button>");
	});
	socket.on('AdmDanmuD', function (res) {
		if($("#" + res).length > 0){
			document.getElementById(res).parentNode.removeChild(document.getElementById(res));
		}
	})
	socket.on('connect', function() {
		console.info("连接弹幕服务器成功");
	});
});
function refresh(){
	socket.emit("reFreshBanList", "");
}
function ban(res) {
	socket.emit("ban", {'ip':res, 'method': "ip"},function(ress){
		if(ress == 200){
			alert("禁言成功");
		}
		else if(ress == 404){
			alert("请先登录");
			window.location.href = "#";
		}
	});
}
