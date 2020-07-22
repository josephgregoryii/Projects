$(document).ready(function(){
    var child = `<img src= ${$.cookie("img")} class="rounded mx-auto d-block"alt="letstakeaselfee" width="300">`;
    $("#account-details-img").append(child);
    var details = {};
    var user_email;


    //disable left click
    $("body").on("contextmenu",function(e){
        return false;
   });

   //disable dragging images away from website
    $("img").mousedown(function(e){
        e.preventDefault();
    });

    //onload
    $.ajax({
        type: "POST",
        url: "../../proxy/account-details.php",
        data: {"user_id" : $.cookie("user_id")},
        datatype: JSON,
        success: function(data) {
            if (data.error){
                //todo
            }
            else{
                details = data["account_details"];
                user_email  = data["email"];

            }
        },
        error: function(data){
            console.log(data["responseText"]);

        },
        complete: function(){
            $("#email-display").html(`${user_email}`);

            /*
             * this each function displays the
             * demographics on profile.
             * database demographic variable names are
             * the same as html side
             */
            $.each(details, function(key, value){
               $(`#${key}`).html(`${value}`); 
            });
        },
    });

    function createObj(obj_data, user_email, justemail, justpassword, emailandpass){
        
        if (justemail && !emailandpass){

            obj_data["user_id"]          = $.cookie("user_id");
            obj_data["cur_email"]        = user_email;
            obj_data["current_password"] = $.trim($("#cur-passwd").val()); 
            obj_data["new_email"]        = $.trim($("#new-email").val());
            obj_data["new_password"]     = "null"; 

            //tells server which operation to use
            obj_data["func"]             = 1; 
        }
        else if(justpassword && !emailandpass){

            if( $.trim($("#new-passwd").val()) == $.trim($("#new-reppasswd").val()) ){

                obj_data["user_id"]          = $.cookie("user_id");
                obj_data["cur_email"]        = user_email;
                obj_data["cur_password"]     = $("#cur-passwd").val(); 
                obj_data["new_email"]        = "null";
                obj_data["new_password"]     = $("#new-passwd").val(); 
                obj_data["func"]             = 2; 
            }
            //new password and repeated new password do not match
            else{
                $("#error-p").html("<strong>ERROR: </strong>passwords do not match")
                return null;
            } 
        }

        //change both
        else if(emailandpass){

            if( $.trim($("#new-passwd").val()) == $.trim($("#new-reppasswd").val()) ){
                obj_data["user_id"]          = $.cookie("user_id");
                obj_data["cur_email"]        = user_email;
                obj_data["cur_password"]     = $("#cur-passwd").val(); 
                obj_data["new_email"]        = $("#new_email").val();
                obj_data["new_password"]     = $("#new-passwd").val();
                obj_data["func"]             = 3; 
            }
            else{
                $("#error-p").html("<strong>ERROR: </strong>passwords do not match")
                return null;
            } 
        }
        return obj_data;
    }

    //new email or password
    $("#account-details-form").submit(function (e){
        e.preventDefault();

        //variable declaration to define what the user wants to change
        let justemail    = ( ($("#new-email").val() != "") && ($("#new-passwd").val() == "") ? 1 : 0 );
        let justpassword = ( ($("#new-email").val() == "") && ($("#new-passwd").val() != "") ? 1 : 0 );
        let emailandpass = ( ($("#new-email").val() != "") && ($("#new-passwd").val() != "") ? 1 : 0 );
        
        //call to helper function that gives correct obj_data values 
        var obj_data = createObj({}, user_email, justemail, justpassword, emailandpass); 

        if(obj_data){
            $.ajax({
                type: "POST",
                url: "../../proxy/change-account-details.php",
                data: obj_data,
                datatype: JSON,
                success : function(data){
                    if (data.error)
                        $("#error-p").html(`<strong>Error:</strong> ${data.error.message}`);
                    else{
                    console.log(data);
                    if (obj_data["func"] == 1 || obj_data["func"] == 3)
                        $("#email-display").html(`${obj_data["new_email"]}`);
                    }

                },
            });
        }



    });


});