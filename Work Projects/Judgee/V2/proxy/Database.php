<?php

class Database{
    protected $host;
    protected $user;
    protected $password;
    protected $database;

    public function __construct($host, $user, $password, $database){
        $this->host     = $host;
        $this->user     = $user;
        $this->password = $password;
        $this->database = $database;
    }

    /* functions is only called by class functions */
    protected function connect(){
        $db = new mysqli(   $this->host,
                            $this->user,
                            $this->password,
                            $this->database);

        /* check connection */
        if($db->connect_errno){
//            $error = sprintf("Connect failed: %s\n", $mysqli->connect_error);
//            printf("%s\n",$error);
            exit(1);
        }
        else{
            return $db;
        }
    }


    /* if $return_id is set to true, it skips getting results *
     * since there are none to fetch                          */
    protected function query($query, $return_id = false){
        
        /* connect to database */
        $db = $this->connect();

        /* perform query */
        $result = $db->query($query, MYSQLI_USE_RESULT);

        if ( !$return_id ){

            /* fetch all results */
            while($row = $result->fetch_assoc() ) {
                $results[] = $row;
            }
            /* free result list */
            $result -> free_result();
        }
        else{
            $results[] = $db->insert_id; 
        }

        /* close connection */
        $db->close();

        return $results;
    }
    
    protected function update($query){
        /* function performs UPDATE or INSERT */

        /* connect to database */
        $db = $this->connect();

        /* If insert_id is greater than zero (0), query executed */
        return (($db->query($query) && $db->affected_rows) ? 1 : 0);

    } 
}

?>
