<?
require_once("db.php");
$db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
$result = $db->getRankedRoomSolveExistReport();
if($result != null){
    echo json_encode($result);
}
    
?>
