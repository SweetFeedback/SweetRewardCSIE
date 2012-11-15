<?php 
require_once("db.php");
require_once("onlineUser.php");

$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
refreshOnlineStatus($db);
$result = $db->getOnlineDeviceList();
if($result != null){
    echo json_encode($result);
}
else{
    return null;
}

?>
