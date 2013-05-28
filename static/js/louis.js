function init(){
	step = -1;
	max_step = 3;
	instruction_word = {};
	instruction_word["0"] = "Today, I would like to show what UI component is. The definition is kind of ambiguous.\nso I will go through some example to better understand";
	instruction_word["1"] = "These are examples for listview in mobile UI design";
	instruction_word["2"] = "Here you come examples for grid view"
	instruction_word["3"] = "now we have some kinds of primitive UI component"
	//console.log(instruction_word);

	image_uri = Array();
	//image_uri.push
	image_uri.push('/static/img/example1.png');

}

function set_buttons(){
	$('#previous').hide();
	$('#move').click(function(){
		//var logo = document.getElementById("logo");	
        //TweenLite.to(logo, 3, {left:"+=100px", ease:Elastic.easeInOut});
        if( step >= max_step-1){
        	return;
        }
        update_instruction_words(++step);
        
        if(step >= max_step-1){
        	$('#move').hide('slow');
        }
        if(step > 0){
        	$('#previous').show('slow');
        }

   	});

	$('#previous').click(function(){
		if (step <= 0) {
			return;
		}
		step--;
		update_instruction_words(step);	
		if(step <= 0){
			$('#previous').hide('slow');
		}
		if(step < max_step-1){
			$('#move').show('slow');
		}
	});
}

function update_instruction_image(step){

}

function update_instruction_words(step){
	console.log("step is now " + step);
	$('#instruction_word').html(instruction_word[step]);
	if(step == 1){
		$('#image').attr('src', '/static/img/example1.png')
	}
}

function heartbeat(){
	setInterval(function(){
		//alert("get data");
		getExtendedWindowData();
	}, 1000);
}

function getExtendedWindowData(){
	$.ajax({
		type: "GET",
		url: "./window_log",
		dataType: "json",
		success: function(data){
			//$.each(data, function(i, item){
			//
			//});
			console.log(data);
			//String showing_string = 'id' + str
			$('#louis').html(data['data'][0]['log_id']);
		},
		error: function(XMLHttpRequest, textStatus, errorThrown){

		}
	});
}