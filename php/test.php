<?php
require_once("db.php");

$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
echo json_encode($db->getAllRoom());
#$db = new DB_PHIGET(Config::read('db.host.gardenia'), Config::read('db.basename.gardenia'), Config::read('db.user.gardenia'), Config::read('db.password.gardenia'));
#print_r($db->getExistReport());
#$db = new DB();
#if( isset($_GET["account"]) && isset($_GET["password"])){
#    $username = $_GET["account"];
#    $password = $_GET["password"];
#    $db = new DB();
#    $result = $db->verifyUser($username, $password);
#    echo json_encode($result);
#}

//echo $db->getNumberOfOnlineUser();
//echo $db->getMaxTimeStamp();
#$db->insertFeedbackStatusByDeviceId(2, 0, "positive");
//$db->getDeviceIdByIpAddr($_SERVER['REMOTE_ADDR']);
//echo $_SERVER['REMOTE_ADDR'];
?>
