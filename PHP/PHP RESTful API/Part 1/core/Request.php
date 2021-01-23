<?php

namespace Scriptshot\Mvc;

class Request{
    public function __construct(){
    }

    public function header($id){
        return $_SERVER["HTTP_" . str_replace('-', '_', $id)];
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

    public function respond($code, $desc="", $data=[]){
        switch ($code){
            case 200:
                $msg = '';
                $desc = '';
            break;
            case 400:
                $msg = '';
                $desc = '';
            break;
            case 401:
                $msg = 'ERR_UNAUTHORIZED';
                $desc = 'authentication failed or has not yet been provided.';
            break;
            case 404:
                $msg = '';
                $desc = '';
            break;
            case 429:
                $msg = 'ERR_TOO_MANY_REQUESTS';
                $desc = 'too many requests in a given amount of time.';
            break;
        }

        $response = [
            'code' => $code,
            'msge' => $msg,
            'desc' => $desc
        ];

        $response = json_encode($response);

        header('X-PHP-Response-Code: ' . $code, true, $code);
        header('X-Powered-By: Genome/1.1');
        header('Content-Type: application/json');

        echo $response;
        exit();
    }

}