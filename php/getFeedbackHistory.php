<?php
require_once("db.php");

$amount = 10;
if(isset($_GET['amount'])){
    $amount = $_GET['amount'];
}

$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
if(isset($_GET['user_id'])){
    $user_id = $_GET['user_id'];
    $result = $db->getRecentFeedbackBy($user_id, $amount);
}
else{
    $result = $db->getRecentFeedback($amount);
}
if($result != null){
    echo json_encode($result);
}
else{
    echo null;
}
?>
