<?php

use Scriptshot\Mvc\Controller;

class UsersController extends BaseController{
    public function initialize(){
        parent::initialize();
    }

    public function indexAction(){
        echo '<h1>Users</h1>';
        echo '<p>List</p>';
    }

    public function profileAction($username=""){
        echo '<h1>Users</h1>';
        echo "<p>$username's Profile</p>";
    }

    public function loginAction($username="", $password=""){
        echo '<h1>Users</h1>';
        echo "<p>login...</p>";

        if ($username == 'user' and $password == '123'){
            echo 'hi user!';
        } else {
            echo 'forbidden';
        }
    }
    
}