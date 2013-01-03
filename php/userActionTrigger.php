<?php 
require_once("db.php");
require_once("policyAgent.php");

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
                if($window_id == 8 || $window_id == 9 || $window_id == 10){
                    $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "close the window at right time");
                    $ret['get_feedback'] = 1;
                }
                else if($window_id == 11 || $window_id == 12 || $window_id == 13){
                    $db->insertFeedbackStatusByDeviceId(2, 11, "positive", "close the window at right time");
                    $ret['get_feedback'] = 1;
                }
                else if($window_id == 1 || $window_id == 2){
                    $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "close the window at right time");
                    $ret['get_feedback'] = 1;
                }
            }
            else if($state == 1){
                if($window_id == 8 || $window_id == 9 || $window_id == 10){
                    $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "open the window at right time");
                    $ret['get_feedback'] = 1;
                }
                else if($window_id == 11 || $window_id == 12 || $window_id == 13){
                    $db->insertFeedbackStatusByDeviceId(2, 11, "positive", "open the window at right time");
                    $ret['get_feedback'] = 1;
                }
                else if($window_id == 1 || $window_id == 2){
                    $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "open the window at right time");
                    $ret['get_feedback'] = 1;
                }
            }
        }
        else{
            $ret['status'] = 1;
        }
    }
    else{
        $result = $db->getNewestExtendedWindowState($window_id);
        if($result != null){
            $state = $result[0]['state'];
            if($agent->judgeWindowStatus($state)){
                #print "the state is correct now";
                $ret = $db->getPeriodExtendedWindowState(1 - $state);
                if($ret != null){
                    if($state == 0){
                        if($window_id == 8 || $window_id == 9 || $window_id == 10){
                            $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "close the window at right time");
                            $ret['get_feedback'] = 1;
                        }
                        else if($window_id == 11 || $window_id == 12 || $window_id == 13){
                            $db->insertFeedbackStatusByDeviceId(2, 11, "positive", "close the window at right time");
                            $ret['get_feedback'] = 1;
                        }
                        else if($window_id == 1 || $window_id == 2){
                            $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "close the window at right time");
                            $ret['get_feedback'] = 1;
                        }
                    }
                    else if($state == 1){
                        if($window_id == 8 || $window_id == 9 || $window_id == 10){
                            $db->insertFeedbackStatusByDeviceId(1, 11, "positive", "open the window at right time");
                            $ret['get_feedback'] = 1;
                        }
                        else if($window_id == 11 || $window_id == 12 || $window_id == 13){
                            $db->insertFeedbackStatusByDeviceId(2, 11, "positive", "open the window at right time");
                            $ret['get_feedback'] = 1;
                        }
                        else if($window_id == 1 || $window_id == 2){
                            $db->insertFeedbackStatusByDeviceId(3, 11, "positive", "open the window at right time");
                            $ret['get_feedback'] = 1;
                        }
                    }
                }
            }
            else if(!$agent->judgeWindowStatus($state)){
                $ret['status'] = "1";
            }
        }
        else{
            $ret['status'] = "2";
        }
    }
    if( !array_key_exists('error', $ret) && !array_key_exists('no_data', $ret)){
        $ret['status'] = 0;
    }
    echo json_encode($ret);
}

?>

