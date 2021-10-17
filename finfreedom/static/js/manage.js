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

function update_company_selector(type_of_acc){
    console.log("Type of Acc: ", type_of_acc);
    var profile_id = $("#profile_id").text();
    console.log("Profile ID: ", profile_id);
    $.ajax(
        {
            method: "POST",
            url: "/get_company_by_type_and_user/",
            dataType: "json",
            data:{
                "csrfmiddlewaretoken": csrftoken,
                "type_of_acc": type_of_acc,
                "profile_id": profile_id,
            },
            success: function (data, textStatus, jqXHR) {
                console.log("response: ", data);
                $("#company_name").prop('disabled', false);
                $("#company_name").empty();
                $("#company_name").append('<option selected value="">Required</option>');
                for(var index in data['results'] ){
                    console.log(data['results'][index]);
                    $("#company_name").append('<option value="' + data['results'][index]['value'] + '">' + data['results'][index]['text'] + '</option>')
                }
                
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: ", textStatus);
            }
        }
    );
}

function create_new_transaction(){
    var json_data = {
        "transaction_info":
        {
            "account_id": $('#company_name').val().trim(),
            "amount": $('#transaction_amount').val().trim(),
            "date_occured": $('#date_occured').val().trim(),
            "name_of_recipient": $('#name_of_recipient').val().trim(),
        },
    }
    $.ajax(
        {
            method: "POST",
            url: "/create_transaction/",
            dataType: "json",
            data:{
                "csrfmiddlewaretoken": csrftoken,
                "data": JSON.stringify(json_data),
            },
            success: function (data, textStatus, jqXHR) {
                if(data['response'] == "success"){
                    clear_transaction_form(); 
                    $("#success_message").text(data['message'])
                    $("#success_modal").modal("show");
                }else{
                    console.log("hit the error")
                    $("#error_message").text(data['message'])
                    $("#error_modal").modal("show");
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: ", textStatus);
            }
        }
    );
}


function clear_transaction_form(){
    $("#type_of_account").val("");
    $("#company_name").empty();
    $("#company_name").append('<option selected value="">Required</option>')
    $("#company_name").prop("disabled", true);
    $("#name_of_recipient").val("");
    $("#date_occured").val("");
    $("#transaction_amount").val("");
}


$(document).ready(function(){
});