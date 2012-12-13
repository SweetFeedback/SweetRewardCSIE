<?php 
require_once("db.php");
require_once("policyAgent.php");

if(isset($_GET['window_id']) && isset($_GET['token']) ){

    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $agent = new PolicyAgent();
    $window_id = $_GET['window_id'];
    $token = $_GET['token'];

    $ret = array();
    $result = $db->getNewestExtendedWindowState($window_id);
    if($result != null){
        $state = $result[0]['state'];
        if($agent->judgeWindowStatus($state)){
            #print "the state is correct now";
            $ret = $db->getPeriodExtendedWindowState(1 - $state);
            if($ret != null){
                if($state == 0){
                    $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "close the window");
                }
                else if($state == 1){
                    $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "open the window");
                }
            }
        }
        else if(!$agent->judgeWindowStatus($state)){
            $ret['error'] = "1";
        }
    }
    else{
        $ret['no_data'] = "1";
    }
    echo json_encode($ret);
}

?>

