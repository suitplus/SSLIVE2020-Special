function htmlSpecialChars(str)
//来源 https://www.cnblogs.com/web-leader/p/4742362.html  
{
	var s = "";
	if (str.length == 0) return "";
	for (var i = 0; i < str.length; i++) {
		switch (str.substr(i, 1)) {
			case "<":
				s += "&lt;";
				break;
			case ">":
				s += "&gt;";
				break;
			case "&":
				s += "&amp;";
				break;
			case " ":
				if (str.substr(i + 1, 1) == " ") {
					s += " &nbsp;";
					i++;
				} else s += " ";
				break;
			case "\"":
				s += "&quot;";
				break;
			case "\n":
				s += "<br>";
				break;
			default:
				s += str.substr(i, 1);
				break;
		}
	}
	return s;
}
document.onkeydown = function() {
	//回车提交
	if (event.keyCode == 13) {
		// $('#bu').click();
		submita();
	}
}

function showSB(msg) {
	var snackbartip = document.querySelector('#snackbar-tip');
	var data = {
		message: msg,
		timeout: 2000,
		actionText: 'Undo'

	};
	document.querySelector('#snackbar-tip').MaterialSnackbar.showSnackbar(data);

}
var T = false;
function valid(){
	T = true;

}
function submita() {
	if(T == false){
		alert("请通过人机验证");
		return false;
	}
	//显示加载特效
	//$('#loading').show();
	//用jq取值
	let username = $('#um').val();
	let password = $('#pd').val();
	//这里调用了用户输入，本应该进行安全排查替换，但是本处暂时没在php中用，所以就执行了简易的替换，希望注意用户输入，
	//本处可能出现的漏洞参考XSS跨站攻击，务必谨慎
	//其实因为下面有加密，此处的替换也可有可无了，但是以防止下面的if语句出现问题还是替换一下
	username = htmlSpecialChars(username);
	password = htmlSpecialChars(password);
	if (username == "" || password == "") {
		//$("#tips").text("密码或用户名不能为空");
		showSB("密码或用户名不能为空")
		//$('#loading').hide();
	} else {
		//用加密传输可以避免一定程度的暴力破解密码，参考Burp Suite
		//也可以防止一些XSS跨站攻击命令的执行
		let str = username + '#' + password;
		let mean = 1; //模式选择
		let ciphertext = '';
		//md5加密
		ciphertext = $.md5(str);
		SHOWING = $.ajax({
			type: "POST",
			url: 'login',
			async: true,
			//使用异步的方式,true为异步方式
			data: {
				'PW': ciphertext
			},
			success: function(result) {
				if (result == "success") {
					//$("#tips").text("用户名和密码正确");
					showSB("登陆成功 正在跳转")
					setTimeout('', "1000");
					document.location.reload();
				} else {
					//$("#tips").text("密码或用户名错误");
					showSB('用户名或密码错误')
				}
			},
			error: function() {
				//$("#tips").text('服务器或网络异常')
				showSB('网络异常 请稍后再试')
			}
		});
		$.when(SHOWING).done(function() {
			$('#loading').hide();
		});
	}
}
