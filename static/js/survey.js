var refreshFlag = 0;

$("#submit").click(function() {
	var question1 = $('input[name="group1"]:checked').val();
	var question2 = $('input[name="group2"]:checked').val();
	var question3 = new Array();
	$.each($('input[name="group3"]:checked'), function(){
		question3.push($(this).val());
	});

	var question4 = new Array();
	$.each($('input[name="group4"]:checked'), function(){
		question4.push($(this).val());
	});

	var question5 = $('input[name="group5"]:checked').val();
	var question6 = $('input[name="group6"]:checked').val();
	var question7 = $('input[name="group7"]:checked').val();
	var question8 = $('input[name="group8"]:checked').val();
	var question9 = $('input[name="group9"]:checked').val();
	var question10 = $('input[name="group10"]:checked').val();
	var question11 = $('#feeling').val();

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
	$.post('./upload_survey', data).done(function(data) {
		
	});

	window.location.href = "./";
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
	setInterval(reload, 30000);
});