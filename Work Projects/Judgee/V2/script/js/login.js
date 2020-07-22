$(document).ready(function(){

    if($.cookie("logged-out") == "1"){
        $.each($.cookie(), function(key,value){
            $.removeCookie(key);
        });
    }

    $("#sign-up").click(function(){
        window.location.href = "../../pages/sign-up.html";
    });

    //check login
    $(".cookie-check").html("<span>Checking cookies...</span>");
    if($.cookie("user_id") == "undefined"){
        window.location.href="../../pages/base.html";
    } else{
        $(".cookie-check").html("");
        $("#email-text, #password-text, #login-submit").prop("disabled", false);
    }

    $("#login-form").on("submit", function (e) {
        e.preventDefault();
        $("#login-submit").prop("disabled",true);

        var obj_data = {}
        $.each($("#login-form").serializeArray(), function() { 
            obj_data[this.name] = this.value;
        });
        
        $.ajax({
            type: "POST",
            url: "../../proxy/login.php",
            data: obj_data,
            datatype: JSON,
            success: function(data) {
                if (data.error){
                    $(".error-group").css("display","inline");
                    $(".error-group").html("<span class='text-danger text-center'>"+data.error.message+"</span>"); 
                    
                }
                else{
                    if($("#remember-me").is(":checked")){
                        $.cookie("user_id",data["user_id"], {"expire" : 365}); 
                    }else{

                        $.cookie("user_id",data["user_id"], {"expire" : 1}); 
                    }
                    window.location.href = "../../pages/base.html";


                }
            },
            error: function(data){
                console.log("error");
                console.log(data["responseText"]);

            },
            complete: function(){
                $("#login-submit").prop("disabled",false);
            },
        });
    }); 
});