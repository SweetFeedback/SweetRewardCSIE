var refreshFlag = 0;

$("#submit").click(function() {
	var question1 = $('input[name="group1"]:checked').val();
	var question2 = $('input[name="group2"]:checked').val();
	var question3 = $('input[name="group3"]:checked').val();
	var question4 = $('input[name="group4"]:checked').val();
	var question5 = $('input[name="group5"]:checked').val();
	var question6 = $('input[name="group6"]:checked').val();
	var question7 = $('input[name="group7"]:checked').val();
	var question8 = $('input[name="group8"]:checked').val();
	var question9 = $('input[name="group9"]:checked').val();
	var question10 = $('input[name="group10"]:checked').val();
	var question11 = $('#feeling').val();

	if(typeof question1 == 'undefined') {
		$("#error_message").text("Please answer question1");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question2 == 'undefined') {
		$("#error_message").text("Please answer question2");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question3 == 'undefined') {
		$("#error_message").text("Please answer question3");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question4 == 'undefined') {
		$("#error_message").text("Please answer question4");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question5 == 'undefined') {
		$("#error_message").text("Please answer question5");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question6 == 'undefined') {
		$("#error_message").text("Please answer question6");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question7 == 'undefined') {
		$("#error_message").text("Please answer question7");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question8 == 'undefined') {
		$("#error_message").text("Please answer question8");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question9 == 'undefined') {
		$("#error_message").text("Please answer question9");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(typeof question10 == 'undefined') {
		$("#error_message").text("Please answer question10");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	} else if(question11 == '') {
		$("#error_message").text("Please answer question11");
		$("#error_message").show();
		$('html, body').animate({scrollTop: '400px'}, 800);
		return;
	}

	$("#error_message").hide();
	

	var data = {
		'question1': question1,
		'question2': question2,
		'question3': question3,
		'question4': question4,
		'question5': question5,
		'question6': question6,
		'question7': question7,
		'question8': question8,
		'question9': question9,
		'question10': question10,
		'question11': question11
	};

	$.get("./feedback_insert?application_id=15&feedback_type=positive&feedback_description=Thanks");	
	//$.get("./feedback_insert?application_id=15&feedback_type=positive&feedback_description=Thanks for taking the survey");
	$.post('./upload_survey', data, function(data) {
		window.location.href = "./";
	});
});



function reload() {

    if(refreshFlag == 1) {
        window.location.href = "./";
    } else {
        refreshFlag = 1;
    }
}

$(document).mousemove(function(event){
    refreshFlag = 0;
});

$(function() {
	$("#error_message").hide();
	setInterval(reload, 30000);
});