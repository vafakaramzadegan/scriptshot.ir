<?php

namespace Scriptshot;

spl_autoload_register(function($class){
    $fn = SCRIPTSHOT_CORE_DIR . '/' . end(explode('\\', $class)) . '.php';
    if (file_exists($fn)) require $fn;
});

class Core{
    public function __construct(){
        date_default_timezone_set(TIMEZONE);

        if (!file_exists(SCRIPTSHOT_CONTROLLERS_DIR)) die('Fatal: Controllers directory does not exist!');
        if (!file_exists(SCRIPTSHOT_MODELS_DIR)) die('Fatal: Model directory does not exist!');

        foreach (glob(SCRIPTSHOT_MODELS_DIR . '/*.php') as $filename)
            include($filename);

        $this->initRouter();
    }

    private function initRouter(){
        $router = new Router();

        $router->init(function(){
            list($controller, $action) = func_get_args();

            $params = (func_num_args() > 2 ? array_slice(func_get_args(), 2): []);

            $controller = ucfirst(
                $controller != '' ? filter_var(strtolower($controller), FILTER_SANITIZE_STRING) : 'Index'
            ) . 'Controller';

            $action = ($action == '' ? 'index' : filter_var(strtolower($action), FILTER_SANITIZE_STRING)). 'Action';

            if (file_exists(SCRIPTSHOT_CONTROLLERS_DIR . '/BaseController.php'))
                include(SCRIPTSHOT_CONTROLLERS_DIR . '/BaseController.php');

            if (file_exists(SCRIPTSHOT_CONTROLLERS_DIR . "/$controller.php")){

                include(SCRIPTSHOT_CONTROLLERS_DIR . "/$controller.php");

                $controllerHdl = new $controller($controller, $action);
                if (method_exists($controllerHdl, $action)){
                    $controllerHdl->initialize();
                    call_user_func_array(array($controllerHdl, $action), $params);
                } else {
                    die("404!");
                }

            } else {
                die('404');
            }
            

        });

        $router->execute();
    }
}
