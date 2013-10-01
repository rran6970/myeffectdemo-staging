$(function(){  
	$('.dropdown-toggle').dropdown();
	$(".timepicker").timepicker();
	$(".datepicker").datepicker({
		'format': 'yyyy-dd-mm'
	}).on('changeDate', function(event){
    	$(this).datepicker('hide');
  	});
});