// function populate_edit_account(e){
//     var account_id = $(e).closest('tr').find('td:nth-child(2)').text();
//     var data = $(e).closest('tr')[0].cells;
//     header_list = ['type_of_account', 'company_name', 'account_name', 'expiration_date', 'amount_on_card', 'credit_on_card']
//     for(var i = 2; i < data.length; i++){

//         console.log(data[i].innerText);
//     }

// }


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


function delete_account(e){
    var account_id = $(e).closest('td').siblings('.account_id_class').text();
    var json_data = {
        "profile_id": $("#profile_id").text(),
        "account_id": account_id,
    }
    $.ajax(
        {
            method: "POST",
            url: "/delete_account/",
            dataType: "json",
            data:{
                "csrfmiddlewaretoken": csrftoken,
                "data": JSON.stringify(json_data),
            },
            success: function (data, textStatus, jqXHR) {
                if(data['response'] == "success"){
                    clear_account_form(); 
                    $("#success_message").text(data['message'])
                    $("#success_modal").modal("show");
                }else{
                    $("#error_message").text(data['message'])
                    $("#error_modal").modal("show");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("Error: ", textStatus);
            }
        }
    );
    $("#confirm_delete_modal").modal('hide');
}

function submit_new_account(){
    var json_data = {
        "account_info":
        {
            "type_of_account": $('#type_of_account').val(),
            "company_name": $("#company_name").val(),
            "account_name": $("#account_name").val(),
            "card_on_name": $("#card_on_name").val(),
            "card_number": $("#card_number").val(),
            "expiration_date": $("#expiration_date").val(),
            "security_code": $("#security_code").val(),
            "payment_day": $("#payment_day").val(),
            "amount_on_card": $("#amount_on_card").val(),
            "credit_on_card": $("#credit_on_card").val(),
            "profile_id": $("#profile_id").text()
        }
    }
    if($("#new_account_form").valid()){
        $.ajax(
            {
                method: "POST",
                url: "/submit_new_account/",
                dataType: "json",
                data:{
                    "csrfmiddlewaretoken": csrftoken,
                    "profile_id": $("#profile_id").text(),
                    "data": JSON.stringify(json_data),
                },
                success: function (data, textStatus, jqXHR) {
                    if(data['response'] == "success"){
                        clear_account_form(); 
                        $("#success_message").text(data['message'])
                        $("#success_modal").modal("show");
                    }else{
                        $("#error_message").text(data['message'])
                        $("#error_modal").modal("show");
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error("Error: ", textStatus);
                }
            }
        );
    }
}



function clear_account_form(){
    $("#type_of_account").val("");
    $("#company_name").val("");
    $("#account_name").val("");
    $("#card_on_name").val("");
    $("#card_number").val("");
    $("#expiration_date").val("");
    $("#security_code").val("");
    $("#payment_day").val("");
    $("#amount_on_card").val("");
    $("#credit_on_card").val("");
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
        $("#new_account_form").validate({
            rules: {
                type_of_account: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                company_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                account_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                card_on_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                expiration_date: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                security_code: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                payment_day: {
                    required: false,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                amount_on_card: {
                    required: false,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                credit_on_card: {
                    required: false,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
            }
        });
    });
});