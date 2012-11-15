<?php
require_once("db.php");

if(isset($_GET['device_id'])){
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $device_id = $_GET['device_id'];
    $result = $db->getFeedbackStatusBy($device_id);
    if($result != null){
        echo json_encode($result);
    }
    else{
        echo null;
    }
}
?>
