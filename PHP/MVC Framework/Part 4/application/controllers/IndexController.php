<?php

use Scriptshot\Mvc\Controller;
use Scriptshot\Filter;

class IndexController extends BaseController{
    public function initialize(){
        parent::initialize();
    }

    public function indexAction(){
        $filter = new Filter();

        $this->view->products = Products::query()->
                                where("productLine = 'Motorcycles'")->
                                columns('*')->
                                limit($filter->sanitize($this->request->get('limit'), 'int'))->
                                order('MSRP DESC')->
                                select();
        
    }
}