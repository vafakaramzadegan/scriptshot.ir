<?php

require "Router.php";

$router = new Router();

$router->route("/", function(){
    echo "Welcome!";
});

$router->route("/users/profile", function($username="", $arg2){
    if (!$username){
        die("You have to pass an username as parameter!");
    }
    echo "Welcome $username!, $arg2";
});

$router->execute();
