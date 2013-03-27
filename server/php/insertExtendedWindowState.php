<?php
require_once("db.php");
if(isset($_GET["window_id"]) && isset($_GET["state"])){
    $location_id = -1;
    $window_id = $_GET['window_id'];
    $state = $_GET['state'];
    $db= DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    if($_GET['location_id']){
        $location_id = $_GET['location_id'];
        $db->insertExtendedWindowState($location_id, $window_id, $state);
    }
    else{
        $db->insertExtendedWindowState2($window_id, $state);
    }
}
?>
