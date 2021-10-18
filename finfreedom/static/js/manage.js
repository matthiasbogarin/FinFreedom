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

function update_company_selector(type_of_acc, selector){
    console.log("hit the update company selector func");
    console.log(type_of_acc, " : ", selector);
    var profile_id = $("#profile_id").text();
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
                console.log($("#tab_name").text() == "expense");
                if($("#tab_name").text() == "expense"){
                    $("#company_name").prop('disabled', false);
                    $("#company_name").empty();
                    $("#company_name").append('<option selected value="">Required</option>');
                    for(var index in data['results'] ){
                        $("#company_name").append('<option value="' + data['results'][index]['value'] + '">' + data['results'][index]['text'] + '</option>')
                    }
                }else if($("#tab_name").text() == "income"){
                    $("#income_company_name").prop('disabled', false);
                    $("#income_company_name").empty();
                    $("#income_company_name").append('<option selected value="">Required</option>');
                    for(var index in data['results'] ){
                        $("#income_company_name").append('<option value="' + data['results'][index]['value'] + '">' + data['results'][index]['text'] + '</option>')
                    }
                }else if($("#tab_name").text() == "credit"){
                    console.log(selector)
                    if(selector == "account"){
                        $("#account_company_name").prop('disabled', false);
                        $("#account_company_name").empty();
                        $("#account_company_name").append('<option selected value="">Required</option>');
                        for(var index in data['results'] ){
                            $("#account_company_name").append('<option value="' + data['results'][index]['value'] + '">' + data['results'][index]['text'] + '</option>')
                        }
                    }else{
                        $("#credit_company_name").prop('disabled', false);
                        $("#credit_company_name").empty();
                        $("#credit_company_name").append('<option selected value="">Required</option>');
                        for(var index in data['results'] ){
                            $("#credit_company_name").append('<option value="' + data['results'][index]['value'] + '">' + data['results'][index]['text'] + '</option>')
                        }
                    }
                }else if($("#tab_name").text() == "savings"){
                    $("#savings_company_name").prop('disabled', false);
                    $("#savings_company_name").empty();
                    $("#savings_company_name").append('<option selected value="">Required</option>');
                    for(var index in data['results'] ){
                        $("#savings_company_name").append('<option value="' + data['results'][index]['value'] + '">' + $("#profile_name").text() + " - " + data['results'][index]['text'] + '</option>')
                    }
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("Error: ", textStatus);
            }
        }
    );
}

function on_select_of_company(){
    if($("#tab_name").text() == "credit" && $("#credit_type_of_account").val() == "credit"){
        $("#credit_name_of_recipient").val("Paid - " + $('#credit_company_name option:selected').text());
        $("#credit_name_of_recipient").prop("disabled", true);
    }else if($("#tab_name").text() == "savings" && $("#savings_type_of_account").val() == "savings"){
        $("#savings_name_of_recipient").val($('#savings_company_name option:selected').text());
        $("#savings_name_of_recipient").prop("disabled", true);
    }
}

function create_expense_transaction(){
    var json_data = {
        "transaction_info":
        {
            "account_id": $('#company_name').val().trim(),
            "amount": Number("-" + $('#transaction_amount').val().trim()),
            "date_occured": $('#date_occured').val().trim(),
            "name_of_recipient": $('#name_of_recipient').val().trim(),
        },
    }
    if($("#add_expense_form").valid()){
        $.ajax(
            {
                method: "POST",
                url: "/create_expense_transaction/",
                dataType: "json",
                data:{
                    "csrfmiddlewaretoken": csrftoken,
                    "data": JSON.stringify(json_data),
                },
                success: function (data, textStatus, jqXHR) {
                    if(data['response'] == "success"){
                        clear_expense_transaction_form(); 
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

function create_income_transaction(){
    var json_data = {
        "transaction_info":
        {
            "account_id": $('#income_company_name').val().trim(),
            "amount": Number($('#income_transaction_amount').val().trim()),
            "date_occured": $('#income_date_occured').val().trim(),
            "name_of_recipient": $('#income_name_of_recipient').val().trim(),
        },
    }
    if($("#add_income_form").valid()){
        $.ajax(
            {
                method: "POST",
                url: "/create_income_transaction/",
                dataType: "json",
                data:{
                    "csrfmiddlewaretoken": csrftoken,
                    "data": JSON.stringify(json_data),
                },
                success: function (data, textStatus, jqXHR) {
                    if(data['response'] == "success"){
                        clear_income_transaction_form(); 
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

function pay_credit_transaction(){
    var json_data = {
        "credit_info":
        {
            "credit_account_id": $("#credit_company_name").val(),
        },
        "account_info":
        {
            "account_id": $("#account_company_name").val(),
        },
        "transaction_info":
        {
            "amount": Number("-" + $('#credit_transaction_amount').val().trim()),
            "date_occured": $('#credit_date_occured').val().trim(),
            "name_of_recipient": $('#credit_name_of_recipient').val().trim(),
        },
    }
    if($("#pay_credit_form").valid()){
        $.ajax(
            {
                method: "POST",
                url: "/pay_credit_transaction/",
                dataType: "json",
                data:{
                    "csrfmiddlewaretoken": csrftoken,
                    "data": JSON.stringify(json_data),
                },
                success: function (data, textStatus, jqXHR) {
                    if(data['response'] == "success"){
                        clear_credit_transaction_form(); 
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

function clear_expense_transaction_form(){
    $("#type_of_account").val("");
    $("#company_name").empty();
    $("#company_name").append('<option selected value="">Required</option>')
    $("#company_name").prop("disabled", true);
    $("#name_of_recipient").val("");
    $("#date_occured").val("");
    $("#transaction_amount").val("");
}

function clear_income_transaction_form(){
    $("#income_type_of_account").val("");
    $("#income_company_name").empty();
    $("#income_company_name").append('<option selected value="">Required</option>')
    $("#income_company_name").prop("disabled", true);
    $("#income_name_of_recipient").val("");
    $("#income_date_occured").val("");
    $("#income_transaction_amount").val("");
}

function clear_credit_transaction_form(){
    $("#credit_type_of_account").val("");
    $("#credit_company_name").empty();
    $("#credit_company_name").append('<option selected value="">Required</option>')
    $("#credit_company_name").prop("disabled", true);
    $("#credit_name_of_recipient").val("");
    $("#credit_date_occured").val("");
    $("#credit_transaction_amount").val("");
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
                if(
                    element[0].id == "transaction_amount" ||
                    element[0].id == "income_transaction_amount" ||
                    element[0].id == "credit_transaction_amount"
                ){
                    error.appendTo(element.parent('.input-group'));
                }else{
                    error.insertAfter(element);
                }
            }
        });
        $("#add_expense_form").validate({
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
                name_of_recipient: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                date_occured: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                transaction_amount: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
            }
        });
        $("#add_income_form").validate({
            rules: {
                income_type_of_account: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                income_company_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                income_name_of_recipient: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                income_date_occured: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                income_transaction_amount: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
            }
        });
        $("#pay_credit_form").validate({
            rules: {
                credit_type_of_account: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                credit_company_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                account_type_of_account: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                account_company_name: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                credit_name_of_recipient: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                credit_date_occured: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
                credit_transaction_amount: {
                    required: true,
                    normalizer: function (value){
                        return $.trim(value);
                    },
                },
            }
        });
    });
});