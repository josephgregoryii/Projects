$(document).ready(function(e){
   
    $("#create-account-form").submit(function(e) {
        e.preventDefault();


        let acc_data = {};
        $.each($("#create-account-form").serializeArray(),function(){
            acc_data[this.name] = this.value;
        });

        const account_data = acc_data;
        //console.log(account_data);

        $.ajax({
            type: "POST",
            url: "../../proxy/sign-up.php",
            data: account_data,
            datatype: JSON,
            success: function(data) {
                //console.log(data);
                if (data.error){
                    alert(`${data.error.message}\n Please try again.`); 
                }
                else{
                    $.cookie("user_id",data["user_id"], {"expires" : 1}); 
                }
            },
            error: function(data){
                console.log("error");
                console.log(data["responseText"]);

            },
            complete: function(){
                $("#sign-up-content").slideUp(1000, function(){ 
                    $("#sign-up-content").load("personality-survey.html").slideDown(1000);
                });
            }
        });
    });
});
