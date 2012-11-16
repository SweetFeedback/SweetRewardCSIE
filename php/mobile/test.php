<?php
require_once("../db.php");
#$db = new DB();
$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
$db->insertFeedbackStatusByUserId(2, 20, "positive");

?>
