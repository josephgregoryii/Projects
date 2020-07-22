$(document).ready(function(){
    var child;
    var obj_data = {
                    "user_id" : $.cookie("user_id"),
                    "region"  : "us-west-2",
                    "Bucket"  : "rate-pics",
                    "version" : "latest",
                    };

    //Technically, this is a GET method, but we need
    //to send the user_id for now
    $.ajax({
        type: "POST",
        url: "../../proxy/account-details.php",
        data: {"user_id" : $.cookie("user_id")},
        datatype: JSON,
        success: function(data) {
            var child = `<span class="mr-2 d-none d-lg-inline text-gray-600 small">${data["account_details"]["full_name"]}</span>`; 
            $("#user_dropdown").append(child); 
            $.ajax({
                type: "POST",
                url: "../../proxy/cloud.php",
                data: obj_data,
                datatype: JSON,
                success: function(data) {
                    if (data['status'] == "error"){
                        //TODO: fix this
                    }
                    else{
                        child = `<img class="img-profile rounded-circle" src="${data["url"]}" </img>`;
                        $.cookie("img", data["url"]);
                    }
                },
                error: function(data){
                    console.log(data["responseText"]);

                },
                complete: function(){
                    $("#user_dropdown").append(child);
                },
            });
        }
});
    $("#user_dropdown")


});