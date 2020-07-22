<?php

namespace Scriptshot\Mvc;

use Scriptshot\Session;

abstract class Controller{
    static private $title;
    static private $action;
    
    public function __construct($title="", $action=""){
        self::$title = str_replace("Controller", "", $title);
        self::$action = str_replace("Action", "", $action);
    }

    public function initialize(){
        $this->view = new View();
        $this->session = new Session();

        register_shutdown_function(
            function(){
                if ($this->view) $this->view->render();
            }
        );
    }

    public function getControllerTitle(){
        return self::$title;
    }

    public function getActionTitle(){
        return self::$action;
    }

}