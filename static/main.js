function capitalizeEachWord(str) {
    return str.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

$(document).ready(function() {
	$('.generate').click(function(e) {
		e.preventDefault;
		$(".title").hide();
		$(".spinner").show();
		$(".answer-wrapper").removeClass("correct");
		$(".answer-wrapper").removeClass("wrong");
		$(".answer").text('');

		$.get( "/generate", function( data ) {
			var rand =  Math.floor(Math.random() * (1 - 0 + 1)) + 0;
			if(rand == 0) {
				$( "#top-title" ).text( data.real.replace(/[.,"'?!`“]/g,"") );
				$( "#bottom-title" ).text( capitalizeEachWord(data.generated) );
				$("#real").val('top-title');
			} else {
				$( "#top-title" ).text( capitalizeEachWord(data.generated) );
				$( "#bottom-title" ).text( data.real.replace(/[.,"'?!`“]/g,"") );
				$("#real").val('bottom-title');
			}
			$(".title").show();
			$(".spinner").hide();
		}, "json");
	});

	$('.title').click(function(e) {
		var answer = ""; 
		$(".answer-wrapper").removeClass("correct");
		$(".answer-wrapper").removeClass("wrong");

		if ($('#real').val() === e.target.id) {
			answer = "wrong";
		}else{
			answer = "correct";
		}
		$(".answer").text(answer);
		$(".answer-wrapper").addClass(answer);
	});

});
