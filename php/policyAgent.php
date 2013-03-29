<?php
class PolicyAgent{
    public function __construct(){
        date_default_timezone_set("Asia/Chongqing"); 
    } 

    public function judgeWindowStatus($window_status){
        $date = new DateTime();
        #echo $date->getTimeStamp();
        $hour = date('H', $date->getTimeStamp());
        if( $hour >= 8 && $hour <= 19) {
            // day time 
            if( $window_status == 1 ){
                return false;
            }
            else{
                return true;
            }
        }
        else{
            // night time 
            if( $window_status == 1 ){
                return true;
            }
            else{
                return false;
            }
        }
    } 
}
?>
