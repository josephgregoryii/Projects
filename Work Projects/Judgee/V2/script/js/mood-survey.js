$(document).ready(function(){
    if(!$.cookie("mood_rate") && $.cookie("user_id")){
        $("#btn-profile").prop("disabled",true);
        $("#btn-logout").prop("disabled",true);
        $("#dialog-form").slideDown(1000);
        $("#mood-survey").submit(function(e) {
            e.preventDefault();

            var obj_data = {};

            $("#mood-survey").prop("disabled",true);
            $.each($("#mood-survey").serializeArray(), function() { 
                obj_data[this.name] = this.value;
            });
            obj_data["user_id"] = $.cookie("user_id");
            $.ajax({
                type: "POST",
                url: "../../proxy/mood-survey.php",
                data: obj_data,
                datatype: JSON,
                success: function(data) {
                    if (data["status"] == "error"){
                        alert("Something went wrong, but its okay! Press 'OK' to continue to Judgee");
                    }
                },
                error: function(data){
                    console.log(data["responseText"]);
                },
                complete: function(){
                    $.cookie("mood_rate",true, {expires: 1});
                
                },
            });

            $("#btn-profile").prop("disabled",false);
            $("#btn-logout").prop("disabled",false);
            $("#dialog-form").slideUp(1000, function(){
                $("#content-div").load("content.html").slideDown(2000);
                $("#accordion-sidebar").fadeIn(2000)
            });

        });
    }else{
        $("#btn-profile").prop("disabled",false);
            $("#btn-logout").prop("disabled",false);
            $("#dialog-form").slideUp(1000, function(){
                $("#content-div").load("content.html").slideDown(2000);
                $("#accordion-sidebar").fadeIn(2000)
            });
    }
    
});