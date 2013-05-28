function win_open(w_id, degree) {
        
    $("#win_"+w_id).css({ WebkitTransform: 'rotate(' + degree + 'deg)'});  
    $("#win_"+w_id).css({ '-moz-transform': 'rotate(' + degree + 'deg)'});                      
    setTimeout(function() {
        ++degree; 
        if(degree>=30){
            degree = 0;
        }else{
            win_open(w_id, degree);                
        }

    },5);
}
function win_close(w_id, degree) {

    $("#win_"+w_id).css({ WebkitTransform: 'rotate(' + degree + 'deg)'});  
    $("#win_"+w_id).css({ '-moz-transform': 'rotate(' + degree + 'deg)'});                      
    setTimeout(function() {
        --degree; 
        if(degree<=0){
            degree = 0;
        }else{
            win_close(w_id, degree);                
        }
    },5);
}

function getUserPreference(){
    /* get profile preference */

    $.ajax({
        type: "GET",
        url: "./php/mobile/getUserPreference.php",
        data: { 
            "token": window.cur_token
        },
        dataType: 'json',
        success: function(data) {
            if(data['success'] == 1){
                window.light_threshold = parseInt(data['data']['light_threshold']); 
                window.temperature_threshold = parseInt(data['data']['temperature_threshold']);
                window.micro_threshold = parseInt(data['data']['micro_threshold']);

                $('#light_preference').text(window.light_threshold);
                $('#temp_preference').text(window.temperature_threshold);
                $('#sound_preference').text(window.micro_threshold);
                $('#user_preference').show();
            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {}
    });
}

function updateWindowStatus(){
    /* get extended windows state*/
    $.ajax({
        type: "GET",
        url: "./php/getExtendedWindowState.php",

        dataType: 'json',
        success: function(data) {
            
            $.each(data, function(i, item) {
                if(item){
                    var w_id = item['window_id'];
                    var w_state = item['state'];
                    var w_status = item['status'];

                    // window_state
                    if(parseInt(w_state) == 0){ //close
                        
                        if($('#win_'+w_id).hasClass("open")){
                            win_close(w_id, 0);
                            $('#win_'+w_id).removeClass("open");
                        }
                    }else{
                        if(!$('#win_'+w_id).hasClass("open")){
                            win_open(w_id, 0);
                            $('#win_'+w_id).addClass("open");
                        }
                    }

                    if(parseInt(w_status) == 0){ //bad, warning
                        if(!$('#win_'+w_id).hasClass("win_err")){
                            $('#win_'+w_id).addClass("win_err");
                        }
                    }else{
                        if($('#win_'+w_id).hasClass("win_err")){
                            $('#win_'+w_id).removeClass("win_err");
                        }
                    }
                }else{
                    
                    if($('#win_'+w_id).hasClass("open")){
                        win_close(w_id, 0);
                        $('#win_'+w_id).removeClass("open");
                    }
                }
                

            });
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert("get sensor Error");
        }
    });    
}


function updateMachineStatus(){
    
    /* get sensor value*/
    $.ajax({
        type: "GET",
        url: "./php/getSensorValuesNew.php",

        dataType: 'json',
        success: function(data) {
            
            $('#mrc_1').addClass('offline');
            $('#mrc_2').addClass('offline');
            $('#mrc_3').addClass('offline');
            //$('#mrc_4').addClass('offline');
            //$('#mrc_5').addClass('offline');

            $.each(data['data'], function(i, item) {
                var d_id = item['device_id'];

                

                // light 
                if(parseFloat(item['light_level']) >= window.light_threshold){
                    $('#mrc_'+d_id+' img.sunglass').css("visibility", "visible");
                }else{
                    $('#mrc_'+d_id+' img.sunglass').css("visibility", "hidden");
                }


                // temperature
                if(parseFloat(item['temperature']) >= window.temperature_threshold+2){
                    $('#mrc_'+d_id+' img.sweat').css("visibility", "visible");
                    $('#mrc_'+d_id+' img.cold').css("visibility", "hidden");
                }else{ 
                    if(parseFloat(item['temperature']) <= window.temperature_threshold-2){                                
                        $('#mrc_'+d_id+' img.cold').css("visibility", "visible");
                        $('#mrc_'+d_id+' img.sweat').css("visibility", "hidden");
                    }else{
                        $('#mrc_'+d_id+' img.sweat').css("visibility", "hidden");
                        $('#mrc_'+d_id+' img.cold').css("visibility", "hidden");
                    }
                }

                // sound_level
                if(parseFloat(item['sound_level']) >= window.micro_threshold){
                    $('#mrc_'+d_id+' img.headphone').css("visibility", "visible");
                }else{
                    $('#mrc_'+d_id+' img.headphone').css("visibility", "hidden");
                }


                // window_state
                /*if(parseInt(item['window_state']) == 1){
                    if(!$('#win_'+d_id).hasClass("open")){
                        win_open(d_id, 0);
                        $('#win_'+d_id).addClass("open");
                    }
                   
                }else{
                    win_close(d_id, 0); 
                    if($('#win_'+d_id).hasClass("open")){
                        win_close(d_id, 0);
                        $('#win_'+d_id).removeClass("open");
                    }
                }*/

                
                //show machine
                $('#mrc_'+d_id).removeClass("offline");

            });
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert("get sensor Error");
        }
    });

    
}

function milliSecondToMinutes(ret){
    var one_minutes = 1000*60;
    return Math.ceil(ret / one_minutes);
}

function checkLogin(){
    $.ajax({
        type: "GET",
        url: "./php/mobile/verifyUser.php",
        dataType: 'json',
        success: function(data) {
                
            if(data["is_logged_in"]==1){

                window.cur_user = data["account"];
                window.cur_token = data["token"];
                window.cur_uid = data["user_id"]; 
                $('#current_user').text("Hi, "+data["account"]+"! ");
                $('#current_user').append('<b class="caret"></b>');
        
                $('#login').hide();
                $('#setting').show();


                getUserPreference();

            }
            else{
                $('#login').show();
                $('#setting').hide();

            }
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
                //alert("Error");    
        }
    });
}

function readLocationData(){
}

function readRoomProblem(room_id, room_name, room_problem_count){
    var problemDiv = $('#room_problem_'+room_id);
    var problemBody = $('<div></div>').addClass('modal-body').appendTo(problemDiv);
    problemBody.append('<button type="button" class="close" data-dismiss="modal">&times;</button>');
    problemBody.append('<div class="room_title"><h3>'+room_name+'</h3><img class="room_emotion" src="img/emotion/emotion'+getEmotion(room_problem_count)+'.png"/></div>');
    problemBody.append("<hr/>")

    /* get existing report */
    $.ajax({
        type: "GET",
        url: "./php/getExistReports.php",
        data: { "room_id": room_id },
        dataType: 'json',
        success: function(data) {

            $.each(data, function(i, item) {
                problemBody.append("<h3>Problem "+ (i+1) +": "+item.title+" ("+item.id+")</h3>");
                problemBody.append('<span style="margin-left: 5px;">Create at '+item.created_at+'</span>');
                problemBody.append('<br/><a href="#" class="btn fixIssue" id="fix_problem_'+item.id+'" data-dismiss="modal"">Fixed</a><hr/>');

                //fix issue
                fixIssueReport(item.id);

            });

        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert("get exist Error");               
        }
    });
    problemDiv.append('<div class="modal-footer"><a href="#" class="btn" data-dismiss="modal" >Close</a></div>');
}

/* no use now*/
function readProblemList(){
    $('.manual-toggle').toggle();
    /* clear problem list */
    $('#problemList').remove();
    $('#problemDetail').remove();
    $('#feedbackList').remove();

    var proList = $('<div></div>').attr('id','problemList');
    $('<ul></ul>').addClass('items').appendTo(proList);
    var proDetail = $('<div></div>').attr('id', 'problemDetail');
    
    var hisList = $('<div></div>').attr('id','feedbackList');
    $('<ul></ul>').addClass('items').appendTo(hisList);
    
    $('#problemArea').append(proList);
    $('#problemArea').append(proDetail);
    $('#feedbackHistory').append(hisList);

    /* get feedback history */
    $.ajax({
        type: "GET",
        url: "./php/getFeedbackHistory.php",
        dataType: 'json',
        success: function(data) {
            
            $.each(data, function(i, item) {
                var historyList = $('<li><a href="#" class="tooltip-test" title="'+item.feedback_description+'">'+item.feedback_type+' ('+item.created_time+')</a></li>');

                if(item.feedback_type == "positive"){
                    historyList.addClass('positive');
                }else if(item.feedback_type == "negative"){
                    historyList.addClass('negative');
                }else if(item.feedback_type == "sound"){
                    historyList.addClass('sound');
                }

                $('#feedbackList .items').append(historyList);
            });

            $('.tooltip-test').tooltip();
            
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert("get exist Error");               
        }
    });


    var problemMap = {};

    /* get existing report */
    $.ajax({
        type: "GET",
        url: "./php/getExistReports.php",
        dataType: 'json',
        success: function(data) {

            $.each(data, function(i, item) {
                $('#problemList .items').append('<li><a class="manual-toggle" data-toggle="modal" href="#problem_'+item.id+'">'+item.title+'</a></li>');

                var problemDiv = $("<div></div>").attr('id','problem_'+item.id).addClass('modal hide fade');
                var problemBody = $('<div></div>').addClass('modal-body').appendTo(problemDiv);

                problemBody.append('<button type="button" class="close" data-dismiss="modal">&times;</button>');
                problemBody.append("<h3>Problem: "+item.title+"</h3>");
                problemBody.append('<span style="margin-left: 5px;">Create at '+item.created_at+'</span>');
                problemDiv.append('<div class="modal-footer"><a href="#" class="btn fixIssue" id="fix_problem_'+item.id+'" data-dismiss="modal"">Fixed it</a><a href="#" class="btn" data-dismiss="modal" >Close</a></div>');
                problemDiv.appendTo('#problemDetail');

                if(item.room in problemMap) problemMap[item.room]++;
                else    problemMap[item.room] = 1;
               

            });
            
            $.each(problemMap, function(i, item){
                
                if(i != 0){
                    $('#room_'+i).css({"background": "rgba(234,0,55,"+item/15.0+")"});
                }
            });


            /* fix an existing report */
            $('.fixIssue').click(function(){
                var report = this.id.split('_');
                $.ajax({
                    type: "GET",
                    url: "./php/makeFixReport.php",
                    data: { "user_id": window.cur_uid, "report_id": report[1] },

                    dataType: 'json',
                    success: function(data) {
                        if(data.hasOwnProperty('success') && data['success'] == 1){
                            $.post("./php/insertFeedback.php?application_id=10&type=positive"); // fix a report and get feedback //

                            readProblemList(); // update problem list
                        }
                        else if(data.hasOwnProperty('reconfirm') && data['reconfirm'] == 1){
                            /// jump out a dialog to ask whether force or not
                            var errorDiv = $("<div></div>").addClass("alert alert-error");
                            errorDiv.text("what the fuck is this ?");
                            errorDiv.appendTo($('#' + report[0]+'_'+report[1]));
                        }
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown) {
                        //alert("fix report Error");
                    }
                });
            });
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert("get exist Error");               
        }
    });
}


function readUserRank(){
    var userRank;
    var hisList;
    $('.manual-toggle').toggle();

    $('#feedbackList').remove();

    hisList = $('<div></div>').attr('id','feedbackList');
    $('<ul></ul>').addClass('items').appendTo(hisList);
    
    $('#feedbackHistory').append(hisList);

    /* get user rank */
    $.ajax({
        type: "GET",
        url: "./php/getSolveProblemUserRank.php",
        dataType: 'json',
        success: function(data) {
            
            $.each(data, function(i, item) {

                if(parseInt(item.count) > 1)
                userRank = $('<li> ' + item.account +' solve <span style="color:red;">'+item.count+' </span>problems!</li>');
                else
                userRank = $('<li> '+ item.account +' solve <span style="color:red;">'+item.count+' </span>problem!</li>');    
                
                if(i == 0) userRank.append('<img src="/static/img/badge/award.png"/>');
                $('#feedbackList .items').append(userRank);
            });

            $('.tooltip-test').tooltip();
            
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert("get exist Error");               
        }
    });                
}

function readFeedbackHistory(){
    $('.manual-toggle').toggle();

    $('#feedbackList').remove();

    var hisList = $('<div></div>').attr('id','feedbackList');
    $('<ul></ul>').addClass('items').appendTo(hisList);
    
    $('#feedbackHistory').append(hisList);

    /* get feedback history */
    $.ajax({
        type: "GET",
        url: "./php/getFeedbackHistory.php",
        dataType: 'json',
        success: function(data) {
            
            $.each(data, function(i, item) {
                var historyList = $('<li><a href="#" class="tooltip-test" title="'+item.feedback_description+'">'+item.feedback_type+' ('+item.created_time+')</a></li>');

                if(item.feedback_type == "positive"){
                    historyList.addClass('positive');
                }else if(item.feedback_type == "negative"){
                    historyList.addClass('negative');
                }else if(item.feedback_type == "sound"){
                    historyList.addClass('sound');
                }

                $('#feedbackList .items').append(historyList);
            });

            $('.tooltip-test').tooltip();
            
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
            //alert("get exist Error");               
        }
    });
}

/*
    1. >9
    2. >6
    3. >3
    4. >0
    5. 0    
*/
function getEmotion(problem_count){
    var level = 3;
    var emotion = 1;
    if(problem_count > level*3) emotion = 5;
    else if(problem_count > level*2) emotion = 4;
    else if(problem_count > level*1) emotion = 3;
    else if(problem_count > level*0) emotion = 2;
    else emotion = 1;

    return emotion;
}

function readRoomRank(){
    $('.manual-toggle').toggle();

    /* clear problem list */
    $('#problemList').remove();
    $('#problemDetail').remove();
    

    var proList = $('<div></div>').attr('id','problemList');
    $('<ul></ul>').addClass('items').appendTo(proList);
    var proDetail = $('<div></div>').attr('id', 'problemDetail');
    
                    
    $('#problemArea').append(proList);
    $('#problemArea').append(proDetail);

    $.ajax({
        type: "GET",
        url: "./php/getUnsolveProblemRoomRank.php",
        
        dataType: 'json',
        success: function(data) {
            $.each(data, function(i, item) {
                $('#problemList .items').append('<li><a class="manual-toggle" data-toggle="modal" href="#room_problem_'+item.room+'">'+item.room_name+': '+item.count+'</a> <img src="/static/img/emotion/emotion'+getEmotion(item.count)+'.png" width="22px"/></li>');

                
                var problemDiv = $("<div></div>").attr('id','room_problem_'+item.room).addClass('modal hide fade');
                problemDiv.appendTo('#problemDetail');

                readRoomProblem(item.room, item.room_name, item.count);

                //update color in map
                $('#room_'+item.room).css({"background": "rgba(234,0,55,"+item.count/15.0+")"});
            });

            
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) {
        }
    });
}

function fixIssueReport(problem_id){
    /* fix an existing report */
    $('#fix_problem_'+problem_id).click(function(event){
        
        $.ajax({
            type: "GET",
            url: "./php/makeFixReport.php",
            data: { "user_id": window.cur_uid, "report_id": problem_id },

            dataType: 'json',
            success: function(data) {
                if(data.hasOwnProperty('success') && data['success'] == 1){
                    $.post("./php/insertFeedback.php?application_id=10&type=positive"); // fix a report and get feedback //
                    readRoomRank();
                    readUserRank();
                }

            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                //alert("fix report Error");
            }
        });
    });

}


function updateLeaderBoard(){
    readRoomRank();
    readUserRank();
    //readFeedbackHistory();
}

$(function(){
    //var degree = 0, timer;
    updateLeaderBoard();
    

    $('#user_preference').hide();

    /* hide headphone */
    //$('.machine').addClass('offline');
    $('.win').removeClass('open');
    

    /* hide setting */
    $('#setting').hide();

    /* log in stuff */
    window.cur_user = "test";
    window.cur_token;
    window.cur_uid = 0;
    checkLogin();

    $('.dropdown-toggle').dropdown();
    $('#loginBt').click(function(){

        $.ajax({

            type: "GET",
            url: "./php/mobile/verifyUser.php",
            data: { "account": $('#account').val(), "password": $('#password').val() },
            dataType: 'json',
            success: function(data) {
                
                if(data["success"]==1){
                    
                    window.cur_user = data["account"];
                    window.cur_token = data["token"];
                    window.cur_uid = data["user_id"];
                    
                    $('#current_user').text("Hi, "+data["account"]+" !");
                    
                    $('#login').hide();
                    //$('#logoutBt').show();

                    $('#setting').show();

                }else{
                    $('#login').show();
                    

                    $('#setting').hide();
                    //alert("No such user!");
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                //alert("Error");    
            }
        });
    });
    $('#logoutBt').click(function(){

        $.ajax({

            type: "GET",
            url: "./php/mobile/logout.php",
            data: { },
            dataType: 'json',
            success: function(data) {
                
                if(data["success"]==1){
                    window.cur_user = 0;
                    window.cur_token = 0;
                    window.cur_uid = 0;

                    $('#current_user').text("");
                     
                    $('#login').show();
                    $('#logoutBt').hide();

                }else{
                    //alert("No such user!");
                }
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                //alert("Error");    
            }
        });
    });
    $('#registerSubmit').click(function(){
        //alert($('#reg_account').val());
        //alert($('#reg_password').val());
        $.ajax({
            type: "GET",
            url: "./php/mobile/createNewUser.php",
            data: { "account": $('#reg_account').val(), "password":$('#reg_password').val()},
            dataType: 'json',
            success: function(data){
                alert("song la");
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
            
            }
        });
    });


    //
    window.category = 0;
    $('#hot').click(function(){
        window.category = 1;
        $('#problem_title').text($('#hot').text());
    });
    $('#cold').click(function(){
        window.category = 2;
        $('#problem_title').text($('#cold').text());
    });
    $('#noise').click(function(){
        $('#problem_title').text($('#noise').text());
        window.category = 3;
    });
    $('#other').click(function(){
        $('#problem_title').text($('#other').text());
        window.category = 0;
    });


    /*$('#problem_select .dropdown-menu li a').on('click', function(){
        $('#problem_title').text($(this).text());
    });*/

    //location
    $('#location_select .dropdown-menu li a').on('click', function(){
        $('#location_title').text($(this).text());
        $('#location_id').val(this.id);
        
    });

    /* make a new report */
    $('#reportSubmit').click(function(){
        $.ajax({
            type: "GET",
            url: "./php/makeNewReport.php",
            data: { "user_id": window.cur_uid, "coordinate_x": "1", "coordinate_y": "1", "title": $('#problemInput').val(), 
                    "category": window.category, "room_id": $('#location_id').val()},

            dataType: 'json',
            success: function(data) {
                $('#problemInput').val("");
                //readProblemList(); /* update problem list */
                readRoomRank();
                //$.post("./php/insertFeedback.php?application_id=10&type=positive"); /* make new report and get feedback */
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                //alert("make new Error");
            }
        });
    });

    
    /* read exist problems */
    //readProblemList();

    /* make machine icon draggable */
    /*$(".machine").draggable({
        cursor: 'move', 
        containment: 'document'}
    );*/
    

    /* update machine status every 1 sec */
    setInterval(function(){
        updateMachineStatus();
        updateWindowStatus();
    }, 1000);

    setInterval(function(){
        
        $('.fixIssue').data-dismiss('modal');
        //readProblemList();
        updateLeaderBoard();

    }, 10000);


});