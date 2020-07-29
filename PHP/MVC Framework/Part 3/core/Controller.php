<?php

namespace Scriptshot\Mvc;

use Scriptshot\Session;
use Scriptshot\Db;

abstract class Controller{
    static private $title;
    static private $action;
    
    public function __construct($title="", $action=""){
        self::$title = str_replace("Controller", "", $title);
        self::$action = str_replace("Action", "", $action);
    }

    public function initialize(){
        new Db();
        $this->view = new View();
        $this->session = new Session();
        $this->request = new Request();

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