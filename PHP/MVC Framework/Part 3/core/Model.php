<?php

namespace Scriptshot\Mvc;

use Scriptshot\Db;

class Model{
    private static $conditions = '';
    private static $columns = '*';
    private static $limit = '';
    private static $order = '';

    public function __construct(){

    }

    private function getConnection(){
        return Db::getConnection();
    }

    private function getFields(){
        $reflect = new \ReflectionClass($this);
        $props = $reflect->getProperties(
            \ReflectionProperty::IS_PUBLIC
        );
        $fields = array();
        foreach ($props as $p)
            array_push($fields, $p->name);
        return $fields;
    }

    public function query(){
        return new static;
    }

    public function where($str){
        self::$conditions = " WHERE $str";
        return $this;
    }
    public function andWhere($str){
        self::$conditions .= " AND $str";
        return $this;
    }
    public function orWhere($str){
        self::$conditions .= " OR $str";
        return $this;
    }

    public function limit($int){
        self::$limit = " LIMIT $int";
        return $this;
    }

    public function order($str){
        self::$order = " ORDER BY $str";
        return $this;
    }

    public function columns($str){
        self::$columns = $str;
        return $this;
    }

    public function select(){
        $modelTitle = strtolower(get_class($this));
        $model = new $modelTitle();

        $stmt = $model->getConnection()->
                prepare("SELECT " . self::$columns . " FROM " . $modelTitle . self::$conditions . self::$order . self::$limit);
        $stmt->execute();
        
        $records = json_decode(
            json_encode($stmt->fetchAll(2)),
            False
        );

        foreach ($records as $key => $rec){
            $result[$key] = new $modelTitle();
            foreach ($result[$key]->getFields() as $f)
                if (strpos(self::$columns, $f) !== false OR self::$columns == "*")
                    $result[$key]->$f = $rec->$f;
        }

        return $result;
    }

}