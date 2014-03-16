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

    $(".youtube-popup").colorbox({iframe:true, innerWidth:640, innerHeight:390});

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

    // Search box
    var search_box = $('#search-box');
    $('#search-box')
        .data('timeout', null)
        .keyup(function(){
            clearTimeout($(this).data('timeout'));
            $(this).data('timeout', setTimeout(function(e){
                showSearchResults(e, search_box)
            }, 500));
    });
    $("#national-challenge-checkbox").on("click", function(e){
        showSearchResults(e, search_box);
    });
    
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

    // Enable question 5 if there is an answer selected
    var question_5 = $("input[name='question_5']");

    if (question_5.is(':checked'))
    {
        question_5.prop('disabled', false);
    }

    // Challenge survey enable/disable question 5 based on answer from question 4
    $("#id_question_4_3").on("click", enabledDisableQuestion5);

    // Challenge survey update score in real time
    $("input[name^='question_']").on("click", ajaxChallengeSurveyUpdateScore);

    twttr.events.bind('follow', followTwitterCallback);
});


function showSearchResults(e, search_box)
{
    var search_result_dropdown = $(".search-result-dropdown");
    var search_result_list = $(".search-result-dropdown ul");
    var value = search_box.val();
    var national_challenges = $("#national-challenge-checkbox").is(':checked');

    var challenge_url = '/challenges/?q=';
    $("#view-all-challenges").attr('href', challenge_url + value);
    $("#search-form").attr('action', challenge_url + value);

    if(value || national_challenges == true)
    {
        $.ajax({
            type: 'GET',
            url: '/challenges/search/',
            data: { 
                'q': value,
                'national_challenges': national_challenges
            },
            beforeSend: function()
            {
                search_result_dropdown.fadeIn("fast");
            },
            success: function (data) {
                search_result_list.empty();

                if (data != "False")
                {
                    var json = JSON.parse(data);                

                    for (var key in json){
                        var id = key;
                        var title = json[key];
                        search_result_list.append("<li><a href='/challenges/" + id + "/'>" + title + "</a></li>")
                    }    
                }
                else
                {
                    search_result_list.append("<li><a>No results found</a></li>")
                }
                
            },
            error: function(data) {
                console.log(data);
            }
        });
    }
    else
    {
        search_result_dropdown.fadeOut("fast");
    }
}

function followTwitterCallback(e)
{
    $.ajax({
        type: 'POST',
        url: '/users/follow-twitter/',
        data: { 'csrfmiddlewaretoken': 'EkBkAdchkoJkyRmajrCvW1E3PoT99rmh' },
        success: function (data) {
            location.reload();
        },
        error: function(data) {
            console.log(data)
        }
    });
}

var challenge_survey_score = 0;

function ajaxChallengeSurveyUpdateScore(e)
{
    var element = $(this);

    $.ajax({
        type: 'GET',
        url: '/challenges/survey-update-score/',
        data: { 'aid': element.val() },
        success: function (data) {
            if (element.is(':checked'))
                challenge_survey_score += parseInt(data);
            else
                challenge_survey_score -= parseInt(data);

            $("#sign-leaderboard #your-points .points").html(challenge_survey_score);
        },
        error: function(data) {}
    });
}

function enabledDisableQuestion5(e)
{
    var checkbox = $(this)

    if (checkbox.is(':checked'))
        $("input[name='question_5']").prop('disabled', false);
    else
        $("input[name='question_5']").prop('disabled', 'disabled');
}

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
            element.removeClass("notification-mark-unread");
            element.addClass("notification-mark-read");
            element.text("Make unread");

            var notification_number = parseInt($("#notification-container span").html());
            notification_number = notification_number + 1;
            $("#notification-container span").html(notification_number);
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
            element.removeClass("notification-mark-read");
            element.addClass("notification-mark-unread");
            element.text("Make read");

            var notification_number = parseInt($("#notification-container span").html());
            notification_number = notification_number - 1;

            if (notification_number == 0)
                $("#notification-container span").hide();   
            else
                $("#notification-container span").html(notification_number);
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

            if (data)
            {
                btn.before(data);
                btn.hide();
            }
            else if (btn.val() == "Check In")
            {
                btn.val("Check Out");
                btn.addClass("dark");
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