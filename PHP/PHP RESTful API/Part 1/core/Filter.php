<?php

namespace Scriptshot;

class Filter extends Mvc\Controller{
    public function __construct(){

    }

    public function sanitize($value, $filter){
        switch ($filter){
            case 'int':
                return filter_var(
                    $value,
                    FILTER_SANITIZE_NUMBER_INT
                );
            case 'int':
                return filter_var(
                    $value,
                    FILTER_SANITIZE_NUMBER_FLOAT
                );
            case 'string':
                return filter_var(
                    $value,
                    FILTER_SANITIZE_STRING
                );
            case 'alphanum':
                return preg_replace(
                    '/[^a-zA-Z0-9]+/',
                    '',
                    $value
                );
                
        }
    }
}