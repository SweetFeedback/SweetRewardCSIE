var roomCovers = {
    'CSIE.340': {x: 500, y: 17, width: 52, height: 56, floor: 1}
}


var roomCoordinates = {
    'CSIE.340': {x: 550, y: 100, floor: 1},
    'CSIE.324': {x: 675, y: 230, floor: 1}
};

var machine1 = {'x': 520, 'y': 500};
var machine2 = {'x': 480, 'y': 270};
var machine3 = {'x': 740, 'y': 380};

var sources = {
    mrc: '/static/img/mrc/mrc.png',
    cold: '/static/img/others/char-cold.png',
    sunglass: '/static/img/others/char-sunglass.png',
    headphone: '/static/img/others/char-headphone.png',
    sweat: '/static/img/others/char-sweat.png',
    transportation: '/static/img/transportation/empty.png'
};
var sourcesLength = 6;

var problemId = -1;
var questionAns;
var questionId;
var optionFlatA = false;
var optionFlatB = false;
var optionFlatC = false;
var optionFlatD = false;

function parseProblemJsonString (data) {
    if(!('data' in data)) {
        return;
    }
    // show problem in the enviroment, else show a question if no problem
    if('problem' in data['data'] && data['data']['problem'].length > 0) {
        var problems = data['data']['problem'];

        for(var i = 0; i < problems.length; i++) {
            var problem = problems[i];
            var id = problem['problem_id'];
            var location = problem['location'];
            var description = problem['problem_desc'];
            if(location in roomCoordinates) {
                var coordinate = roomCoordinates[location];

                plotProblem(id, coordinate.x, coordinate.y, coordinate.floor, description);
            }

            // init problem id and dialog description
            if(problemId == -1) {
                problemId = id;
                $("#problem-desc").html(description);
            }
        }
        setInterval(blink, 1000);
        $("#problem-dialog").show();
        $("#dialog-wrap").show();
    } else if('question' in data['data']) {
        var question = data['data']['question'];
        var description = question['problem_desc'];
        var optionA = question['option_1'];
        var optionB = question['option_2'];
        var optionC = question['option_3'];
        var optionD = question['option_4'];
        questionId = question['problem_id'];
        questionAns = question['answer'];

        $("#question-desc").html("Q: " + description);

        $("#question-optionA").html('<div style="display: table-cell; width:110px; height: 80px; text-align: center; vertical-align:middle;">'+optionA+"</div>");
        $("#question-optionB").html('<div style="display: table-cell; width:110px; height: 80px; text-align: center; vertical-align:middle;">'+optionB+"</div>");
        $("#question-optionC").html('<div style="display: table-cell; width:110px; height: 80px; text-align: center; vertical-align:middle;">'+optionC+"</div>");
        $("#question-optionD").html('<div style="display: table-cell; width:110px; height: 80px; text-align: center; vertical-align:middle;">'+optionD+"</div>");

        $("#question-dialog").show();
        $("#dialog-wrap").show();
    }

}

$("#take-survey").click(function() {
    window.location.href = "./survey";
});

function judgeAnswer(option) {
    var answer = 0;
    if(option == 'A') {
        answer = 1;
    } else if(option == 'B') {
        answer = 2;
    } else if(option == 'C') {
        answer = 3;
    } else {
        answer = 4;
    }


    if(questionAns != answer) {
        $("#question-message").html("Try different answer!");
        $("#question-message").show();
        $("#question-option" + option).css("background-color", "rgb(255, 143, 143)");
        $.get("./question_log?problem_id="+questionId+"&option="+answer+"&correct=0");
    } else {
        $("#survey-dialog").show();

        $("#question-message").html('Correct! Enjoy the candies!');
        $("#question-message").show();

        $("#question-option" + option).css("background-color", "rgb(204, 255, 204)");
        $.get("./question_log?problem_id="+questionId+"&option="+answer+"&correct=1");
        $.get("./feedback_insert?application_id=14&feedback_type=positive&feedback_description=well done");
        optionFlatA = true;
        optionFlatB = true;
        optionFlatC = true;
        optionFlatD = true;
    }
}

$("#question-optionA").click(function() {
    if(optionFlatA) {
        return;
    }
    optionFlatA = true;

    judgeAnswer('A');
});

$("#question-optionB").click(function() {
    if(optionFlatB) {
        return;
    }
    optionFlatB = true;
    judgeAnswer('B');
});

$("#question-optionC").click(function() {
    if(optionFlatC) {
        return;
    }
    optionFlatC = true;
    judgeAnswer('C');
});

$("#question-optionD").click(function() {
    if(optionFlatD) {
        return;
    }
    optionFlatD = true;
    judgeAnswer('D');
});

function checkProblem() {
    $.ajax({
        type: "GET",
        url: "./get_problem?",
        dataType: 'json',
        success: function(data) {
            parseProblemJsonString(data);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            var data = {
                data: {
                    problem: [
                        {
                        problem_id: 1,
                        location: 'CSIE.340',
                        problem_desc: "hi"
                        }, 
                        {
                        problem_id: 2,
                        location: 'CSIE.324',
                        problem_desc: "hii"
                        }

                    ]
                    /*
                    question: {
                        error_message: "Mobile computing and networks",
                        option_1: "Knowledge is liberty.",
                        option_2: "Reach within, shape the future.",
                        option_3: "My heart is in the work.",
                        option_4: "Think. Grow. Change.",
                        problem_category: "introduction",
                        problem_desc: "What is the Carnegie Mellon University motto?",
                        problem_id: 1,
                        answer: 3,
                        updated_at: "Tue, 06 Aug 2013 12:34:03 GMT"
                    }
                    */
                }
            };
            parseProblemJsonString(data);
        }
    });
}

$("#close-me").click(function() {
    $.ajax({
        type: "GET",
        url: "./confirm_to_solve_problem?problem_id=" + problemId,
        dataType: 'json',
        success: function(data) {
            $("#problem-desc").html("Thank You!<br>Remember to come back to get candy!");
            $("#close-me").hide();
            $("#survey-dialog").show();
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#problem-desc").html("Thank You!<br>Remember to come back to get candy!");
            $("#close-me").hide();
            $("#survey-dialog").show();
        }
    });

});

function plotProblem(id, x, y, floor, description) {
    var str = ' <img id="problem' + id + '" src="/static/img/red-bullet.png" width="40" height="40"' +
    'style="position: absolute; z-index: 700; '+
    'margin-left: ' + x + 'px; ' +
    'margin-top: ' + y + 'px;'+
    '">';

    if(floor == 1) {
        $('#map1').append(str);
    } else if(floor == 2) {

    }

    // set up tooltip
    $('#problem' + id).tooltip({
        title: "Help This Room"
    });

    $('#problem' + id).click(function() {
        $("#problem" + problemId).show();
        $("#problem-desc").html(description);
        $("#close-me").show();
        $("#survey-dialog").hide();
        //$("#dialog").popover('show');

        // update problem id for submitting to server
        problemId = id;
    });
}

function plotHuman(id, x, y, floor) {
    var str = ' <img id="human' + id + '" src="/static/img/human.png" width="40" height="40"' +
    'style="position: absolute; z-index: 500; '+
    'margin-left: ' + x + 'px; ' +
    'margin-top: ' + y + 'px;'+
    '">';

    if(floor == 1) {
        $('#map1').append(str);
    } else if(floor == 2) {

    }
}

function plotLight(id, x, y, floor) {
    var str = ' <img id="light' + id + '" src="/static/img/light.png" width="40" height="40"' +
    'style="position: absolute; z-index: 500; '+
    'margin-left: ' + (x-10) + 'px; ' +
    'margin-top: ' + (y-10) + 'px;'+
    '">';

    if(floor == 1) {
        $('#map1').append(str);
    } else if(floor == 2) {
    }
}

function plotBulb(id, x, y, floor) {
    var str = ' <img id="bulb' + id + '" src="/static/img/bulb.png" width="40" height="40"' +
    'style="position: absolute; z-index: 500; '+
    'margin-left: ' + (x-10) + 'px; ' +
    'margin-top: ' + (y-10) + 'px;'+
    '">';

    if(floor == 1) {
        $('#map1').append(str);
    } else if(floor == 2) {
        
    }
}

function getSensorData() {
    $.ajax({
        type: "GET",
        url: "./sensor_data",
        dataType: 'json',
        success: function(data) {

            var motionData = data['data']['motion'];
            var lightDatas = data['data']['light'];

            for(var i = 0; i < motionData.length; i++) {
                if(parseInt(motionData[i]['value']) > 800) {
                    if(motionData[i]['location'] in roomCoordinates) {
                        var coordinate = roomCoordinates[motionData[i]['location']];
                        plotHuman(i, coordinate.x-20, coordinate.y-20, coordinate.floor);
                    }
                }
            }

            for(var i = 0; i < lightDatas.length; i++) {
                var lightData = lightDatas[i];
                var location = lightData['location'];
                var value = parseInt(lightData['value'])

                if(location in roomCoordinates) {
                    var coordinate = roomCoordinates[location];
                    var cover = roomCovers[location];

                    if(value < 790) {
                        var str = ' <img id="cover' + i + '" src="/static/img/yellow-cover.png" width="' + cover.width + '" height="' + cover.height + '"' +
                        'style="position: absolute; z-index: 50; '+
                        'margin-left: ' + (cover.x) + 'px; ' +
                        'margin-top: ' + (cover.y) + 'px;'+
                        '">';

                        if(cover.floor == 1) {
                            $('#map1').append(str);
                        } else if(cover.floor == 2) {

                        }
                        
                        //plotLight(i, coordinate.x, coordinate.y, coordinate.floor);
                    } else {
                        var str = ' <img id="cover' + i + '" src="/static/img/gray-cover.png" width="' + cover.width + '" height="' + cover.height + '"' +
                        'style="position: absolute; z-index: 50; '+
                        'margin-left: ' + (cover.x) + 'px; ' +
                        'margin-top: ' + (cover.y) + 'px;'+
                        '">';

                        if(cover.floor == 1) {
                            $('#map1').append(str);
                        } else if(cover.floor == 2) {

                        }
                        
                        //plotBulb(i, coordinate.x, coordinate.y, coordinate.floor);
                    }
                }
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
        }
    });
}


var cnt = 0;

function blink() {
    if(cnt == 0) {
        $("#problem" + problemId).show();
        cnt = 1;
    } else {
        $("#problem" + problemId).hide();
        cnt = 0;
    }
}

var refreshFlag = 1;

function reload() {
    if(refreshFlag == 1) {
        location.reload();
    } else {
        refreshFlag = 1;
    }
}

$(document).mousemove(function(event){
    refreshFlag = 0;
});


$(function() {
    checkProblem();
    //getSensorData();

    $("#question-dialog").hide();
    $("#problem-dialog").hide();
    $("#question-message").hide();
    $("#survey-dialog").hide();


    $("#dialog-wrap").hide();
    $('html, body').animate({scrollTop: '100px'}, 800);

    setInterval(reload, 60000);
});
