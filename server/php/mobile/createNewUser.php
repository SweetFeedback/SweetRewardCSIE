<?php
require_once("../db.php");


if( isset($_GET["account"]) && isset($_GET["password"])){
    $username = $_GET["account"];
    $password = $_GET["password"];
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $db->insertNewUser($username, $password);
    echo json_encode($db->verifyUser($username, $password));
}

?>
