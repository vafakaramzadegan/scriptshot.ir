<?php

use Scriptshot\Mvc\Controller;

class IndexController extends BaseController{
    public function initialize(){
        parent::initialize();
    }

    public function indexAction(){
        $this->view->name = $this->session->get("username");
        
    }
}