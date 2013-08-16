var roomCovers = {
    'B23.104': {x: 360, y: 517, width: 52, height: 56, floor: 1},
    'B23.105B': {x: 320, y: 517, width: 47, height: 56, floor: 1},
    'B23.107': {x: 225, y: 520, width: 60, height: 80, floor: 1},
    'B23.109': {x: 135, y: 480, width: 90, height: 120, floor: 1},
    'B23.110': {x: 135, y: 370, width: 90, height: 120, floor: 1},
    'B23.114': {x: 135, y: 260, width: 50, height: 65, floor: 1}, 
    'B23.115': {x: 180, y: 260, width: 50, height: 65, floor: 1}, 
    'B23.116': {x: 230, y: 260, width: 50, height: 65, floor: 1},
    'B23.120': {x: 702, y: 517, width: 45, height: 56, floor: 1},
    'B23.122': {x: 662, y: 517, width: 47, height: 56, floor: 1},
    'B23.123': {x: 360, y: 425, width: 47, height: 62, floor: 1},
    'B23.124': {x: 630, y: 517, width: 40, height: 56, floor: 1},
    'B23.126': {x: 575, y: 517, width: 52, height: 56, floor: 1},
    'B23.129A': {x: 440, y: 285, width: 150, height: 150, floor: 1},
    'B23.210': {x: 190, y: 520, width: 60, height: 75, floor: 2},
    'B23.211': {x: 90, y: 350, width: 100, height: 125, floor: 2},
    'B23.212': {x: 90, y: 470, width: 100, height: 117, floor: 2},
    'B23.213': {x: 810, y: 530, width: 85, height: 60, floor: 2},
    'B23.214': {x: 845, y: 485, width: 52, height: 40, floor: 2},
    'B23.214B': {x: 845, y: 440, width: 52, height: 48, floor: 2},
    'B23.215': {x: 845, y: 350, width: 52, height: 52, floor: 2},
    'B23.215B': {x: 845, y: 400, width: 52, height: 40, floor: 2},
    'B23.216': {x: 740, y: 530, width: 70, height: 55, floor: 2},
    'B23.217A': {x: 750, y: 360, width: 50, height: 42, floor: 2},
    'B23.217B': {x: 750, y: 405, width: 50, height: 38, floor: 2},
    'B23.228': {x: 510, y: 130, width: 62, height: 65, floor: 2},
    'B23.229': {},
    'B23.230': {x: 420, y: 130, width: 60, height: 65, floor: 2},
    'B23.kitchen': {x: 740, y: 410, width: 57, height: 77, floor: 1}
}


var roomCoordinates = {
    'B23.104': {x: 370, y: 535, floor: 1},
    'B23.105B': {x: 325, y: 530, floor: 1},
    'B23.107': {x: 235, y: 540, floor: 1},
    'B23.109': {x: 165, y: 530, floor: 1},
    'B23.110': {x: 160, y: 415, floor: 1},
    'B23.114': {x: 140, y: 280, floor: 1}, 
    'B23.115': {x: 190, y: 280, floor: 1}, 
    'B23.116': {x: 235, y: 280, floor: 1},
    'B23.120': {x: 700, y: 530, floor: 1},
    'B23.122': {x: 670, y: 530, floor: 1},
    'B23.123': {x: 365, y: 440, floor: 1},
    'B23.124': {x: 625, y: 530, floor: 1},
    'B23.126': {x: 580, y: 530, floor: 1},
    'B23.129A': {x: 500, y: 340, floor: 1},
    'B23.210': {x: 190, y: 530, floor: 2},
    'B23.211': {x: 120, y: 400, floor: 2},
    'B23.212': {x: 120, y: 500, floor: 2},
    'B23.213': {x: 830, y: 540, floor: 2},
    'B23.214': {x: 855, y: 490, floor: 2},
    'B23.214B': {x: 855, y: 445, floor: 2},
    'B23.215': {x: 855, y: 360, floor: 2},
    'B23.215B': {x: 855, y: 400, floor: 2},
    'B23.216': {x: 760, y: 540, floor: 2},
    'B23.217A': {x: 750, y: 365, floor: 2},
    'B23.217B': {x: 750, y: 405, floor: 2},
    'B23.228': {x: 530, y: 145, floor: 2},
    'B23.229': {},
    'B23.230': {x: 430, y: 145, floor: 2},
    'B23.kitchen': {x: 750, y: 430, floor: 1}
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


function checkProblem() {
    $.ajax({
        type: "GET",
        url: "./get_problem?",
        dataType: 'json',
        success: function(data) {
            if(!('data' in data)) {
                return;
            }

            if('problem' in data['data']) {
                if(data['data']['problem'].length <= 0) {
                    return;
                }

                var problems = data['data']['problem'];

                for(var i = 0; i < problems.length; i++) {
                    var problem = problems[i];
                    var id = problem['problem_id'];
                    var location = problem['location'];
                    var description = problem['description'];

                    if(location in roomCoordinates) {
                        var coordinate = roomCoordinates[location];                            
                        plotProblem(id, coordinate.x, coordinate.y, coordinate.floor, description);
                    }

                        // init problem id
                        if(problemId == -1) {
                            problemId = id;
                        }
                    }

                    setInterval(blink, 1000);

                    $("#dialog").popover({
                        html: true,
                        placement: 'top',
                        trigger: 'manual',
                        content: data['data']['problem'][0]['description'] + '<br><button id="close-me" type="button" class="btn btn-primary">OK, I take it</button>'
                    });

                    $("#dialog").parent().delegate('button#close-me', 'click', function() {
                        $("#dialog").popover('hide');
                        $.ajax({
                            type: "GET",
                            url: "./confirm_to_solve_problem?problem_id=" + problemId,
                            dataType: 'json',
                            success: function(data) {
                            },
                            error: function(XMLHttpRequest, textStatus, errorThrown) {
                            }
                        });
                    });
                    $("#dialog").popover('show');
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                var data = {
                    data: {
                        question: {
                            error_message: "Mobile computing and networks",
                            option_1: "Mobile computing and networks",
                            option_2: "Space travel",
                            option_3: "Startups",
                            option_4: "Public Transportation",
                            problem_category: "introduction",
                            problem_desc: "The CyLab Mobility Research Center was established to explore developments in",
                            problem_id: 1,
                            updated_at: "Tue, 06 Aug 2013 12:34:03 GMT"
                        },
                        problem: [
                        {problem_id: 5, location: 'B23.123', description: "Oops! There's no one in the room<br> but the light was left on!<br> Can you visit Room 123 and turn it off?<br>I'll give you candy if you do!"},
                        {problem_id: 10, location: 'B23.107', description: "Oops! There's no one in the room<br> but the light was left on!<br> Can you visit Room 107 and turn it off?<br>I'll give you candy if you do!"},
                        {problem_id: 3, location: 'B23.109', description: "Oops! There's no one in the room<br> but the light was left on!<br> Can you visit Room 109 and turn it off?<br>I'll give you candy if you do!"},
                        {problem_id: 2, location: 'B23.110', description: "Oops! There's no one in the room<br> but the light was left on!<br> Can you visit Room 110 and turn it off?<br>I'll give you candy if you do!"},
                        {problem_id: 99, location: 'B23.115', description: "Oops! There's no one in the room<br> but the light was left on!<br> Can you visit Room 115 and turn it off?<br>I'll give you candy if you do!"}
                        ]
                    }
                };



                if(data['data']['problem'].length <= 0) {
                    return;
                }

                var problems = data['data']['problem'];

                for(var i = 0; i < problems.length; i++) {
                    var problem = problems[i];
                    var id = problem['problem_id'];
                    var location = problem['location'];
                    var description = problem['description'];

                    if(location in roomCoordinates) {
                        var coordinate = roomCoordinates[location];

                        plotProblem(id, coordinate.x, coordinate.y, coordinate.floor, description);
                    }

                        // init problem id and dialog description
                        if(problemId == -1) {
                            problemId = id;
                            $("#dialog_desc").html(description);
                        }
                    }

                    setInterval(blink, 1000);

                    $("#dialog").show();

                }
            });
}

$("#close-me").click(function() {
    $.ajax({
        type: "GET",
        url: "./confirm_to_solve_problem?problem_id=" + problemId,
        dataType: 'json',
        success: function(data) {
            $("#dialog_desc").html("Thank You!");
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            $("#dialog_desc").html("Thank You!<br>Remember to come back to get candy!");
            $("#close-me").hide();
        }
    });

});

function plotProblem(id, x, y, floor, description) {
    console.log("plot problem");
    var str = ' <img id="problem' + id + '" src="/static/img/red-bullet.png" width="40" height="40"' +
    'style="position: absolute; z-index: 700; '+
    'margin-left: ' + x + 'px; ' +
    'margin-top: ' + y + 'px;'+
    '">';

    if(floor == 1) {
        $('#map1').append(str);
    } else if(floor == 2) {
        $('#map2').append(str);
    }

        // set up tooltip
        $('#problem' + id).tooltip({
            title: "Help This Room"
        });

        $('#problem' + id).click(function() {
            /*
            $("#dialog").popover('destroy');
            $("#dialog").popover({
                html: true,
                placement: 'top',
                trigger: 'manual',
                content: description + '<br><button id="close-me" type="button" class="btn btn-primary">OK, I take it</button>'
            });

            // show previous problem red dot
            
            */
            $("#problem" + problemId).show();
            $("#dialog_desc").html(description);
            //$("#dialog").popover('show');

            // update problem id for submitting to server
            problemId = id;
            
        });
    }

    function plotHuman(id, x, y, floor) {
        console.log("plot human");
        var str = ' <img id="human' + id + '" src="/static/img/human.png" width="40" height="40"' +
        'style="position: absolute; z-index: 500; '+
        'margin-left: ' + x + 'px; ' +
        'margin-top: ' + y + 'px;'+
        '">';

        if(floor == 1) {
            $('#map1').append(str);
        } else if(floor == 2) {
            $('#map2').append(str);
        }
    }

    function plotLight(id, x, y, floor) {
        console.log("plot light");
        return;
        var str = ' <img id="light' + id + '" src="/static/img/light.png" width="40" height="40"' +
        'style="position: absolute; z-index: 500; '+
        'margin-left: ' + (x-10) + 'px; ' +
        'margin-top: ' + (y-10) + 'px;'+
        '">';

        if(floor == 1) {
            $('#map1').append(str);
        } else if(floor == 2) {
            $('#map2').append(str);
        }
    }

    function plotBulb(id, x, y, floor) {
        console.log("plot bulb");
        return;
        var str = ' <img id="bulb' + id + '" src="/static/img/bulb.png" width="40" height="40"' +
        'style="position: absolute; z-index: 500; '+
        'margin-left: ' + (x-10) + 'px; ' +
        'margin-top: ' + (y-10) + 'px;'+
        '">';

        if(floor == 1) {
            $('#map1').append(str);
        } else if(floor == 2) {
            $('#map2').append(str);
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

                        if(value > 900) {
                            var str = ' <img id="cover' + i + '" src="/static/img/yellow-cover.png" width="' + cover.width + '" height="' + cover.height + '"' +
                            'style="position: absolute; z-index: 50; '+
                            'margin-left: ' + (cover.x) + 'px; ' +
                            'margin-top: ' + (cover.y) + 'px;'+
                            '">';

                            if(cover.floor == 1) {
                                $('#map1').append(str);
                            } else if(cover.floor == 2) {
                                $('#map2').append(str);
                            }
                            
                            plotLight(i, coordinate.x, coordinate.y, coordinate.floor);
                        } else {
                            var str = ' <img id="cover' + i + '" src="/static/img/gray-cover.png" width="' + cover.width + '" height="' + cover.height + '"' +
                            'style="position: absolute; z-index: 50; '+
                            'margin-left: ' + (cover.x) + 'px; ' +
                            'margin-top: ' + (cover.y) + 'px;'+
                            '">';

                            if(cover.floor == 1) {
                                $('#map1').append(str);
                            } else if(cover.floor == 2) {
                                $('#map2').append(str);
                            }
                            
                            plotBulb(i, coordinate.x, coordinate.y, coordinate.floor);
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
        //location.reload();
    } else {
        refreshFlag = 1;
    }
}

$(document).mousemove(function(event){
    refreshFlag = 0;
});


$(function() {
    checkProblem();
    getSensorData();

    $('#myTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    })

    setInterval(reload, 30000);
});