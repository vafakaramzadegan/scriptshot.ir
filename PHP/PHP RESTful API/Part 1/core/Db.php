<?php

namespace Scriptshot;

use \PDO as PDO;

class Db{
    static private $connection;

    public function __construct(){
        self::$connection = new PDO(
            'mysql:host=' . DATABASE_SETTINGS['host'] .
            ';dbname=' . DATABASE_SETTINGS['database'] .
            ';charset=utf8',
            DATABASE_SETTINGS['user'],
            DATABASE_SETTINGS['password']
        );
        self::$connection->setAttribute(
            PDO::ATTR_ERRMODE,
            PDO::ERRMODE_EXCEPTION
        );
    }

    public static function getConnection(){
        return self::$connection;
    }
}