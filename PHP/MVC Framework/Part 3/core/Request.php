<?php

namespace Scriptshot\Mvc;

class Request{
    public function __construct(){
    }

    public function get($id){
        return (
            isset($_GET[$id]) ? $_GET[$id] : null
        );
    }

    public function post($id){
        return (
            isset($_POST[$id]) ? $_POST[$id] : null
        );
    }

    public function file($id){
        return (
            isset($_FILE[$id])? $_FILE[$id] : null
        );
    }

    public function redirect($url){
        header("Location: $url");
        exit();
    }

}