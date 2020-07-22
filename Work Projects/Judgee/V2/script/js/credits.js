$(document).ready(function(){

    $.ajax({
        type: "POST",
        url : "../../proxy/credits.php",
        data: {"user_id" : $.cookie("user_id")},
        success : function(data){

            //check if there are any errors with server
            if(data.error){
                console.log(data.error.message);

            }else{
                
                // variable holds credits for display
                const child =`Total Credits: ${data.credits}`

                //load the html contents
                $("#credit-tr").html(child);


                // this is sort of a hacky way to get the number of purchasable traits
                //its really just if (number is greater than 0), else no purchasable traits
                try{
                    var num_purchasable_traits = Object.keys(data.traits).length - Object.keys(data.feedback).length;
                } catch (TypeError){
                    var num_purchasable_traits = 0;
                }

                // this variable stores the buttons that we'll be adding to the front end
                var table_child;

                //make sure we are not working with empty objects
                if(num_purchasable_traits != 0){

                    $.each(data.feedback, function(index,key){
                        if (key){

                            // capitalize the first letter of the trait for display purposes
                            let trait_name = key.trait_name.substr(0,1).toUpperCase()+key.trait_name.substr(1);

                            //this will loop over itself and append each <tr> for every available trait
                            table_child += 
                            `<tr>
                                <td class="text-center" id="${key.trait_name}">${trait_name}</td>
                                <td class="text-center" id="${key.trait_name}-can-purchase">
                                    <div class="btn-group btn-group-toggle" data-toggle="buttons">
                                        <label class="btn btn-primary">
                                            <input type="radio" name="purchase" id="${key.trait_name}" value="1" autocomplete="off">Available (3 credits)
                                        </label 
                                    </div>
                                </td>
                            </tr>`;
                        }
                    });

                // there are no traits for purchase :(
                } else{
                    table_child =  
                    `<tr>
                        <td class="text-center" id="none">No Available Traits for Purchase</td>
                        <td class="text-center" id="none-can-purchase">Come Back Later for More Traits!
                        </td>
                    </tr>`; 
                }

                //insert <tr> tags with options for purchase
                $("#trait-purchased-table").html(table_child);

                // if the user does not have enough credits,
                // they cannot purchase anything
                if (data.credits < 3){

                    // disable button
                    $("input:radio[name='purchase']").attr("disabled","disabled");
                }else{

                    //reenable button
                    $("input:radio[name='purchase']").removeAttr("disabled");
                }

                // check to see user has clicked one of the purchase buttons for a trait feedback
                $("input:radio[name='purchase']").change(function(e){

                    // button is pressed
                    if($(this).val() == "1"){

                        // user has i <= n data.traits for available feedback purchase
                        for(let i in data.traits){

                            // since its an object with (int) index,
                            // we need to find the id associated with
                            // the trait name
                            if(data.traits[i].trait_name == this.id){

                                //user defined function call
                                purchaseFeedback(data.traits[i].trait_id);

                                //load feedback page after
                                $("#content-div").slideUp(1000, function(){
                                    $("#content-div").load("my-feedback.html").slideDown(1000);
                                });

                            }
                        }
                    }
                });
                
            }
        }

    });

    function purchaseFeedback(id){
        $.ajax({
            type: "POST",
            url : "../../proxy/purchase-feedback.php",
            data: {
                    "user_id" : $.cookie("user_id"), 
                    "trait_id" : id
                },
            success : function(data){
                if(data.error){
                    console.log(data.error.message);
                }else{
                    console.log(data.success.message);
                }
            }
        });
    }

});