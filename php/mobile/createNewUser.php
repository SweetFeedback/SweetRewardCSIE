<?php
require_once("../db.php");


if( isset($_GET["account"]) && isset($_GET["password"])){
    $username = $_GET["account"];
    $password = $_GET["password"];
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $result = array();
    if($db->insertNewUser($username, $password)!=null){
        $result = json_encode($db->verifyUser($username, $password));
    }
    else{
        $result['existed'] = 1;
    }
    echo json_encode($result);
}

?>
