<?php

use Scriptshot\Mvc\Controller;

class BaseController extends Controller{
    public function initialize(){
        parent::initialize();

        $this->session->set("username", "Vafa Karamzadegan");
    }
}
