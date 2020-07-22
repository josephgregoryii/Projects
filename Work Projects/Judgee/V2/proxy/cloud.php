<?php
require '../vendor/autoload.php';
use Aws\S3\S3Client;


if ( isset($_POST["user_id"]) ) {
    header('Content-type: application/json');
    $data = getPicture($_POST, $_POST["user_id"]); 
    echo $data;
}

function getPicture($data, $key){

    $json = file_get_contents("./bucket_info.JSON");
    $json_array = json_decode($json,true);

    $s3 = new S3Client([
        "region"  => $json_array["region"],
        "version" => $json_array["version"]
    ]);

    $cmd = $s3->getCommand("GetObject",[
        "Bucket"    => $json_array["Bucket"],
        "Key"       => (int)$key
    ]);

    $request = $s3->createPresignedRequest($cmd, "+10 minutes");
    $signedUrl = (string) $request->getUri();
    return json_encode(array("status" => "success", "url" => $signedUrl));
}
?>