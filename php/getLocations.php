<?php 
require_once("db.php");

$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
if(isset($_GET["location_id"])){
    echo json_encode($db->getLocationInformation($_GET['location_id']));
}
else{
    echo json_encode($db->getAllLocationInformation());
}

?>
