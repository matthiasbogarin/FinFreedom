// function populate_edit_account(e){
//     var account_id = $(e).closest('tr').find('td:nth-child(2)').text();
//     var data = $(e).closest('tr')[0].cells;
//     header_list = ['type_of_account', 'company_name', 'account_name', 'expiration_date', 'amount_on_card', 'credit_on_card']
//     for(var i = 2; i < data.length; i++){

//         console.log(data[i].innerText);
//     }

// }

function delete_account(e){
    var account_id = $(e).closest('tr').find('td:nth-child(2)').text();
    console.log("Perform Delete")
    $("#confirm_delete_modal").modal('hide');
}