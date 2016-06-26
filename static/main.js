function capitalizeEachWord(str) {
    return str.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

$(function() {

});

$(document).ready(function() {
	$answerWrapper = $(".answer-wrapper");
	  $answer = $(".answer");
    $words = $(".words")
	  $title = $(".title");
	  $spinner = $(".spinner");


	$('.generate').click(function(e) {
		e.preventDefault;
		  $title.hide();
      $words.hide();

		  $spinner.show();
		  $answerWrapper.removeClass("correct");
		  $answerWrapper.removeClass("wrong");
		  $answer.text('');

		$.get( "/generate", function( data ) {
			var rand =  Math.floor(Math.random() * (1 - 0 + 1)) + 0;
			if(rand == 0) {
				//#HACK: need better data sanitization to deal with capitalization and punctuation
				$( "#top-title" ).text( capitalizeEachWord(data.real.replace(/[.,"'?!`“”]/g,"")) );
				$( "#bottom-title" ).text( capitalizeEachWord(data.generated) );
				$("#real").val('top-title');
			} else {
				$( "#top-title" ).text( capitalizeEachWord(data.generated) );
				$( "#bottom-title" ).text( capitalizeEachWord(data.real.replace(/[.,"'?!`“”]/g,"")) );
				$("#real").val('bottom-title');
			}
			  $title.show();
			  $spinner.hide();




		}, "json");
	});

    $( 'a#process_input' ).bind('click', function() {
				$.getJSON('/input_word', {
				    inputword: $('input[name="inputword"]').val(),

				}, function(data) {

            var output="<ul>";
            for (var i in data) {
                output+="<li style=list-style-type:none;>" + data[i].simword + "  :  " + data[i].value + "</li>";
            }

            output+="</ul>";
            $words.html(output);
            $words.show();
				});

				return false;
		});

	$title.click(function(e) {
		var answer = ""; 
		$answerWrapper.removeClass("correct");
		$answerWrapper.removeClass("wrong");

		if ($('#real').val() === e.target.id) {
			answer = "wrong";
		}else{
			answer = "correct";
		}

		$answer.text(answer);
		$answerWrapper.addClass(answer);
	});

});
