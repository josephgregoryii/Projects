<?php
require "Functions.php";
try {
    if( isset( $_POST["current_user_id"] )) {
        header('Content-type: application/json');
        $json = file_get_contents("./database_credentials.JSON");
        $json_array = json_decode($json,true);
       
        try {
            $db = new Functions(    $json_array["host"],
                                    $json_array["user"],
                                    $json_array["password"],
                                    $json_array["database"]);
            if($db->connect_errno){
                throw new Exception($db->error);
            }
        }catch(Exception $exc){
                echo json_encode(array("status" => "error","message" => $exc->getMessage())); 
        }

        if($db->traitFeedbackExists($_POST["user_id"], $_POST["trait_id"])){
            $ratings_from_db = $db->getRatings($_POST["user_id"], $_POST["trait_id"]);

            //get number of ratings and increment by 1
            $num_ratings = (int)$ratings_from_db["num_ratings"];
            $num_ratings++;

            //add new num_ratings to dictionary
            $ratings_from_db["num_ratings"] = $num_ratings;

            //get average rating score
            $avg_rating = (float)$ratings_from_db["avg_rating"];

            if ($num_ratings > 1){

                //Since we incremented the number of ratings for this
                //user and trait, we need to subtract 1 from it
                //and multiply it by the average rating in order to
                //get the total number of rates for this user&&trait
                $total_rating_score = $avg_rating * ($num_ratings - 1); 

                //add the current rate to the overall rating score
                $total_rating_score = $total_rating_score + $_POST["rating"];

                //simple math
                $new_avg_rating = $total_rating_score / $num_ratings;

                //insert new average rating
                $ratings_from_db["avg_rating"] = $new_avg_rating;

                $db->updateFeedback($ratings_from_db);
            
            }else{
                
                $new_avg_rating = $_POST["rating"] / $num_ratings;

                $ratings_from_db["avg_rating"] = (int)$new_avg_rating;

                $db->updateFeedback($ratings_from_db);
            }

        } else{
            $to_db = array(
                "user_id"     => $_POST["user_id"],
                "trait_id"    => $_POST["trait_id"],
                "num_ratings" => 1,
                "avg_rating"  => $_POST["rating"]
            );
            $db->insertFeedback($to_db);
        }

        //updating credits
        $current_rates = (int)$db->getUserRatings($_POST["current_user_id"]);
        $current_rates++;

        if($current_rates == 3){
            $current_rates = 0;
            $result = (int)$db->getCredit($_POST["current_user_id"]);
            $result++;
            $db->updateCredit($_POST["current_user_id"], $result);
        }

        $db->updateUserRates($_POST["current_user_id"], $current_rates);
        $credits = $db->getCredit($_POST["current_user_id"]);
        echo json_encode(array("status" => "success","credit"=> $credits));


    }else {
        throw new Exception("No data sent to server");
    }
}catch (Exception $exc){
    echo json_encode(array("status" => "error","message" => $exc->getMessage()));
}
?>