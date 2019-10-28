$(function() {
	$( "#PINform" ).draggable();
});

function addNumber(e){
	var v = $( "#PINbox" ).val();
	if (v.length < 19) {
		if (v.replace(/ /gi, '').length % 4 == 0 && v) {
				$( "#PINbox" ).val( v + ' ' + e.value);
		}
		else {
			$( "#PINbox" ).val( v + e.value );
		}
	}
}

function addPin(e){
	var v = $( "#PINbox" ).val();
	if (v.length < 4) {
			$( "#PINbox" ).val( v + e.value );
	}
}

function addCash(e){
	var v = $( "#PINbox" ).val();
	if (v.length < 12) {
			$( "#PINbox" ).val( v + e.value );
	}
}

function clearForm(e){
	$( "#PINbox" ).val( "" );
}
