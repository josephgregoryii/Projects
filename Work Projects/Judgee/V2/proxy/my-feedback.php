<?php 
require "Functions.php";
try {
    if( isset( $_POST["user_id"] )) {
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
        $feedback     = $db->getFeedback($_POST["user_id"]); 
        $all_feedback = $db->getAllFeedback();
        echo json_encode(array("success" => array("message" => "Feedback Available"),
                               "feedback" => $feedback,
                               "all_feedback" => $all_feedback));
    }else {
        throw new Exception("No data sent to server");
    }
}catch (Exception $exc){
    echo json_encode(array("error" => array("message" => $exc->getMessage())));
}

?>