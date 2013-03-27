<?php 
require_once("../db.php");

if(isset($_GET["token"])){
    $token = $_GET["token"];
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $user_status = $db->getUserByToken($token);
    //echo 
    $user_id = $user_status[0]['user_id'];

    echo json_encode($db->getFeedbackStatusByUserId($user_id));
}

?>
