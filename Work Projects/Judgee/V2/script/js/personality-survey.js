$(document).ready(function(e){
   
    $("#personality-form").submit(function(e) {
        e.preventDefault();

        let user_id = $.cookie("user_id");


        // we will bind this to a const later
        let pers_data = {
            "smart"      : {},
            "creative"   : {},
            "attractive" : {},
            "dependable" : {},
            "social"     : {},
            "insecure"   : {},
            "cooperative": {},
        };

        
        let check_rankings = new Array();

        let rankings_checked = true;

        // i is for storing the ranking importance
        // i.e., the firs tranking that is found, will be
        // set to the correct trait at the i'th spot
        let i = 1;
        $.each($("#personality-form").serializeArray(),function(){
            if(this.name.includes("smart")){

                // first question related to smart
                // is the trait affinity
                if(this.name.includes("1")){
                    pers_data["smart"]["trait_affinity"] = this.value; 

                // second question related to smart
                // is the certainty of response
                } else if(this.name.includes("2")){
                    pers_data["smart"]["certainty"] = this.value; 
                
                // third question related to smart
                // is importance of trait
                } else if(this.name.includes("3")){
                    pers_data["smart"]["importance"] = this.value; 
                }

                // add trait_id if not in dictionary
                if(!("trait_id" in pers_data["smart"]))
                    pers_data["smart"]["trait_id"] = 1;

                // add user_id to each object if it is
                // not in it 
                // -----------------------------------
                // database accepts only 
                // one dictionary at a time
                if (!("user_id" in pers_data["smart"]))
                    pers_data["smart"]["user_id"] = user_id; 

            } else if(this.name.includes("creative")){
                
                // first question related to creative 
                // is the trait affinity
                if(this.name.includes("1")){
                    pers_data["creative"]["trait_affinity"] = this.value; 

                // second question related to creative 
                // is the certainty of response
                } else if(this.name.includes("2")){
                    pers_data["creative"]["certainty"] = this.value; 
                
                // third question related to creative 
                // is importance of trait
                } else if(this.name.includes("3")){
                    pers_data["creative"]["importance"] = this.value; 
                }

                // add trait_id if not in dictionary
                if(!("trait_id" in pers_data["creative"]))
                    pers_data["creative"]["trait_id"] = 2;
                    
                // add user_id to each object if it is
                // not in it 
                // -----------------------------------
                // database accepts only 
                // one dictionary at a time
                if (!("user_id" in pers_data["creative"]))
                    pers_data["creative"]["user_id"] = user_id; 

            
            } else if(this.name.includes("attractive")){

                // first question related to attractive 
                // is the trait affinity
                if(this.name.includes("1")){
                    pers_data["attractive"]["trait_affinity"] = this.value; 

                // second question related to attractive 
                // is the certainty of response
                } else if(this.name.includes("2")){
                    pers_data["attractive"]["certainty"] = this.value; 
                
                // third question related to attractive 
                // is importance of trait
                } else if(this.name.includes("3")){
                    pers_data["attractive"]["importance"] = this.value; 
                }

                // add trait_id if not in dictionary
                if(!("trait_id" in pers_data["attractive"]))
                    pers_data["attractive"]["trait_id"] = 3;

                // add user_id to each object if it is
                // not in it 
                // -----------------------------------
                // database accepts only 
                // one dictionary at a time
                if (!("user_id" in pers_data["attractive"]))
                    pers_data["attractive"]["user_id"] = user_id; 
        
            } else if(this.name.includes("dependable")){

                // first question related to dependable 
                // is the trait affinity
                if(this.name.includes("1")){
                    pers_data["dependable"]["trait_affinity"] = this.value; 

                // second question related to dependable 
                // is the certainty of response
                } else if(this.name.includes("2")){
                    pers_data["dependable"]["certainty"] = this.value; 
                
                // third question related to dependable 
                // is importance of trait
                } else if(this.name.includes("3")){
                    pers_data["dependable"]["importance"] = this.value; 
                }

                // add trait_id if not in dictionary
                if(!("trait_id" in pers_data["dependable"]))
                    pers_data["dependable"]["trait_id"] = 4;


                // add user_id to each object if it is
                // not in it 
                // -----------------------------------
                // database accepts only 
                // one dictionary at a time
                if (!("user_id" in pers_data["dependable"]))
                    pers_data["dependable"]["user_id"] = user_id;

            } else if(this.name.includes("social")){

                // first question related to social 
                // is the trait affinity
                if(this.name.includes("1")){
                    pers_data["social"]["trait_affinity"] = this.value; 

                // second question related to social 
                // is the certainty of response
                } else if(this.name.includes("2")){
                    pers_data["social"]["certainty"] = this.value; 
                
                // third question related to social 
                // is importance of trait
                } else if(this.name.includes("3")){
                    pers_data["social"]["importance"] = this.value; 
                }

                // add trait_id if not in dictionary
                if(!("trait_id" in pers_data["social"]))
                    pers_data["social"]["trait_id"] = 5;


                // add user_id to each object if it is
                // not in it 
                // -----------------------------------
                // database accepts only 
                // one dictionary at a time
                if (!("user_id" in pers_data["social"]))
                    pers_data["social"]["user_id"] = user_id;

            } else if(this.name.includes("insecure")){

                // first question related to insecure 
                // is the trait affinity
                if(this.name.includes("1")){
                    pers_data["insecure"]["trait_affinity"] = this.value; 

                // second question related to insecure 
                // is the certainty of response
                } else if(this.name.includes("2")){
                    pers_data["insecure"]["certainty"] = this.value; 
                
                // third question related to insecure
                // is importance of trait
                } else if(this.name.includes("3")){
                    pers_data["insecure"]["importance"] = this.value; 
                }

                // add trait_id if not in dictionary
                if(!("trait_id" in pers_data["insecure"]))
                    pers_data["insecure"]["trait_id"] = 6;


                // add user_id to each object if it is
                // not in it 
                // -----------------------------------
                // database accepts only 
                // one dictionary at a time
                if (!("user_id" in pers_data["insecure"]))
                    pers_data["insecure"]["user_id"] = user_id;

            } else if(this.name.includes("cooperative")){

                // first question related to cooperative 
                // is the trait affinity
                if(this.name.includes("1")){
                    pers_data["cooperative"]["trait_affinity"] = this.value; 

                // second question related to cooperative
                // is the certainty of response
                } else if(this.name.includes("2")){
                    pers_data["cooperative"]["certainty"] = this.value; 
                
                // third question related to cooperative
                // is importance of trait
                } else if(this.name.includes("3")){
                    pers_data["cooperative"]["importance"] = this.value; 
                }

                // add trait_id if not in dictionary
                if(!("trait_id" in pers_data["cooperative"]))
                    pers_data["cooperative"]["trait_id"] = 7;


                // add user_id to each object if it is
                // not in it 
                // -----------------------------------
                // database accepts only 
                // one dictionary at a time
                if (!("user_id" in pers_data["cooperative"]))
                    pers_data["cooperative"]["user_id"] = user_id;

            // add each ranking to correct trait object
            } else if (this.name.includes("rank")){
            
                // trait will be key to add to trait object
                let trait = this.value;

                // ERROR CHECK //
                // check if a ranking is already used
                if(trait.toLowerCase() in check_rankings){
                }else{
                    check_rankings.push(trait.toLowerCase());
                }

                // e.g., pers_data["smart"]["ranking"] = 4;
                pers_data[trait.toLowerCase()]["ranking"] = i++;
            }
                
        });
        const personality_data = pers_data;
        //console.log(personality_data);

        if(rankings_checked){
            $.ajax({
                type: "POST",
                url: "../../proxy/personality-survey.php",
                data: personality_data,
                datatype: JSON,
                success: function(data) {
                    //console.log(data);
                    if (data.error){
                        $("#error-p").html("<span class='text-danger text-center'>"+data.error.message+"</span>"); 
                        alert(data.error.message);
                    }
                    else{
                        $.cookie("user_id",data["user_id"], {"expire" : 1}); 
                        //window.location.href="../../pages/base.html";
                    }
                },
                error: function(data){
                    console.log("error");
                    //console.log(data);

                }
            });
        }

    });
});

