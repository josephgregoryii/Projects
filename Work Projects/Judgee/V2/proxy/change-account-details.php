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

        //echo json_encode(array("test" =>$db->loginSuccess($_POST["cur_email"], $_POST["cur_password"]) ));

        if($db->loginSuccess($_POST["cur_email"], $_POST["cur_password"])){
        
            if( $_POST["func"] == 1){
                $db->changeLoginInfo($_POST["user_id"], $email = $_POST["new_email"]);
                
                echo json_encode(array("status" => "success", "message" => "Email changed successfully", "email" => $_POST["new_email"]));
            }
            else if ($_POST["func"] == 2){
                $db->changeLoginInfo($_POST["user_id"], null, $password = $_POST["new_password"]);

                echo json_encode(array("status" => "success", "message" => "Password changed successfully"));
            }
            else if ($_POST["func"] == 3){
                $db->changeLoginInfo($_POST["user_id"], $email = $_POST["new_email"], $password = $_POST["new_password"]);

                echo json_encode(array("status" => "success", "message" => "Email and password changed successfully", "email" => $_POST["new_email"]));
            }
        } else{
            throw new Exception("Current password incorrect");
        }

    }else {
        throw new Exception("No data sent to server");
    }
}catch (Exception $exc){
    echo json_encode(array("error" => array("message" => $exc->getMessage())));
}

?>