<?php 
require "Functions.php";

try{
    if( isset( $_POST["user_id"] )) {
        header('Content-type: application/json');
        $json = file_get_contents("./database_credentials.JSON");
        $json_array = json_decode($json,true);
       
        try{
            $db = new Functions(    $json_array["host"],
                                    $json_array["user"],
                                    $json_array["password"],
                                    $json_array["database"]);
            if($db->connect_errno){
                throw new Exception($db->error);
            }
        
        //catch database connection error
        }catch(Exception $exc){
            echo json_encode(array("error" => array("message" => $exc->getMessage())));
        }
        
        $credits  = $db->getCredit($_POST["user_id"]);
        $traits   = $db->getTraits();
        $feedback = $db->getFeedback($_POST["user_id"],TRUE);
        echo json_encode(array("credits" => $credits, "traits" => $traits, "feedback" => $feedback));

    
    } else{
        throw new Exception("No data sent to server");
    }

//Login Failed or no data was sent to server
}catch(Exception $exc) {
    echo json_encode(array("error" => array("message" => $exc->getMessage())));
}

?>