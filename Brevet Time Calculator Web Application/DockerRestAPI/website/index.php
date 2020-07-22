<html>
  <head> <title> Project 6 - Restful API </title> </head>
    <body>
      <h1>List of laptops</h1>
        <ul>
            <?php
            $json = file_get_contents('http://laptop-service/');
            $obj = json_decode($json);
	        $laptops = $obj->Laptops;
            foreach ($laptops as $l) {
                echo "<li>$l</li>";
            }

            $json = file_get_contents('http://laptop-service/listAll');
            $listAll = json_decode($json);
            foreach ($listAll as $l) {
                foreach ($l as $x){
                    echo "<li>$x</li>";
                    }
            }

            $json = file_get_contents("http://laptop-service/listOpenOnly");
            $listOpenOnly = json_decode($json);
            foreach ($listOpenOnly as $l) {
                foreach($l as $x) {
                    echo "<li>$x</li>";
                }
            }
            $json = file_get_contents('http://laptop-service/listCloseOnly');
            $listCloseOnly = json_decode($json);
            foreach ($listCloseOnly as $l) {
                foreach($l as $x) {
                    echo "<li>$x</li>";
                }
            }

            $listAllCSV = json_decode(file_get_contents('http://laptop-service/listAll/csv'));
            if (!empty($listAllCSV)){
                echo "<li>$listAllCSV</li>";
            }

            $listOpenCSV = json_decode(file_get_contents('http://laptop-service/listOpenOnly/csv'));
            if (!empty($listOpenCSV)){
                echo "<li>$listOpenCSV</li>";
            }

            $listCloseCSV = json_decode(file_get_contents('http://laptop-service/listCloseOnly/csv'));
            if (!empty($listCloseCSV)){
                echo "<li>$listCloseCSV</li>";
            }

            $json = file_get_contents('http://laptop-service/listAll/json');
            $listAllJSON = json_decode($json);
            foreach ($listAllJSON as $l) {
                foreach($l as $x) {
                    echo "<li>$x</li>";
                }
            }
            $json = file_get_contents('http://laptop-service/listOpenOnly/json');
            $listOpenJSON = json_decode($json);
            foreach ($listOpenJSON as $l) {
                foreach($l as $x) {
                    echo "<li>$x</li>";
                }
            }
            $json = file_get_contents('http://laptop-service/listCloseOnly/json');
            $listCloseJSON = json_decode($json);
            foreach ($listCloseJSON as $l) {
                foreach($l as $x) {
                    echo "<li>$x</li>";
                }
            }
            ?>
        </ul>
    </body>
</html>
