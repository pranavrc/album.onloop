var watermark = "Album/Soundtrack Search (Leave blank for random album.)";
var requests;

function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}

/* Decode HTML entities from search query */
function htmlDecode(value){
	return $('<div/>').html(value).text();
}

/* Parse the JSON file in case of an empty search. Pivot method for running the AJAX requests. */
function jsonParse() {
	var jsonFile = "/static/list_of_albums.json";

	$.getJSON(jsonFile).success(function(data) {
		var randomIndex = Math.floor(Math.random() * data.albums.length/5); //Pick a random album index.
		var randomString = data.albums[randomIndex]; //Album at index.
		var decodedString = htmlDecode(randomString);
		var formData;
		formData = assignformString(decodedString);
		sendRequest(1, 10, formData); //10 AJAX requests sequentially.
	});

	return false;
}

/* Collect the input data before sending off the requests */
function assignformString(albumChosen) {
	formString = $('#userform');
	var f = formString.serializeArray();
	if(f[0].value == "" || f[0].value == watermark) {
		f[0].value = albumChosen;
		$('.submitText').val(f[0].value);
	}
	return f[0].value;
}

/* Send AJAX requests to server */
function sendRequest(count, maxCount, formData) {
	if (count == 1) $('div.myDiv').html("<img class=\"loader\" src=\"/static/loader.gif\" alt=\"Fetching...\" />");
	else $('div.myDiv').append("<img class=\"loader\" src=\"/static/loader.gif\" alt=\"Fetching...\" />");

	if (requests) requests.abort();
	requests = $.ajax({type:'POST', url: '/', data:{"query": formData, "count": count}, success: function(response) {
			if (count == 1) { $('div.myDiv').html(response); }
			else { $('img.loader').replaceWith(response); }
			count++;
			if (count <= maxCount) {
				sendRequest(count, maxCount, formData);
			}
			}});

	return false;

}

/* Watermark and onClick handlers on DOM load */
$(document).ready(function(){
	/*jQuery(function($){
	       $('.submitText').Watermark(watermark);
	});*/
	urlparam = getURLParameter('q');
	if (urlparam != 'null') {
		urlparam = urlparam.split('+').join(' ');
		if (urlparam == 'random') {
			$('.submitText').val('');
		} else {
			$('.submitText').val(urlparam);
		}
		jsonParse();
	}
	
	$('a[href=#topOfPage]').click(function(){
		$('html, body').animate({scrollTop:0});
		$('.submitText').val('');
		$('.submitText').focus();
	        return false;
	});


    		/*$(".submitBtn").attr("disabled", "true");
		$(".submitText").keyup(function(){
	        if ($(this).val() != "") {
        	    $(".submitBtn").removeAttr("disabled");
	        } else {
	            $(".submitBtn").attr("disabled", "true");
	        }
	       });*/
});
