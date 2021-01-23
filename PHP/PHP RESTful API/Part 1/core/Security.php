<?php

namespace Scriptshot;

class Security{
    public function __construct(){
    }

    public function random_srting($length=16){
        return bin2hex(openssl_random_pseudo_bytes($length));
    }

}