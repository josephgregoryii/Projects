<?php 
require "Functions.php";

try{
    if( isset( $_POST["email"] ) && isset( $_POST["passwd"] ) ) {
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

        $login_info = array(
            "email" => $_POST["email"],
            "passwd" => $_POST["passwd"]
        );

        if ($db->saveLoginInfo($login_info)){
            if (!$db->loginSuccess($login_info["email"], $login_info["passwd"]) ){
                throw new Exception("Login failed. Please try again.");
            }
            unset($login_info["passwd"]);
            unset($_POST["passwd"]);
        }
        else{
            throw new Exception("Could not save login info");
        }

        if ($db->saveAccountInfo($_POST)){
            $user_id = $db->returnUserId($_POST["email"]);
            echo json_encode(array("status" => "success", "user_id" => $user_id));
        }else{
            throw new Exception("Could not save account info");
        }
    
    } else{
        throw new Exception("No data sent to server");
    }

//Login Failed or no data was sent to server
}catch(Exception $exc) {
    echo json_encode(array("error" => array("message" => $exc->getMessage())));}

?>