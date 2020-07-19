<?php

use Scriptshot\Mvc\Controller;

class BaseController extends Controller{
    public function initialize(){
        parent::initialize();

        echo '<p style="color: red"><i>baseController Initialized</i></p>';
    }
}
