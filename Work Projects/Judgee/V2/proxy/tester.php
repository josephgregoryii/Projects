<?php header('Content-type: text/html; charset=utf-8');

require "Functions.php";


echo round(memory_get_usage()/1048576,2).''.' MB' . '<br>';

$json = file_get_contents("./database_credentials.JSON");
$data = json_decode($json,true);


/* new database object*/
$db = new Functions($data["host"],
                    $data["user"],
                    $data["password"],
                    $data["database"]);

/* test functions */
$result1 = $db->getEmail(5);
$result2 = $db->getEmail(10000);
echo "Email 1: " . $result1 . "<br>";
echo "Email 2: " . $result2 . "<br>";

$result3 = $db->userExists("Users",5);
$result4 = $db->userExists("Users",10000);
echo "User Exists: " . $result3 . "<br>";
echo "User Exists: " . (boolval($result4) ? 1 : 0 ) . "<br>";

$email1 = "4@fakemail.com";
$pass1 = "0cc175b9c0f1b6a831c399e269772661";
$result5 = $db->loginSuccess($email1, $pass1);
echo "Login Success: " . (boolval($result5) ? "true":"false") . "<br>";

$email2 = "notanemail@fakemail.com";
$pass2  = "notapassword";
$result6 = $db->loginSuccess($email2, $pass2);
echo "Login Success: " . (boolval($result6) ? "true":"false") . "<br>";

$info1 = array(
    "email" => "0@fakemail.com",
    "passwd" => "0cc175b9c0f1b6a831c399e269772661"
);
//$result7 = $db->save_login_info($info1);
//echo "Saved Login Info (user_id): " . $result7 . "<br>";

//returns 1
$result8 = $db->returnUserId($info1["email"], $info1["passwd"]);

//returns 0 (not a valid email and user)
$result9 = $db->returnUserId("emaildoesnotexist@fakemail.com", $info1["passwd"]);

//display results
echo "returned user_id: " . $result8 . "<br>";
echo "returned user_id: " . $result9 . "<br>";

//true
$result10 = $db->changeLoginInfo(20, "newnotanemail3@fakemail.com", null);

//true
$result11 = $db->changeLoginInfo(20, "newnewnotanemail3@fakemail.com","newtestpassword3");

//true
$result12 = $db->changeLoginInfo(20, null,"newnewtestpassword3");

//false
$result13 = $db->changeLoginInfo(200000, "thisshouldnotwork3","shouldnotwork3");

echo "changed login email: " . (boolval($result10) > 0 ? "true" : "false") . "<br>";
echo "changed login email and password: " . (boolval($result11) > 0 ? "true" : "false") . "<br>";
echo "changed login password: " . (boolval($result12) > 0 ? "true" : "false") . "<br>";
echo "changed login invalid email and password: " . (boolval($result13) > 0 ? "true" : "false") . "<br>";

//returns 20
$result14 = $db->returnUserId("newnewnotanemail3@fakemail.com","newnewtestpassword3");
echo "returned user_id: " . $result14 . "<br>";

$result15 = $db->getUserRatings(5);
echo sprintf("number of ratings from user 5: %u rating(s) <br>" , $result15);

$result16 = $db->getRatings(4, 3);
echo var_dump($result16);
echo "<br>";

$result17 = $db->getCredit(1);
echo "credits: " . $result17 . "<br>";

$result18 = $db->updateCredit(1,10);
echo "updated credit: " . (boolval($result18) ? "true":"false") . "<br>";

$result10000 = $db->updateCredit(0,10);
echo "updated credit: " . (boolval($result10000) ? "true":"false") . "<br>";

$result19 = $db->getCredit(1);
echo "credits: " . $result19 . "<br>";

$result20 = $db->getAccountDetails(1);
echo var_dump($result20) . "<br>";

$info = array(
    'user_id' => 19,
        'full_name' => "Test Person " . "14",
        'birthdate'=> "1989-01-01",
        'race' => "White",
        'ethnicity' => "White",
        'sex' => "Male",
        'gender' => "Male",
        'orientation' => "Heterosexual",
        'height' => 72,
        'weight' => 180,
        'marital_status' => "Single",
        'num_children' => 0,
        'education_level' => "High School",
        'employment_status' => "Unemployed",
        'employment_field' => "Technology",
        'annual_income' => 100000,
        'parental_income' => 100000,
        'ideology' => "Anarchist",
        'smoking_status' => 0,
        'drinks_per_week'=> 0,
        'weed_per_week' => 0,
        'substance_use' => 0,
        'dieting_status' => 0,
        'num_partners' => 69,
        'safe_sex' => 0,
        'credit' => 0
);

$result21 = $db->saveAccountInfo($info);
echo "saved account info: " . (boolval($result21) ? "true" : "false") . "<br>";

$info2 = array(
    "user_id" => 19,
    "trait_id" => 1,
    "trait_affinity" => 1,
    "certainty" => 1,
    "importance" => 1,
    "ranking" => 1
);

$result22 = $db->savePersonalityInfo($info2);
echo "saved personality info: " . (boolval($result22) ? "true" : "false");
echo "<br>";

$result23 = $db->traitFeedbackExists(1,5);
echo "trait feedback exists: " . (boolval($result23) ? "true" : "false") . "<br>";

$result24 = $db->traitFeedbackExists(1,4);
echo "trait feedback exists: " . (boolval($result24) ? "true" : "false") . "<br>";

$result25 = $db->countFeedback(5);
echo $result25 . "<br";





$vars = array_keys(get_defined_vars());
for ($i = 0; $i < sizeOf($vars); $i++) {
    print($vars[i]);
    unset($$vars[$i]);
}
unset($vars,$i);

echo round(memory_get_usage()/1048576,2).''.' MB' .'<br>';
echo round(memory_get_peak_usage()/1048576,2).''.' MB' .'<br>';

?>
