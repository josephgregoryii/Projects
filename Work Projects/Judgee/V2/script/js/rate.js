$(document).ready(function(){
   
    //disable "right-click" on page
    $("body").on("contextmenu",function(e){
        return false;
   });
   
   //immediate call to get user rate image
    getRatePicture();
    
    $("#rate-others-form").on("submit", function (e) {
        e.preventDefault();
        var info = {
            "current_user_id" : Number($.cookie("user_id")),
            "user_id"         : Number(obj_data["user_id"]),
            "trait_id"        : Number(obj_data["trait_id"]),
            "rating"          : Number($("input[name='rate']:checked").val())
        };
        rateOthers(info);
        getRatePicture();
    });

    var child;
    var trait_child;
    var obj_data = {};

    function getRatePicture(){
        $.ajax({
            type: "POST",
            url: "../../proxy/choose-rate-others.php",
            data: {"user_id" : $.cookie("user_id")},
            datatype: JSON,
            success: function(data) {
                if (data['status'] == "error"){
                    //todo
                }
                else{
                    obj_data["user_id"]    = data["info"]["user_id"];
                    obj_data["trait_name"] = data["info"]["trait_name"];
                    obj_data["trait_id"] = data["info"]["trait_id"];

                }
            },
            error: function(data){
                console.log("e",data["responseText"]);

            },
            complete: function(){
                $.ajax({
                    type: "POST",
                    url: "../../proxy/cloud.php",
                    data: obj_data,
                    datatype: JSON,
                    success: function(data){
                        if (data["status"] == "success"){
                            child       = `<img src=${data["url"]} class="rounded mx-auto d-block" alt="chosen_user" width="300"></img>`
                            trait_child = `<h3 class="font-weight-bold text-primary text-uppercase mb-1 text-center" id="trait-name">${obj_data["trait_name"]}</h3>`
                        }
                    },
                    error: function(data){
                        console.log(data["responseText"]);
                    },
                    complete: function(){
                        $("#rate-pic").slideUp(1000, function(){
                            $("#rate-pic").html(child);
                        });
                        $("#rate-pic").delay(100).slideDown(1000);
                        $("#trait-name-div").html(trait_child);

                        //disable dragging images away from website
                        $("img").mousedown(function(e){
                            e.preventDefault();
                    })
                    }

                });
            }
        });
    }

    function rateOthers(info){
    /*
    The functioanlity of the rating system relys heavily on the
    database. Therefore, the server will provide the "heavy lifting"
    and logic of the system.
    */
        $.ajax({
            type: "POST",
            url: "../../proxy/rate-others.php",
            data: info,
            datatype: JSON,
            success: function(data) {
                if (data['status'] == "success"){
                    console.log(data["credit"]);
                }
            },
            error: function(data){
                console.log("ERROR",data["responseText"]);

            },
            complete: function(){
                
            }
        });
    }
});