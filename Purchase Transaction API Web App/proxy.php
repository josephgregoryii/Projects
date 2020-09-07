<?php


if( isset($_POST['functionName'] ) ) {
    
    //statement to create an API access to callable functions 
    if      ($_POST['functionName'] == "authenticate")          { authenticate();       }
    else if ($_POST['functionName'] == 'loggedIn')              { loggedIn();           }
    else if ($_POST['functionName'] == 'createTransaction')     { createTransaction();  }
}

function createTransaction(){
/*********************************************************
    Creates a function using cookie authToken and the
    $_POST array to insert date, merchant, and amount
    into the Expensify API
    ARGS:
        None
    RETURNS:
        None
**********************************************************/
    if( isset($_COOKIE['authToken'])    &&
        isset($_POST['date'])           &&
        isset($_POST['merchant'])        &&
        isset($_POST['amount'])) {

        //reads .JSON file to get api URLS
        $str = file_get_contents('./api.json',true);
        $API = json_decode($str,true);

        $create_data= array(
            'authToken'         => $_COOKIE['authToken'],
            'created'           => $_POST['date'],
            'amount'            => $_POST['amount'],
            'merchant'          => $_POST['merchant']
            );
        $curl = curl_init();

        curl_setopt($curl, CURLOPT_URL, $API['create_post']);
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $create_data);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

        $result = curl_exec($curl);
        print_r($result);

        }
    
}


function loggedIn() {
/*********************************************************
    Function runs at onload. Serves as a GET method to grab a JSON 
    request from Expensify API using cookies.
    JSON object will contain parameters for Javascript file to handle

    ARGS:
        None
    RETURNS:
        None
**********************************************************/
    if( isset($_COOKIE['authToken']) && 
        !empty($_COOKIE['authToken'])) {

        //reads .JSON file to get api URLS
        $str = file_get_contents('./api.json',true);
        $API = json_decode($str,true);

        $display_data = array(
            'authToken'         => $_COOKIE['authToken'],
            'returnValueList'   => 'transactionList'
            );
        $curl = curl_init();

        $url  = sprintf("%s&%s", $API['get'], http_build_query($display_data));
        curl_setopt($curl, CURLOPT_URL, $url);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        $result = curl_exec($curl);
        print_r($result);
    }
}

function authenticate(){
/*********************************************************
    If a user has not been logged in, this function handles
    authentication through the Expensify API.
    ARGS:
        None
    RETURNS:
        None
**********************************************************/

    //check to make sure posts are correct
    if( isset($_POST['partnerName'])        &&
        isset($_POST['partnerPassword'])    && 
        isset($_POST['partnerUserID'])      && 
        isset($_POST['partnerUserSecret'])) {

        $str = file_get_contents('./api.json',true);
        $API = json_decode($str,true);

        $data = array(
            'partnerName'         => $_POST['partnerName'],
            'partnerPassword'     => $_POST['partnerPassword'],
            'partnerUserID'       => $_POST['partnerUserID'],
            'partnerUserSecret'   => $_POST['partnerUserSecret']
            );

        $curl = curl_init();

        //cURL POST
        curl_setopt($curl, CURLOPT_URL, $API['auth_post']);
        curl_setopt($curl, CURLOPT_POST, 1);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

        $result = curl_exec($curl);
        $json = json_decode($result,true);

        //This checks to see if authentication is successfull.
        //This fetches the data for transaction table display.
        if ($json['jsonCode'] == 200){
            $display_data = array(
                'authToken'         => $json['authToken'],
                'returnValueList'   => 'transactionList'
                );

            //FORTEST: set cookie for 5 minutes
            //setcookie("authToken", $json['authToken'], time() + (60*5));
            
            setcookie("authToken", $json['authToken']);

            //store accoundID and email for create transaction
            $GLOBALS['accountID'] = $json['accountID'];
            $GLOBALS['email']     = $json['email'];

            $curl = curl_init();

            //
            $url  = sprintf("%s&%s", $API['get'], http_build_query($display_data));
            curl_setopt($curl, CURLOPT_URL, $url);
            curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
            $result = curl_exec($curl);
            print_r($result);

        //Otherwise, send the json object to script
        //for error handling
        } else {

            print_r($result);
            curl_close($curl);
        }
    }
}

?>
