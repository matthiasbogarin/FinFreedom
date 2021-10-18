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
});