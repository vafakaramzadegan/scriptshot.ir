<?php

use Scriptshot\Mvc\Controller;
use Scriptshot\Filter;

class IndexController extends BaseController{
    public function initialize(){
        parent::initialize();
    }

    public function indexAction(){
        $filter = new Filter();

        $products = Products::query()->
                                where("productLine = 'Motorcycles'")->
                                columns('*')->
                                limit(10)->
                                order('MSRP DESC')->
                                select();

        echo json_encode($products);
        
    }
}