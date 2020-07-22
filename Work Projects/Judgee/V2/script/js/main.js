/* 
 * js file handles content loading throughout the webapp.
 * handles sidebar navigation.
 */

$(document).ready(function(){
    
if (!$.cookie("user_id")){
        window.location.href = "../index.html";
}

$("#confirm_logout").click(function(e){
    e.preventDefault();
    $.each($.cookie(), function(key,value){
        $.removeCookie(key);
    });
    $.cookie("logged-out","1", {"path" : "/"});

    window.location.href = "../index.html";
});

    //home page
    $("#nav-home").click(function(e){
        
        //prevent refresh
        e.preventDefault();
        $("#content-div").slideUp(1000, function(){
            $("#content-div").load("content.html").slideDown(1000);
        })
    });
       
    //rate page
    $("#nav-rate").click(function(e){
        
        //prevent refresh
        e.preventDefault();
        $("#content-div").slideUp(1000, function(){
            $("#content-div").load("rate-others.html").delay(1000).slideDown(1000);
        });
    });

    //credits page
    $("#nav-credits").click(function(e){
        
        //prevent refresh
        e.preventDefault();
        $("#content-div").slideUp(1000, function(){
            $("#content-div").load("credits.html").slideDown(1500);
        });
    });

    //feedback page
    $("#nav-feedback").click(function(e){
        
        //prevent refresh
        e.preventDefault();
        $("#content-div").slideUp(1000, function(){
            $("#content-div").load("my-feedback.html").slideDown(2000);
        });
    });

    //profile page
    $("#btn-profile").click(function(e){
        
        //prevent refresh
        e.preventDefault();
        $("#content-div").slideUp(1000, function(){
            $("#content-div").load("account-details.html").slideDown(1000);
        });
    });
});
