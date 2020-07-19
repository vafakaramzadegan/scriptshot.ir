<?php

namespace Scriptshot;

class Router{
    private $requestURI;
    private $callback;

    private function parse($uri){
        return explode('/', trim(parse_url($uri, PHP_URL_PATH), '/'));
    }

    public function __construct(){
        $this->requestURI = $this->parse($_SERVER['REQUEST_URI']);
    }

    public function init($callback){
        $this->callback = $callback;
    }

    public function execute(){
        call_user_func_array($this->callback, $this->requestURI);
    }
}