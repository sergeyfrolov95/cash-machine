$(function() {
	$( "#PINform" ).draggable();
});
/*
function addNumber(e){
	var v = $( "#PINbox" ).val();
	if (v.length < 20) {
		if (v.replace('-', '').length % 4 == 0 && v.length) {
				$( "#PINbox" ).val( v + '-' + e.value );
		}
		else {
			$( "#PINbox" ).val( v + e.value );
		}
	}
}
*/
function addNumber(e){
	var v = $( "#PINbox" ).val();
	if (v.length < 16) {
			$( "#PINbox" ).val( v + e.value );
	}
}
function clearForm(e){
	$( "#PINbox" ).val( "" );
}
function submitForm(e) {
	if (e.value == "") {
		alert("Enter a PIN");
	} else {
		alert( "Your PIN has been sent! - " + e.value.replace('-', '') );
		data = {
			pin: e.value.replace('-', '')
		}

		$( "#PINbox" ).val( "" );
	};
};
