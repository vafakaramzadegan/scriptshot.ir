<?php

use Scriptshot\Mvc\Controller;

class IndexController extends BaseController{
    public function initialize(){
        parent::initialize();
    }

    public function indexAction(){
        echo '<h1>Homepage</h1>';
        echo '<p>Welcome!</p>';
    }
}