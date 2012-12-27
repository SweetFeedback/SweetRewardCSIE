<?php
require_once("db.php");

$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));

$result = $db->getRankedRoomUnSolveExistReport();
$ret = array();
if($result != null){
    foreach( $result as $row){
        $information = $db->getLocationInformation(1);
        if( $information != null){
            $row['room_name'] = $information[0]['room_name'];
            $row['coordinate_x'] = $information[0]['coordinate_x'];
            $row['coordinate_y'] = $information[0]['coordinate_y'];
            $row['floor_level'] = $information[0]['floor_level'];
        }
        array_push($ret, $row);
    }
}
echo json_encode($ret);
?>
