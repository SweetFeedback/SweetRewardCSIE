<?php 
require_once("db.php");
#if(isset($_GET["token"])){
#    $token = $_GET["token"];
$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
$db->getFeedbackRanking();
#}
?>
