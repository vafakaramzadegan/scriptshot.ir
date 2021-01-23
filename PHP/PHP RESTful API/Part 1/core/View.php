<?php

namespace Scriptshot\Mvc;

class View extends Controller{
    static private $hasView = true;
    static private $variables;

    public function __construct(){
        if (!file_exists(SCRIPTSHOT_VIEWS_CACHE_DIR))
            if (!mkdir(SCRIPTSHOT_VIEWS_CACHE_DIR, 0755, true)) die('Fatal: unable to create view cache directory!<br/>you must do it manually!');

        if (!is_writable(SCRIPTSHOT_VIEWS_CACHE_DIR)) die('Fatal: view cache directory must be writeable!');
    
    }

    public static function disable(){
        self::$hasView = false;
    }
 
    public static function enable(){
        self::$hasView = true;
    }

    public function render(){
        $controller = strtolower(parent::getControllerTitle());
        $action = strtolower(parent::getActionTitle());

        $viewPath = SCRIPTSHOT_VIEWS_DIR . '/' .
                    $controller . '/' .
                    $action .
                    SCRIPTSHOT_VIEW_EXT;

        if (file_exists($viewPath) && self::$hasView){
            $php_file = SCRIPTSHOT_VIEWS_CACHE_DIR . '/' . md5($controller . $action);
            file_put_contents($php_file, self::parseTemplate(file_get_contents($viewPath)));
            include $php_file;
        }            
    }

    private function parseTemplate($template){
        $output = $template;

        $output = preg_replace('/{([\S\t]+)}/i', '<?= $$1 ?>', $output);        

        return $output;
    }

    public function __get($varName){
        if (array_key_exists($varName, self::$variables)) return self::$variables[$varName];
    }

    public function __set($varName, $value){
        self::$variables[$varName] = $value;
    }
    
}