<?php

class Router{
    private $requestURI;
    private $parameters;
    private $routeCallback;
    
    private function parse($uri){
        return explode("/", trim(parse_url($uri, PHP_URL_PATH), "/"));
    }
    
    public function __construct(){
        $this->requestURI = $this->parse($_SERVER["REQUEST_URI"]);
    }
    
    public function route($pattern, $callback){
        $routePattern = $this->parse($pattern);
        
        if (count($this->requestURI) >= count($routePattern)){
            $diff = array_diff_assoc($this->requestURI, $routePattern);
            
            if (count($diff) == count($this->requestURI) - count($routePattern)){
                $this->parameters = $diff;
                $this->routeCallback = $callback;
            }
        }
    }
    
    public function execute(){
        if ($this->routeCallback){
            call_user_func_array($this->routeCallback, $this->parameters);
        } else {
            header("HTTP/1.0 404 Not Found");
            echo "<h1>404 :-(</h1>";
        }
    }
}
