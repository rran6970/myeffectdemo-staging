$(function(){  
    $(".btn").button();
	$(".dropdown-toggle").dropdown();
	$(".timepicker").timepicker();
	$(".datepicker").datepicker({
		'format': 'yyyy-mm-dd'
	}).on('changeDate', function(event){
    	$(this).datepicker('hide');
  	});

    $(".notification-link").on('click', ajaxReadNotification);
    $(".notification-mark-read").on('click', ajaxQuickReadNotification);
    $(".notification-mark-unread").on('click', ajaxQuickUnreadNotification);

    $(".popup-image").colorbox({
        speed: 250,
        inline: true, 
        scrolling: true,
        opacity: 0.7,
        photo: true,
        fadeOut: 200
    });

    $(".popup-600").colorbox({
        speed: 250,
        width: "600px",
        height: "500px",
        inline: true, 
        scrolling: true,
        opacity: 0.7,
        fadeOut: 200
    });

    $(".popup-200").colorbox({
        speed: 250,
        width: "200px",
        height: "500px",
        inline: true, 
        scrolling: true,
        opacity: 0.7,
        fadeOut: 200
    });

    $("[rel=tooltip]").tooltip({ 
        "html" : true,
        "animation" : true,
        "delay" : { show: 300, hide: 200 }
    });
    $(".popover-btn").popover({ placement:"right", html:true });  

    // $('form.participation-forms').on('submit', ajaxParticipation);
    $('form.participation-forms').on('submit', ajaxCheckInCheckOut);
	$('form.members-forms').on('submit', ajaxApproveMember);

    $("#id_team_type").on("change", function(e){
        if ($(this).val() == "representing")
        {
            $("#clean-team-group-td").fadeIn();
        }
        else
        {
            $("#clean-team-group-td").fadeOut();   
        }
    });
});

function ajaxQuickUnreadNotification(e)
{
    var element = $(this);
    var form = element.closest("form");

    $.ajax({
        type: form.attr('method'),
        url: '/notifications/quick-unread/',
        data: form.serialize(),
        success: function (data) {
            element.closest("li").addClass("unread");

            var notification_number = parseInt($("#notification-container").html());
            notification_number = notification_number + 1;
            $("#notification-container").html(notification_number);
        },
        error: function(data) {}
    });

    e.preventDefault();
    return false;
}

function ajaxQuickReadNotification(e)
{
    var element = $(this);
    var form = element.closest("form");

    $.ajax({
        type: form.attr('method'),
        url: '/notifications/quick-read/',
        data: form.serialize(),
        success: function (data) {
            element.closest("li").removeClass("unread");

            var notification_number = parseInt($("#notification-container").html());
            notification_number = notification_number - 1;
            $("#notification-container").html(notification_number);
        },
        error: function(data) {}
    });

    e.preventDefault();
    return false;
}

function ajaxReadNotification(e)
{
    var element = $(this);
    var form = element.closest("form");

    url = element.attr("href");

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            window.location = url;
        },
        error: function(data) {
            window.location = url;
        }
    });

    e.preventDefault();
    return false;
}

function ajaxCheckInCheckOut(e)
{       
    var form = $(this);

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            btn = form.find("#confirm-btn");

            if (btn.val() == "Check In")
            {
                btn.val("Check Out");
                btn.addClass("dark");
            }
            else if (data)
            {
                btn.before(data + " Hours");
                btn.hide();
            }
            else
            {
                btn.val("Check In");
            }
        },
        error: function(data) {}
    });
    e.preventDefault();
    return false;
}

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