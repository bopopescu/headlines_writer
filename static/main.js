$(document).ready(function() {
	$('.generate').click(function(e) {
		e.preventDefault;
		$(".answer-wrapper").removeClass("correct");
		$(".answer-wrapper").removeClass("wrong");
		$(".answer").text('');

		$.get( "/generate", function( data ) {
			var rand =  Math.floor(Math.random() * (1 - 0 + 1)) + 0;
			if(rand == 0) {
				$( "#top-title" ).text( data.real.replace(/[.,"'?!`“]/g,"") );
				$( "#bottom-title" ).text( data.generated );
				$("#real").val('top-title');
			} else {
				$( "#top-title" ).text( data.generated );
				$( "#bottom-title" ).text( data.real.replace(/[.,"'?!`“]/g,"") );
				$("#real").val('bottom-title');
			}
			console.log(rand);
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
