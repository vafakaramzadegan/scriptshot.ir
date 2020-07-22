<?php

namespace Scriptshot\Mvc;

class View extends Controller{
    static private $hasView = true;
    static private $variables;

    public function __construct(){

    }

    public static function disable(){
        self::$hasView = false;
    }
 
    public static function enable(){
        self::$hasView = true;
    }

    public function render(){
        $viewPath = SCRIPTSHOT_VIEWS_DIR . '/' .
                    strtolower(parent::getControllerTitle()) . '/' .
                    strtolower(parent::getActionTitle()) .
                    SCRIPTSHOT_VIEW_EXT;

        if (file_exists($viewPath) && self::$hasView){
            echo self::parseTemplate(file_get_contents($viewPath));
        }            
    }

    private function parseTemplate($template){
        $output = $template;

        $keys = array_keys(self::$variables);
        $values = array_values(self::$variables);

        foreach ($keys as $k => $v){
            $keys[$k] = '{' . $v . '}';
        }

        $output = str_replace($keys, $values, $output);
        

        return $output;
    }

    public function __get($varName){
        if (!array_key_exists($varName, self::$variables)){
            throw new Exception('-----');
        } else return self::$variables[$varName];
    }

    public function __set($varName, $value){
        self::$variables[$varName] = $value;
    }
    
}