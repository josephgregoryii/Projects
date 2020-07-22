<?php
require "Functions.php";

try{
    if (isset ($_POST["mood-rate"]) && isset ($_POST["user_id"])){
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
            echo json_encode(array("status" => "error","message" => $exc->getMessage())); 
        }
        if(!$db->insertPreMoodSurvey($_POST)){
            throw new Exception("Could not insert to database");
        }
        echo json_encode(array("status" => "success"));
    }
} catch(Exception $exc){
    echo json_encode(array("status" => "error","message" => $exc->getMessage()));
}

?>