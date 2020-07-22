<?php

namespace Scriptshot;

require(SCRIPTSHOT_CORE_DIR . '/Router.php');
require(SCRIPTSHOT_CORE_DIR . '/Controller.php');
require(SCRIPTSHOT_CORE_DIR . '/View.php');
require(SCRIPTSHOT_CORE_DIR . '/Session.php');

class Core{
    public function __construct(){
        date_default_timezone_set(TIMEZONE);

        if (!file_exists(SCRIPTSHOT_CONTROLLERS_DIR)) die('Fatal: Controllers directory does not exist!');

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
