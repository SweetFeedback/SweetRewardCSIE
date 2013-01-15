<?php 
require_once("db.php");
require_once("policyAgent.php");
define("SUCCESS", 0);
define("WRONG_STATE", 1);
define("NO_DATA", 2);
define("NO_FEEDBACK", 3);
# status 0 -> success
# status 1 -> status not correct
# status 2 -> no data error 
# status 3 -> no feedback 
if(isset($_GET['window_id']) && isset($_GET['token']) ){

    $db = DB::getInstance(Config::read('db.host'), Config::read('db.basename'), Config::read('db.user'), Config::read('db.password'));
    $agent = new PolicyAgent();
    $window_id = $_GET['window_id'];
    $token = $_GET['token'];
    $ret = array();
    if( isset($_GET['action']) ){
        $action = $_GET['action'];
        if($agent->judgeWindowStatus($action)){
            if($state == 0){
                if( ($window_id >= 8 && $window_id <= 13) || ($window_id == 1 || $window_id == 2)){
                    $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "close the window $window_id at right time");
                    $ret['get_feedback'] = $window_id;
                }
                else if ( $window_id >= 14 && $window_id <= 21 ){
                    $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "close the window $window_id at right time");
                    $ret['get_feedback'] = $window_id;
                }
            }
            else if($state == 1){
                if( ($window_id >= 8 && $window_id <= 13) || ($window_id == 1 || $window_id == 2)){
                    $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "open the window $window_id at right time");
                    $ret['get_feedback'] = $window_id;
                }
                else if ( $window_id >= 14 && $window_id <= 21 ){
                    $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "open the window $window_id at right time");
                    $ret['get_feedback'] = $window_id;
                }
            }
        }
        else{
            $ret['status'] = WRONG_STATE;
        }
    }
    else{
        $result = $db->getNewestExtendedWindowState($window_id);
        if($result != null){
            $state = $result[0]['state'];
            if($agent->judgeWindowStatus($state)){
                print "the state is correct now";
                $return_status = $db->getPeriodExtendedWindowState(1 - $state, $window_id);
                if($return_status != null){
                    if($state == 0){
                        if( ($window_id >= 8 && $window_id <= 13) || ($window_id == 1 || $window_id == 2)){
                            $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "close the window $window_id at right time");
                            $ret['get_feedback'] = $window_id;
                        }
                        else if ( $window_id >= 14 && $window_id <= 21 ){
                            $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "close the window $window_id at right time");
                            $ret['get_feedback'] = $window_id;
                        }
                    }
                    else if($state == 1){
                        if( ($window_id >= 8 && $window_id <= 13) || ($window_id == 1 || $window_id == 2)){
                            $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "open the window $window_id at right time");
                            $ret['get_feedback'] = $window_id;
                        }
                        else if ( $window_id >= 14 && $window_id <= 21 ){
                            $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "open the window $window_id at right time");
                            $ret['get_feedback'] = $window_id;
                        }
                    }
                }
                else{
                    $ret['status'] = NO_FEEDBACK;
                }
            }
            else if(!$agent->judgeWindowStatus($state)){
                $ret['status'] = WRONG_STATE;
            }
        }
        else{
            $ret['status'] = NO_DATA;
        }
    }
    if( !isset($ret['status'])){
        $ret['status'] = SUCCESS;
    }
    echo json_encode($ret);
}

?>

