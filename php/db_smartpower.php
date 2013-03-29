<?php 
require_once("config.php");
class DB{
    public $dbh;
    public $data_tableName = "data";
    
    private static $instance;
    public static function getInstance($hostname, $dbname, $user, $password){
        if(!isset(self::$instance)){
            $object = __CLASS__;
            self::$instance = new $object($hostname, $dbname, $user, $password);
        }
        return self::$instance;
    }
    public function __construct($hostname, $dbname, $user, $password)
    {
        $dsn = 'mysql:host='.$hostname.';dbname='.$dbname;
        try{
            $this->dbh = new PDO($dsn, $user, $password);
            date_default_timezone_set('America/Los_Angeles');
        }
        catch(PDOException $e){
        } 
    }
    public function getNewestTempData(){
        $query = "select * from $this->data_tableName where sensor_name=\"temperature\" order by timestamp limit 1";
        $result = $this->dbh->query($query);
        if($result->rowCount() > 0){
            return ($result->fetchAll());
        }
        return null;
    }
    public function getNewestSoundData(){
        $query = "select * from $this->data_tableName where sensor_name=\"sound\" order by timestamp limit 1";
        $result = $this->dbh->query($query);
        if($result->rowCount() > 0){
            return ($result->fetchAll());
        }
        return null;
    }
    public function getNewestHumidityData(){
        $query = "select * from $this->data_tableName where sensor_name=\"humidity\" order by timestamp limit 1";
        $result = $this->dbh->query($query);
        if($result->rowCount() > 0){
            return ($result->fetchAll());
        }
        return null;
    }
    public function getNewestMotionData(){
        $query = "select * from $this->data_tableName where sensor_name=\"motion\" order by timestamp limit 1";
        $result = $this->dbh->query($query);
        if($result->rowCount() > 0){
            return ($result->fetchAll());
        }
        return null;
    }
    public function getNewestLightData(){
        $query = "select * from $this->data_tableName where sensor_name=\"light\" order by timestamp limit 1";
        $result = $this->dbh->query($query);
        if($result->rowCount() > 0){
            return ($result->fetchAll());
        }
        return null;
    }
}
?>
