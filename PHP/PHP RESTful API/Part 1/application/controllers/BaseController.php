<?php

use Scriptshot\Mvc\Controller;
use Scriptshot\Security;
use Scriptshot\Filter;

class BaseController extends Controller{
    public function initialize(){
        parent::initialize();

        $this->view->disable();

        $filter = new Filter();

        $token = $filter->sanitize($this->request->header('X-API-KEY'), "alphanum");

        if (!isset($token)){
            $this->request->respond(401);
        }

        $auth = Apiauth::query()->where("token = '$token'")->select()[0];

        if (!$auth){
            $this->request->respond(401);
        }

        if ($auth->enabled == 0){
            $this->request->respond(401);
        }

        $now = time();

        if ($now - $auth->last_activity < (60 / MAX_REQUESTS_PER_MINUTE)){
            $this->request->respond(429);
        }

        $auth->last_activity = time();
        $auth->update();

    }
}
