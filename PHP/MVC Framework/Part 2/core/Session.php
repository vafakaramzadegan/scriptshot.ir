<?php

namespace Scriptshot;

class Session{
    public function __construct(){
        session_start();
    }

    public function destroy(){
        session_unset();
        session_destroy();
        return true;
    }

    public function set($id, $value){
        $_SESSION[$id] = $value;
    }

    public function get($id){
        return $_SESSION[$id];
    }

    public function unset($id){
        unset($_SESSION[$id]);
        return true;
    }

}