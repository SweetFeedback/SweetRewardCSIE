<?php
require_once("../db.php");
$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
$result['success'] = 0;
if(isset($_GET['token'])){
    $token = $_GET['token'];
    $user_id = $db->getUserIdByToken($token);
    if($user_id != null){
        $result['data'] = $db->getUserPreference($user_id);
        $result['success'] = 1;
    }
}
echo json_encode($result);
?>
