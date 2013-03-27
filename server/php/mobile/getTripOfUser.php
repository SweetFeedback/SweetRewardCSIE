<?php
require_once("../db.php");
require_once("../onlineUser.php");


if(isset($_GET["token"])){
    $token = $_GET["token"];
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $user_id = $db->getUserIdByToken($token);
    echo json_encode($db->getTripsOfUser($user_id));
}
?>
