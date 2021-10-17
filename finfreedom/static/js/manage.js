
function update_campany_selector(type_of_acc){
    console.log("Type of Acc: ", type_of_acc);
    $.ajax(
        {
            method: "POST",
            url: "check_if_email_exists/",
            dataType: "json",
            data:{
                "csrfmiddlewaretoken": csrftoken,
                "type_of_acc": type_of_acc,
            },
            success: function (data, textStatus, jqXHR) {
                console.log("response: ", data);
                
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("Error: ", textStatus);
            }
        }
    );
}


$(document).ready(function(){

});