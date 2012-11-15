<?php 
require_once("../db.php");
if(isset($_GET["token"]) && isset($_GET["trip_id"])){
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $token = $_GET["token"];
    $trip_id = $_GET["trip_id"];
	$user_id = $db->getUserIdByToken($token);

	$result = $db->getTransportationStatusByTrip($user_id, $trip_id);
	echo json_encode($result);
}
?>
