<?php
require_once("db.php");

#$db = new DB();
$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
if(isset($_GET["room_id"])){
    $room_id = $_GET["room_id"];
    $reuslt = $db->getRoomExistReport($room_id);
}else{
    $result = $db->getExistReport();
}
if($result != null){
    echo json_encode($result);
}
else{
    echo null;
}
?>
