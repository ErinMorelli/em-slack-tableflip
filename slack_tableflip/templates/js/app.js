(function() {
	
	$('.close').on('click', function(e) {
		e.preventDefault();
		$('.alert').remove();
	});
	
})();