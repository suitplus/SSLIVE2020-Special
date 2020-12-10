// console.js
function logOut() {
	//登出
	//取消这3个cookie，通过把过期设为-1
	$.cookie('user', "", {
		expires: -1,
		path: '/'
	});
	$.cookie('time', "", {
		expires: -1,
		path: '/'
	});
	$.cookie('token', "", {
		expires: -1,
		path: '/'
	});
	location.reload();
}
function clear_cache(){
	$.ajax({
		url: "/cache_clear",
		method: "GET",
		data: {},
		success: function(data) {
			$("#cache_tip").text("成功");
		}
	});
}
function changelive() {
	$.ajax({
		url: "/livestart",
		method: "POST",
		data: {},
		success: function(data) {
			inLive = (inLive == 1 ? 0 : 1);
			if (data == "success") {
				if (inLive == 1) {
					$("#LiveControlButton").text("停 止直 播");
					$("#LiveStatusReminder").css("visibility", "visible");
				} else {
					$("#LiveControlButton").text("开 始 直 播");
					$("#LiveStatusReminder").css("visibility", "hidden");
				}
			}
		}
	});
}
