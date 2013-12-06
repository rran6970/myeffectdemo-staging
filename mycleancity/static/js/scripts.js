$(function(){  
	$('.dropdown-toggle').dropdown();
	$(".timepicker").timepicker();
	$(".datepicker").datepicker({
		'format': 'yyyy-mm-dd'
	}).on('changeDate', function(event){
    	$(this).datepicker('hide');
  	});
    $(".popover-btn").popover({ placement:"right", html:true });  

    $('form.participation-forms').on('submit', ajaxParticipation);
	$('form.members-forms').on('submit', ajaxApproveMember);
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

function ajaxApproveMember(e)
{		
	var form = $(this);

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            hidden_field = form.find("#action");
            action_btn = form.find("#action-btn");

            if(hidden_field.val() == "approve")
            {
	            hidden_field.val("remove");
    	        action_btn.val("Remove");
    	        action_btn.addClass("dark");

                action_btn.closest("td").prev().text("approved");
    	    }
    	    else if(hidden_field.val() == "remove")
    	    {
                action_btn.hide();
                action_btn.closest("td").prev().text("removed");
    	    }
        },
        error: function(data) {}
    });
    e.preventDefault();
    return false;
}