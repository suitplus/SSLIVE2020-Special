var CountdownEnd = new Date("2021/04/18,19:00:00");
$.ajax({
	url: "/files/config/coding/livestart.json",
	method: "GET",
	success: function(data) {
		// 请注意，这里的月份一定要减1，即一月应该是“0月”
		CountdownEnd = new Date(data.year, data.month - 1, data.day, data.hour, data.minute);
	},
});

function newtime() {
	var now = new Date();

	var rest = parseInt((CountdownEnd.getTime() - now.getTime()) / 1000);

	var day = parseInt(rest / 3600 / 24);
	var hour = parseInt((rest / 3600) % 24);
	var min = parseInt((rest / 60) % 60);
	var sec = parseInt(rest % 60);


	if (day.toString().length == 1) {
		day = "0" + day
	}
	if (hour.toString().length == 1) {
		hour = "0" + hour
	}
	if (min.toString().length == 1) {
		min = "0" + min
	}
	if (sec.toString().length == 1) {
		sec = "0" + sec
	}

	if (rest <= 0) {
		$("#timer-countdown").html(
			'00 <span class="timer-small">天</span> 00 <span class="timer-small">时</span> 00 <span class="timer-small">分</span> 00 <span class="timer-small">秒</span>'
		);
		clearInterval(newtime);
	} else {
		$("#timer-countdown").html(day + ' <span class="timer-small">天</span> ' + hour +
			' <span class="timer-small">时</span> ' + min + ' <span class="timer-small">分</span> ' + sec +
			' <span class="timer-small">秒</span>')
	}
};