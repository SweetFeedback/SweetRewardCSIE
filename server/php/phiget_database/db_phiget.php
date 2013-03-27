<?php 
require_once("../config.php");
class DB_PHIGET{
    public $dbh;
    private static $instance;
    
    public function __construct($hostname, $dbname, $username, $password){
        $dsn = 'mysql:host='.$hostname.';dbname='.$dbname;
        try{
           $this->dbh = new PDO($dsn, $username, $password);
        }
        catch(PDOException $e){
        }
    } 
    public static function getInstance($hostname, $dbname, $username, $password){
        if(!isset(self::$instance)){
            $object = __CLASS__;
            self::$instance = new $object($hostname, $dbname, $username, $password);
        }
        return self::$instance;
    }
    public function getSensorData(){
    
    }
}
?>
