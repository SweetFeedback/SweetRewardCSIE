<?php 
require_once("../db.php");
if(isset($_GET["token"])){
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
	$token = $_GET["token"];
	$user_id = $db->getUserIdByToken($token);

	$result = $db->getTransportationStatus($user_id);
	echo json_encode($result);
}
?>

