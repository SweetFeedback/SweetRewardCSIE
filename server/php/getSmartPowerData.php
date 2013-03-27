<?php 
require_once("db_smartpower.php");

$db_smartpower = DB::getInstance(Config::read('db.host.gardenia'), Config::read('db.basename.smartpower'), Config::read('db.user.gardenia'), Config::read('db.password.gardenia'));
$result = array();

$temp = $db_smartpower->getNewestTempData();
if($temp != null){
    $result['temperature'] = $temp[0];
}
$sound = $db_smartpower->getNewestSoundData();
if($sound != null){
    $result['sound'] = $sound[0];
}
$humidity = $db_smartpower->getNewestHumidityData();
if($humidity != null){
    $result['humidity'] = $humidity[0];
}
$motion = $db_smartpower->getNewestMotionData();
if($motion != null){
    $result['motion'] = $motion[0];
}
$light = $db_smartpower->getNewestLightData();
if($light != null){
    $result['light'] = $light[0];
} 
echo json_encode($result);
?>
