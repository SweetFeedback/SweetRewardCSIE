<?php
require_once("db.php");
if(isset($_GET['id'])){
    $id = $_GET['id'];
    #$db = new DB();
    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $db->updateFeedbackStatusBy($id);
}
?>
