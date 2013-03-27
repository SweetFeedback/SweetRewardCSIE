<?php

require_once("db.php");
$coming_ip = $_SERVER['REMOTE_ADDR'];

if(isset($_GET["user_id"]) && isset($_GET["coordinate_x"]) && isset($_GET["coordinate_y"]) && isset($_GET["title"])){
    $user_id = $_GET["user_id"];
    $coordinate_x = $_GET["coordinate_x"];
    $coordinate_y = $_GET["coordinate_y"];
    $title = mysql_escape_string($_GET["title"]);
    if(isset($_GET["room_id"])){
        $room_id = $_GET["room_id"];
    }
    else{
        $room_id = 0;
    }
    $db_help = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    if(isset($_GET["category"]) && isset($_GET["room_id"])){
        $category = $_GET["category"];
        $db_help->insertFixReportByCategoryAndRoom($title, $coordinate_x, $coordinate_y, $user_id, $category, $room_id);
    }
    else if(isset($_GET["category"])){
        $category = $_GET["category"];
        $db_help->insertFixReportByCategory($title, $coordinate_x, $coordinate_y, $user_id, $category);
    }
    else{
        $db_help->insertFixReport($title, $coordinate_x, $coordinate_y, $user_id);
    }
}
?>
