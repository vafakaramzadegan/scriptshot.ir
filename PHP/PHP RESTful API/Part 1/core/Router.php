<?php

namespace Scriptshot;

class Router{
    private $requestURI;
    private $callback;

    private function parse($uri){
        return explode('/', trim(parse_url($uri, PHP_URL_PATH), '/'));
    }

    public function __construct(){
        $request_uri = $this->parse($_SERVER['REQUEST_URI']);
        $path_mask = $this->parse(SCRIPTSHOT_URI_PREFIX);

        $this->requestURI = array_diff_assoc($request_uri, $path_mask);
    }

    public function init($callback){
        $this->callback = $callback;
    }

    public function execute(){
        call_user_func_array($this->callback, $this->requestURI);
    }
}