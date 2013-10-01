$(function(){  
	$('.dropdown-toggle').dropdown();
	$(".timepicker").timepicker();
	$(".datepicker").datepicker({
		'format': 'yyyy-dd-mm'
	}).on('changeDate', function(event){
    	$(this).datepicker('hide');
  	});
    $(".popover-btn").popover({ placement:"bottom" });  

	$('form.participation-forms').on('submit', ajaxParticipation);
});

function ajaxParticipation(e)
{		
	var form = $(this);

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            hidden_field = form.find("#participated");
            participated_btn = form.find("#confirm-btn");

            if(hidden_field.val() == "true")
            {
	            hidden_field.val("false");
    	        participated_btn.val("Unconfirm");
    	        participated_btn.addClass("dark");
    	    }
    	    else
    	    {
				hidden_field.val("true");
    	        participated_btn.val("Confirm");
    	        participated_btn.removeClass("dark");
    	    }
        },
        error: function(data) {}
    });
    e.preventDefault();
    return false;
}