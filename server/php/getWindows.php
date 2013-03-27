<?php 
require_once("db.php");

$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
if(isset($_GET["window_id"])){
    echo json_encode($db->getWindowInformation($_GET['window_id']));
}
else{
    echo json_encode($db->getAllWindowsInformation());
}

?>
