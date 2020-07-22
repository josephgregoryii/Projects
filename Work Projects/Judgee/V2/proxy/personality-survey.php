<?php 
require "Functions.php";

try{
    if($_POST) {
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
        $traits = ["smart","creative","attractive", "dependable","social","insecure","cooperative"];

        for($j = 0; $j < 7; $j++){
            if (!isset($_POST[$traits[$j]]["ranking"])){
                throw new Exception("Please select each trait only once");
            }
        }
        
        $i = 0;
        while ($i < 7){
            if (!$db->savePersonalityInfo($_POST[$traits[$i++]])){
                throw new Exception("Could not save login info");
            }
        }
        echo json_encode(array("success" => array("message" => "Personality Info Saved")));
    }else{
        throw new Exception("No data sent to server");
    }

//Login Failed or no data was sent to server
}catch(Exception $exc) {
    echo json_encode(array("error" => array("message" => $exc->getMessage())));
}

?>