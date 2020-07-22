<?php
require "Database.php";

class Functions extends Database{
    public function __construct($host, $user, $password, $database){
        Database::__construct($host, $user, $password, $database);
    }


/* ********************Account Details and Information******************** */

    /* string function */
    public function getEmail($user_id){
        $query  = sprintf(  "SELECT email FROM Users WHERE user_id = %d",
                            $user_id
                        );
        $result = $this->query($query);

        if (sizeof($result) == 0)   { return "Does not exist"; }
        else                        { return $result[0]["email"]; }
    }

    /* boolean function */
    public function userExists($table, $user_id){
        $query  = sprintf(  "SELECT user_id FROM %s WHERE user_id = %d",
                            $table,
                            $user_id
                        );
        $result = $this->query($query);

        return (sizeof($result[0]) > 0 ? TRUE : FALSE );
    }

    /* boolean function */
    public function loginSuccess($email, $password){
        $query = sprintf(   "SELECT email, passwd FROM Users WHERE email = '%s'",
                            $email
                        );
        $result = $this->query($query);

        if (password_verify($password, $result[0]["passwd"])){
            return TRUE;
        }else{
            return FALSE;
        }
    }
    
    /* int function */
    public function saveLoginInfo($info){
        $query = sprintf(   "INSERT INTO Users (email, passwd, traits) VALUES ('%s', '%s', '%s')", 
                            $info['email'],
                            password_hash($info['passwd'], PASSWORD_DEFAULT),
                            "1,2,3,4,5,6,7"
                        );
        $result = $this->query($query, true);
        return (int)$result[0];
    }

    /* int function */
    public function returnUserId($email){
        $query = sprintf(   "SELECT user_id FROM Users WHERE email = '%s'",
                            $email
                        );

        $result = $this->query($query);
        if (sizeof($result) > 0)    { return (int)$result[0]["user_id"]; }
        else                        { return 0; }
    
    }

    /* boolean function */
    public function saveAccountInfo($info){
        $query = sprintf(
                "INSERT INTO Demographics 
                (user_id, full_name, birthdate, race, ethnicity, sex, gender, height, weight, orientation, " .
                "marital_status, num_children, education_level, employment_status, employment_field, " .
                "annual_income, parental_income, ideology, smoking_status, drinks_per_week, " .
                "weed_per_week, substance_use, dieting_status, num_partners, safe_sex, credit) " .
                "VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', %d, %d, '%s', '%s', %d, '%s', '%s', " .
                    "'%s', %d, %d, '%s', %d, %d, %d, %d, %d, %d, %d, %d)",
                $info['user_id'],$info['full_name'], $info['birthdate'], $info['race'], $info['ethnicity'],
                $info['sex'], $info['gender'], $info['height'], $info['weight'], $info['orientation'],
                $info['marital_status'], $info['num_children'], $info['education_level'],
                $info['employment_status'], $info['employment_field'], $info['annual_income'], $info['parental_income'],
                $info['ideology'], $info['smoking_status'], $info['drinks_per_week'], $info['weed_per_week'],
                $info['substance_use'], $info['dieting_status'], $info['num_partners'], $info['safe_sex'], $info['credit']
                );
        return ($this->query($query,true) ? TRUE : FALSE );
    }

    /* boolean function */
    public function savePersonalityInfo($info){
        $query = sprintf(   "INSERT INTO Personality_survey (user_id, trait_id, trait_affinity, certainty, importance, ranking) " . 
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            $info["user_id"], $info["trait_id"], $info["trait_affinity"],
                            $info["certainty"], $info["importance"], $info["ranking"]
                        );
        return ($this->query($query, true) ? TRUE : FALSE );
    }

    /* boolean function */
    public function changeLoginInfo($user_id, $email = null, $password = null){
        
        /* calls to class function to save execution time */
        if ( !$this->userExists("Users", $user_id) ) { 
            return FALSE; 
        }


        /* change email and password */
        if ($email && $password){
            $query = sprintf(   "UPDATE Users SET email = '%s', passwd = '%s' WHERE user_id = %d",
                                $email,
                                password_hash($password, PASSWORD_DEFAULT),
                                $user_id
                            );
        }

        /* change email */
        if ($email && is_null($password)){
            $query = sprintf(   "UPDATE Users SET email = '%s' WHERE user_id = %d",
                                $email,
                                $user_id
                            );
        }
        
        /* change password */
        if(is_null($email) && $password){
            $query = sprintf(   "UPDATE Users SET passwd = '%s' WHERE user_id = %d",
                                password_hash($password, PASSWORD_DEFAULT),
                                $user_id
                            );
        }
        return ($this->update($query) ? TRUE : FALSE );
    }
   
    public function getAccountDetails($user_id){
        $query = sprintf(   "SELECT * FROM Demographics WHERE user_id = %d",
                            $user_id
                        );
        $result = $this->query($query);
        return $result[0];
    }

/* ************************Ratings and Credits**************************** */

    /* array function */
    public function getRatings($user_id, $trait_id){
        $query = sprintf(   "SELECT user_id, trait_id, num_ratings, avg_rating FROM Feedback WHERE user_id = %d AND trait_id = %d",
                            $user_id,
                            $trait_id
                        );
        $result = $this->query($query);
        return $result[0];
    }

    /* int function */
    public function getUserRatings($user_id){
        $query = sprintf(   "SELECT ratings FROM Users WHERE user_id = %d",
                            $user_id
                        );
        $result = $this->query($query);
        $ratings = $result[0]["ratings"];
        return $ratings;
    }

    /* boolean function */
    public function updateUserRates($user_id, $rates){
        $query = sprintf(   "UPDATE Users SET ratings = %d WHERE user_id = %d",
                            $rates,
                            $user_id
                        );
        return ($this->update($query) ? TRUE : FALSE );
    }

    /* int function */
    public function getCredit($user_id){
        $query = sprintf(   "SELECT credit FROM Demographics WHERE user_id = %d",
                            $user_id  
                        );
        $result = $this->query($query);
        $credit = $result[0]["credit"];
        return (int)$credit;
        
    }

    /* boolean function */
    public function updateCredit($user_id, $reset = null){
        //TODO:
        //implement reset option to reset credits
        /*if ($reset) { } */
        $credit = $this->getCredit($user_id);

        if($credit > 3){
            $credit = $credit - 3;
        }else {
            $credit = 0;
        }
        $query = sprintf(   "UPDATE Demographics SET credit = %d WHERE user_id = %d",
                            $credit,
                            $user_id
                        );
        $result = $this->update($query);
        return $result;
    }

/* ************************Feedback and Traits**************************** */

    /* boolean function */
    public function traitFeedbackExists($user_id, $trait_id){
        $query = sprintf(   "SELECT user_id, trait_id FROM Feedback WHERE user_id = %d AND trait_id = %d",
                            $user_id,
                            $trait_id
                        );
        $result = $this->query($query);
        return ( sizeof($result) > 0 ? 1 : 0 );
    } 

    /* boolean function */
    public function insertFeedback($info, $purchased = 0){
        $query = sprintf(   "INSERT INTO Feedback (user_id, trait_id, num_ratings, avg_rating, purchased)" .
                            "VALUES (%d, %d, %d, %d, %d)",
                            $info["user_id"], $info["trait_id"],
                            $info["num_ratings"], $info["avg_rating"],
                            $purchased
                        );
        $result = $this->query($query, true);
        return $result;
    }

    /* boolean function */
    public function purchaseFeedback($info, $purchased = 1){
        $query = sprintf(   "UPDATE Feedback SET purchased = %d WHERE user_id = %d AND trait_id = %d",
                            $purchased,
                            $info["user_id"],
                            $info["trait_id"]
                        );
        $result = $this->update($query);
        return $result;
    }

    /* int function */
    public function countFeedback($user_id, $purchased = 1){
        $query = sprintf(   "SELECT COUNT(*) FROM Feedback WHERE user_id = %d AND purchased = %d",
                            $user_id,
                            $purchased
                        );
        $result = $this->query($query);

        return (int)$result[0]["COUNT(*)"];
    }

    /* boolean function */
    public function updateFeedback($info, $purchased = False){
        if (!$purchased){
            $query = sprintf(   "UPDATE Feedback SET num_ratings = %d, avg_rating = %d " . 
                                "WHERE user_id = %d AND trait_id = %d",
                                $info["num_ratings"], $info["avg_rating"], 
                                $info["user_id"], $info["trait_id"]
                            );
        }else {
            $query = sprintf(   "UPDATE Feedback SET purchased = %d WHERE " . 
                                "user_id = %d AND trait_id = %d",
                                $info["purchased"], $info["user_id"],
                                $info["trait_id"]
                            );
        }
        $result = $this->query($query,true);
        return $result;
        
    } 

    /* array function */
    public function getFeedback($user_id, $for_credit = False){
        if (!$for_credit) {
            $query = sprintf(   "SELECT t.trait_name, f.num_ratings, f.avg_rating " . 
                                "FROM Feedback f JOIN Traits t USING (trait_id) " . 
                                "WHERE f.user_id = %d AND f.purchased = 1",
                                $user_id
                            );
        }else {
            $query = sprintf(   "SELECT t.trait_name, f.num_ratings, f.avg_rating " . 
                                "FROM Feedback f JOIN Traits t USING (trait_id) " . 
                                "WHERE f.user_id = %d AND f.purchased = 0",
                                $user_id
                            );
        }
        $result = $this->query($query);
        return $result;
    }

/* *********************Helper/Misc. Functions**************************** */

    public function numberOfUsers(){
        $query = "SELECT COUNT(*) FROM Users";
        $result = $this->query($query);

        return(int)$result[0]["COUNT(*)"];
    }

    public function chooseRandomUserAndTrait($current_user, $trait=True){
        $num_users = $this->numberOfUsers();
        $random_id = $current_user;

        if ($trait){
            while ($random_id == $current_user) {
                //$random_id = rand(1,$num_users);
                
                //for testing purposes
                $random_id = rand(1,10);
            }
        }
        
        $query = sprintf(   "SELECT traits FROM Users WHERE user_id = %d",
                            $random_id
                        );
        $result = $this->query($query);
        $result = $result[0]["traits"];

        $traits   = explode (",", $result);
        $size     = sizeof($traits) - 1;

        $index    = rand(0, $size);
        
        $trait_id = (int)$traits[$index];

        $query = sprintf(   "SELECT trait_name FROM Traits WHERE trait_id = %d",
                            $trait_id
                        );
        $result     = $this->query($query);
        $trait_name = $result[0]["trait_name"];

        $info = array(
            "user_id"       => $random_id,
            "trait_id"      => $trait_id,
            "trait_name"    => $trait_name
        );
        return $info;
    }

    public function deleteUser($user_id){
        $query = sprintf(   "DELETE FROM Users WHER user_id = %d",
                            $user_id
                        );
        $result = $this->query($query);
        return $result;
    }

    public function insertPreMoodSurvey($info){
        $query = sprintf(   "INSERT INTO Pre_mood_survey (user_id, mood_rate) VALUES (%d, %d)", 
                            $info["user_id"], $info["mood-rate"] );
        $result = $this->query($query,true);
        return $result;
    }

    public function getTraits(){
        $query = "SELECT * FROM Traits";
        $result = $this->query($query);
        return $result;
    }

    public function getAllFeedback(){
        $query = "SELECT * FROM Feedback";
        $result = $this->query($query);
        return $result;
    }

}
?>