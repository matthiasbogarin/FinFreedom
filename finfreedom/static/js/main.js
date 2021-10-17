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
    console.log("email changed: ", email);
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
                console.log("response: ", data);
                if(data['exists']){
                    console.log("Alert User that Email already exists and clear the email input");
                    message = "This email already exists in our system, you can reset your password or enter another email.";
                    $('#alert_email_exists').html('<div class="text-center alert alert-warning alert-dismissible mt-3" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
                    $("#email").val("");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: ", textStatus);
            }
        }
    );
    //run a ajax call to the api to get the response if this email already exists in the system.
}

function check_if_passwords_match(){
    console.log("Password: ", $("#new_password").val());
    console.log("Verify Password: ", $("#verify_password").val());
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
                console.log("response: ", data);
                if(!data['matched']){
                    message = "Password's did not match, please try again.";
                    $('#password_dont_match').html('<div class="text-center alert alert-danger alert-dismissible mt-3" role="alert">' + message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
                    $("#new_password").val("");
                    $("#verify_password").val("");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: ", textStatus);
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
        console.log("Validated");
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
                console.log("data: ", data);
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
                console.log(errorThrown);                $("#create_account_modal").modal('hide');
                $("#create_account_modal").modal('hide');
                $("#error_message").text(data['message'])
                $("#error_modal").modal("show");
            }
        });
    }
}




$(document).ready(function(){
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
                error.insertAfter(element);
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

