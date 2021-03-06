function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function check_if_email_exist(email){
    $.ajax(
        {
            method: "GET",
            url: "finfreedom_api/check_if_email_exists/",
            dataType: "json",
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            data:{
                "email": email,
            },
            success: function (data, textStatus, jqXHR) {
                if(data['exists']){
                    message = "This email already exists in our system, you can reset your password or enter another email.";
                    $('#alert_email_exists').html('<div class="text-center alert alert-warning alert-dismissible mt-3" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
                    $("#email").val("");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("Error: ", textStatus);
            }
        }
    );
    //run a ajax call to the api to get the response if this email already exists in the system.
}

function check_if_passwords_match(){
    $.ajax(
        {
            method: "GET",
            url: "finfreedom_api/check_if_passwords_match/",
            dataType: "json",
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            data:{
                "new_password": $("#new_password").val(),
                "verify_password": $("#verify_password").val(),
            },
            success: function (data, textStatus, jqXHR) {
                if(!data['matched']){
                    message = "Password's did not match, please try again.";
                    $('#password_dont_match').html('<div class="text-center alert alert-danger alert-dismissible mt-3" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
                    $("#new_password").val("");
                    $("#verify_password").val("");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("Error: ", textStatus);
            }
        }
    );
    //run a ajax call to the api to get the response if this email already exists in the system.
}

function submit_new_account(){
    var json_data = {
        "profile_info":
        {
            "email": $('#email').val().trim(),
            "first_name": $('#first_name').val().trim(),
            "last_name": $('#last_name').val().trim(),
            "username": $('#new_username').val().trim(),
            "password": $("#new_password").val().trim(),
        },
        "employer_info": 
        {
            "employer_name": $('#employer_name').val().trim(),
            "position": $('#position').val().trim(),
            "salary": $('#salary').val().trim(),
            "income_date": $('#income_date').val().trim(),
            "income_frequency": $('#income_frequency').val().trim(),
        }
    }
    if($("#create_account_form").valid()){
        $.ajax({
            method: "POST",
            url: "create_account/",
            dataType: "json",
            
            data: {
                "csrfmiddlewaretoken": csrftoken,
                "data": JSON.stringify(json_data),
            },
            beforeSend: function () {
                
            },
            success: function (data, textStatus, jqXHR) {
                $("#create_account_modal").modal('hide');
                if(data['response'] == "success"){
                    $("#success_message").text(data['message'])
                    $("#success_modal").modal("show");
                }else{
                    $("#error_message").text(data['message'])
                    $("#error_modal").modal("show");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error(errorThrown);                $("#create_account_modal").modal('hide');
                $("#create_account_modal").modal('hide');
                $("#error_message").text(data['message'])
                $("#error_modal").modal("show");
            }
        });
    }
}




$(document).ready(function(){
    console.log($("#page").text());
    console.log($("#page").text() == "Account");
    if($("#page").text() == "Account"){
        $("#manage_active").hide();
        $("#profile_active").hide();
        $("#transaction_active").hide();
        $("#account_inactive").hide();
        
        $("#account_active").show();
        $("#manage_inactive").show();
        $("#profile_inactive").show();
        $("#transaction_inactive").show();
    }else if($("#page").text() == "Manage"){
        $("#account_active").hide();
        $("#profile_active").hide();
        $("#transaction_active").hide();
        $("#manage_inactive").hide();
        
        $("#manage_active").show();
        $("#account_inactive").show();
        $("#profile_inactive").show();
        $("#transaction_inactive").show();
    } else if($("#page").text() == "Transaction"){
        $("#account_active").hide();
        $("#manage_active").hide();
        $("#profile_active").hide();
        $("#transaction_inactive").hide();
        $("#transaction_active").show();
        $("#account_inactive").show();
        $("#manage_inactive").show();
        $("#profile_inactive").show();
    }else if($("#page").text() == "Profile"){
        $("#account_active").hide();
        $("#manage_active").hide();
        $("#transaction_active").hide();
        $("#profile_inactive").hide();
        $("#profile_active").show();
        $("#account_inactive").show();
        $("#manage_inactive").show();
        $("#transaction_inactive").show();
    }

    $(function () {
        $.validator.setDefaults({
            errorClass: 'invalid-feedback',
            highlight: function (element) {
                $(element)
                    .closest('.form-control')
                    .addClass('is-invalid');
            },
            unhighlight: function (element) {
                $(element)
                    .closest('.form-control')
                    .removeClass('is-invalid');
            },
            errorPlacement: function (error, element) {
                if(element[0].id == "salary"){
                    error.appendTo(element.parent('.input-group'));
                }else{
                    error.insertAfter(element);
                }
            }
        });
        $("#create_account_form").validate({
            rules: {
                email: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                first_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                last_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                new_username: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                new_password: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                verify_password: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                employer_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                position: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                salary: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                income_date: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                income_frequency: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
            }
        });
    });
});

