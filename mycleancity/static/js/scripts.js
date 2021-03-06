$(function(){  
    var auto_complete_callback = function (request, response) {
        $.ajax({
          url: communities_search_url + request.term,
          success: function (data) {
            var suggestions = []
            var items = eval(data);
            for(var i = 0; i < items.length; i++){
              suggestions.push(items[i].name);
            }
            if(suggestions.length == 0){
              response(["No suggestions"]);
            }else{
              response(suggestions);
            }
          }
        });
    }

    $("#community-td input").autocomplete({source: auto_complete_callback});

    $("#team-search-box").on('input', function() {
      var $team_rows = $("tr", $("#team-list-table"));
      var search_expr = $(this).val();
      $team_rows.each(function () {
        var team_name = $(".team-name-wrapper", $(this)).html();
        if(team_name.toLowerCase().indexOf(search_expr.toLowerCase()) != -1){
          $(this).show();
        }else{
          $(this).hide();
        }
      });
    });

    $(".btn").button();

    $("[rel='tooltip']").tooltip();

    // Number field validator mask
    // $(".number-field").inputmask("9{3}");

    // Phone number vaidator mask
    var $phoneNumber = $(".phone-number");
    if($phoneNumber.length){
        $phoneNumber.inputmask("9{1,3}-9{1,3}-9{1,4}");
    }

    // Javascript to enable link to tab
    var url = document.location.toString();
    if (url.match('#')) {
        $('.nav-tabs a[href=#'+url.split('#')[1]+']').tab('show') ;
    } 

    // Change hash for page-reload
    $('.nav-tabs a').on('shown', function (e) {
        window.location.hash = e.target.hash;
    });

    // Prevents selecting of checkbox to close search dropdown
    $("input[type='checkbox']").on("click", function(){

    });

    $("[data-toggle='tab']").on("click", function(){
        var link = $(this);
        var url = link.attr("href");

        window.history.pushState("string", "Title", url);
    });

	$(".dropdown-toggle").dropdown();
	$(".timepicker").timepicker({
        'defaultTime': false,
        'showMeridian': false
    });
	$(".datepicker").datepicker({
		'format': 'yyyy-mm-dd'
	}).on('changeDate', function(event){
    	$(this).datepicker('hide');
  	});

    $(".notification-link").on('click', ajaxReadNotification);
    $(".notification-mark-read").on('click', ajaxQuickReadNotification);
    $(".notification-mark-unread").on('click', ajaxQuickUnreadNotification);

    $('.dropdown-menu input, .dropdown-menu select, .dropdown-menu label').click(function(e) {
        e.stopPropagation();
    });
    
    $("body").click(function(){
      $(".search-result-dropdown").fadeOut()
    });

    $(".iframe").colorbox({
        //open:true, 
        iframe:true, 
        width:"80%", 
        height:"80%", 
        overlayClose: false,
        escKey: false
    });

    $(".contact_for_license").colorbox({
        iframe:true, 
        width:"420px", 
        height:"90%"
    });

        $(".download_file_box").colorbox({
        iframe:true,
        width:"420px",
        height:"50%"
    });
    // $("#relaunch-signup-link").colorbox({
    //     iframe: true,
    //     open: true,
    //     inline: true, 
    //     speed: 250,
    //     width: "80%",
    //     height: "80%",
    //     scrolling: true,
    //     opacity: 0.7,
    //     fadeOut: 200,
    //     overlayClose: false,
    //     escKey: false
    // });

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
            $("#city-search-box").val("");
            $("#tag-search-box").val("");
            $("#title-search-box").val("");
            $("#category-search-selection").val("");
            clearTimeout($(this).data('timeout'));
            $(this).data('timeout', setTimeout(function(e){
                showSearchResults(e);
            }, 500));
    });
    $('.advanced-search-box')
        .data('timeout', null)
        .keyup(function(){
            $('#search-box').val("");
            clearTimeout($(this).data('timeout'));
            $(this).data('timeout', setTimeout(function(e){
                showSearchResults(e);
            }, 500));
    });

    $("#category-search-selection").on("change", function(e){
        $('#search-box').val("");
        showSearchResults(e);
    });

    $("#national-challenge-checkbox").on("click", function(e){
        showSearchResults(e);
    });
    $("#clean-team-only-checkbox").on("click", function(e){
        showSearchResults(e);
    });
    $("#virtual-action-checkbox").on("click", function(e){
        showSearchResults(e);
    });
    
    // $('form.participation-forms').on('submit', ajaxParticipation);
    $('form.participation-forms').on('submit', ajaxCheckInCheckOut);
	$('form.members-forms').on('submit', ajaxApproveMember);
    $('form.participant_action-forms').on('submit', ajaxApproveParticipant);

    // Posted Challenge host is Change Team
    $("#id_host_is_clean_team").on("click", hostIsCleanTeam);

    $("#id_clean_ambassadors").on("change", populateMainContactInfo);

    // Challenge survey update score in real time
    $("input[name^='question_']").on("click", ajaxChallengeSurveyUpdateScore);

    var twttrBindFcn = function () {
        /*  Try to bind every second until the twttr variable is defined */
        if(!(typeof twttr === 'undefined')){
            twttr.events.bind('follow', followTwitterCallback);
        }else{
            setTimeout(twttrBindFcn, 1000);
        }
    }
    twttrBindFcn();

    // Change Team invite button
    $("#send-invite-form").on("submit", function(){
        var button = $("#send-invite-form").find("#send-invite-button");
        button.prop('disabled', 'disabled');
        button.val('Sending...');

        return true;
    });

    $(".resend-invite-form").on("submit", resendInvite);

    // Show post message box on Change Team Profile
    $("#show-post-message-box").on("focus", function(){
        $("#post-message-container").fadeIn(500).show();
        $("#post-message-container form textarea").focus();
    });

    $("#post-message-container form textarea").on("blur", function(){
        $("#post-message-container").fadeOut(500);
    });

    $("#post-message-container form").on("submit", postMessage);

});

$("#create_team_rdo").on("click", function(e){
    $("#org_type_tr").hide();
    $("#registered_number_tr").hide();
    $("#category_tr").hide();
    $("#number_of_users_tr").hide();
    $("#submit_org_tr").hide();
    $("#submit_tr").fadeIn();
});

$("#representing_rdo").on("click", function(e){
    $("#org_type_tr").fadeIn();
    if($("#id_org_type").val() == "nonprofit_charity"){
        $("#submit_org_tr").hide();
        $("#registered_number_tr").fadeIn();
        $("#category_tr").fadeIn();
        $("#submit_tr").fadeIn();
    }else{
        $("#submit_tr").hide();
        $("#number_of_users_tr").fadeIn();
        $("#submit_org_tr").fadeIn();
    }
});

$("#id_org_type").on("change", function(e){
    if($(this).val() == "nonprofit_charity"){
        $("#number_of_users_tr").hide();
        $("#submit_org_tr").hide();
        $("#registered_number_tr").fadeIn();
        $("#category_tr").fadeIn();
        $("#submit_tr").fadeIn();
    }
    else{
        $("#category_tr").hide();
        $("#registered_number_tr").hide();
        $("#submit_tr").hide();
        $("#number_of_users_tr").fadeIn();
        $("#submit_org_tr").fadeIn();
    }
});

$("#edit-social-connection").on("click", function(e){
    if($(this).text()=="Edit"){
        $(".social-login-cross").css("display", "block");
        $(".social-login-add").css("opacity", "1");
        $(this).text("Cancel");
    }else{
        $(".social-login-cross").css("display", "none");
        $(".social-login-add").css("opacity", "0");
        $(this).text("Edit");
    }
});

$("#clean-team-members-list #id_role").on("change", function(e){
    if ($(this).val() == "organization")
    {
        window.location.replace("/clean-team/invite-org/");
    }
    else if ($(this).val() == "friend"){
        $("#invite-heading").html("Invite Friends");
        $("#invite-subtitle").html("Invite your friends to join MyEffect.");
    }
    else if ($(this).val() == "agent"){
        $("#invite-heading").html("Invite Friends");
        $("#invite-subtitle").html("Invite your friends to support your Change Team.");
    }
    else if ($(this).val() == "leader"){
        $("#invite-heading").html("Invite Leader");
        $("#invite-subtitle").html("Invite a leader to become a manager of your Change Team.");
    }
});

$("#invite_id_role").on("change", function(e){
    if ($(this).val() != "organization")
    {
        window.location.replace("/clean-team/invite/?role=" + $(this).val());
    }
});

function resendInvite(e)
{
    var form = $(this);
    var button = $(this).find(".resend-invite-button");
    button.after("<span class='resend-sent'>Sent</span>");
    button.hide();

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            
        },
        error: function(data) {
            console.log(data);
        }
    });

    return false;
}

function populateMainContactInfo(e)
{
    var uid = $(this).val();
    
    $.ajax({
        type: 'GET',
        url: '/users',
        data: { 
            'uid': uid,
        },
        success: function (data) {
            var json = JSON.parse(data);                

            for (var key in json){
                var user = json[key]["fields"];
                var first_name = user.first_name
                var last_name = user.last_name
                var email = user.email

                $("#id_contact_first_name").val(first_name);
                $("#id_contact_last_name").val(last_name);
                $("#id_contact_email").val(email);
            }    
        },
        error: function(data) {
            console.log(data);
        }
    });
}

function postMessage(e)
{
    var form = $(this);
    var textfield = form.find("textarea");

    var message = textfield.val();

    $.ajax({
        type: 'POST',
        url: '/clean-team/post-message-ajax',
        data: form.serialize(),
        success: function (data) {
            textfield.val("");
            $("#post-message-container").hide().fadeOut(1000);

            var post = $(data);
            var posts = $("#wall .posts");

            posts.prepend(post);
        },
        error: function(data) {
            console.log(data);
        }
    });

    return false;
}

function showSearchResults(e)
{
    var search_result_dropdown = $(".search-result-dropdown");
    var search_result_list = $(".search-result-dropdown ul");
    var value = $("#search-box").val();
    var city = $("#city-search-box").val();
    var tag = $("#tag-search-box").val();
    var title = $("#title-search-box").val();
    var cat = $("#category-search-selection").val();
    var national_challenges = $("#national-challenge-checkbox").is(':checked');
    var clean_team_only = $("#clean-team-only-checkbox").is(':checked');
    var virtual_action = $("#virtual-action-checkbox").is(':checked');

    var challenge_url = '/challenges/?q=' + value;

    if (city != "")
    {
        challenge_url += '&city='+ city;
    }

    if (tag != "")
    {
        challenge_url += '&tag='+ tag;
    }

    if (title != "")
    {
        challenge_url += '&title='+ title;
    }

    if (cat != "")
    {
        challenge_url += '&cat='+ cat;
    }

    if (national_challenges != "")
    {
        challenge_url += '&national_challenges=on';
    }

    if (clean_team_only != "")
    {
        challenge_url += '&clean_team_only=on';
    }

    if (virtual_action != "")
    {
        challenge_url += '&virtual_action=on';
    }

    $("#view-all-challenges").attr('href', challenge_url);
    $("#search-form").attr('action', challenge_url);

    if(value || city || tag || title || cat || national_challenges == true || clean_team_only == true || virtual_action == true)
    {
        $.ajax({
            type: 'GET',
            url: '/challenges/search/',
            data: { 
                'q': value,
                'city': city,
                'tag': tag,
                'title': title,
                'cat': cat,
                'national_challenges': national_challenges,
                'clean_team_only': clean_team_only,
                'virtual_action': virtual_action
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
                        // var id = key;
                        var title = json[key];
                        search_result_list.append(title)
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
    var csrf_token = $("input[name='csrfmiddlewaretoken']").val();

    $.ajax({
        type: 'POST',
        url: '/users/follow-twitter/',
        data: { 'csrfmiddlewaretoken': csrf_token },
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

function hostIsCleanTeam(e)
{
    var checkbox = $(this);

    if (checkbox.is(':checked'))
    {
        var clean_team_name = $("#pre_loaded_clean_team_name").val();
        var first_name = $("#pre_loaded_first_name").val();
        var last_name = $("#pre_loaded_last_name").val();
        var email = $("#pre_loaded_email").val();
        var contact_phone = $("#pre_loaded_contact_phone").val();

        $("#id_organization").val(clean_team_name);
        $("#id_organization").attr("readonly", "readonly");

        $("#id_contact_first_name").val(first_name);
        $("#id_contact_first_name").attr("readonly", "readonly");

        $("#id_contact_last_name").val(last_name);
        $("#id_contact_last_name").attr("readonly", "readonly");

        $("#id_contact_email").val(email);
        $("#id_contact_email").attr("readonly", "readonly");

        $("#id_contact_phone").inputmask('remove');
        $("#id_contact_phone").val(contact_phone);
    }
    else
    {
        $("#id_organization").val("");
        $("#id_organization").removeAttr("readonly");

        $("#id_contact_first_name").val("");
        $("#id_contact_first_name").removeAttr("readonly");

        $("#id_contact_last_name").val("");
        $("#id_contact_last_name").removeAttr("readonly");

        $("#id_contact_email").val("");
        $("#id_contact_email").removeAttr("readonly");

        $("#id_contact_phone").val("");
        $("#id_contact_phone").inputmask("9{1,3}-9{1,3}-9{1,4}");
    }    
}

function showParticipatingMessageBox(e)
{
    $("#participate-btn").hide();
    $("#participating-message-box").fadeIn();
    $("#id_send_btn").focus();
}

function participatePeriodValidate(e)
{
    if ($('input[name=subscribe]:checked').val()=="period") {
        var re = /^\d{4}\-\d{2}\-\d{2}$/;
        var start_date=$('#id_start_date').val();
        var end_date=$('#id_end_date').val();
        if (start_date=='' || end_date=='') {
            $('#date-period-error').text('Date value incomplete');
            return false;
        }
        else if (!start_date.match(re) || !end_date.match(re)) {
            $('#date-period-error').text('Date format sould be like 2015-04-27');
            return false;
        }
        var date_start = new Date(start_date.substring(0, 4), parseInt(start_date.substring(5, 7))-1, start_date.substring(8, 10));
        var date_end = new Date(end_date.substring(0, 4), parseInt(end_date.substring(5, 7))-1, end_date.substring(8, 10));
        var now = new Date();
        var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        if (date_start > date_end) {
            $('#date-period-error').text('End date must equal or after start date');
            return false;
        }
        else if (today > date_start) {
            $('#date-period-error').text('Start date must equal or after today');
            return false;
        }
    }
    $('#date-period-error').text('');
    return true;
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
    button = form.find("#confirm-btn");

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        beforeSend: function() {            
            var loading = $("<img class='loading' src='" + window.static_url + "images/loading-25x25.gif' />");
            button.before(loading);
            button.hide();
        },
        success: function (data) {            
            if (data)
            {
                form.find(".loading").hide();
                button.before(data);
                button.hide();
            }
            else if (button.val() == "Check In")
            {
                form.find(".loading").hide();
                button.show();
                button.val("Check Out");
                button.addClass("dark");
            }
            else if (button.val() == "Add")
            {
                button.before(data);
                button.hide();
            }
            else
            {
                form.find(".loading").hide();
                button.show();
                button.val("Check In");
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
            location.reload();
        },
        error: function(data) {alert("some thing is wrong...")}
    });
    e.preventDefault();
    return false;
}

function ajaxApproveParticipant(e)
{       
    var form = $(this);

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            location.reload();
        },
        error: function(data) {alert("some thing is wrong...")}
    });
    e.preventDefault();
    return false;
}
