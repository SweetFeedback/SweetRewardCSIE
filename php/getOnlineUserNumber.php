<?php 
require_once("db.php");
require_once("onlineUser.php");

$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
refreshOnlineStatus($db);
$result['num_online_user'] = $db->getNumberOfOnlineUser();
echo json_encode($result);

?>
