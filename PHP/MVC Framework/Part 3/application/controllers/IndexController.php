<?php

use Scriptshot\Mvc\Controller;

class IndexController extends BaseController{
    public function initialize(){
        parent::initialize();
    }

    public function indexAction(){
        $products = Products::query()->
                                where("productLine = 'Motorcycles'")->
                                columns('*')->
                                limit(10)->
                                order('MSRP DESC')->
                                select();

        $this->view->data = '';
        foreach ($products as $key => $p){
            $this->view->data .=
            sprintf("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s$</td></tr>", $p->productCode, $p->productName, $p->productScale, $p->MSRP);
        }
        
    }
}