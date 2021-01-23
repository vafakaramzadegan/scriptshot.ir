<?php

namespace Scriptshot;

class ExceptionHandler{
    public static function start(){
        set_exception_handler(array('Scriptshot\ExceptionHandler', 'handleException'));
        set_error_handler(array('Scriptshot\ExceptionHandler', 'handleError'));
        
    }

    public static function handleException($exception){
        die('custom: ' . $exception->getMessage());
    }

    public static function handleError($errno, $errstr, $errfile, $errline){
        if (!(error_reporting() & $errno)) return false;

        switch ($errno) {
            case E_WARNING:
                $bgColor = '#ffe082';
                $title = 'Warning';
                break;
            case E_NOTICE:
                $bgColor = '#ffe082';
                $title = 'Notice';
                break;   
            default:
                $bgColor = '#FFBABA';
                $title = 'Error';
                break;
        }

        echo '
        <div style="font-family: verdana; margin: 10px 0; padding: 10px; border-radius: 3px 3px 3px 3px; background-color: ' . $bgColor .  ';">
            <h4 style="margin-top: 0; color: #D8000C; font-size: 16px;">' . $title . '</h4>
            <p style="font-size: 14px; font-weight: normal;">Code: ' . $errno . '<br/>
            File: ' . $errfile . ' (<b>Line: ' . $errline .  '</b>)<br/><br/>
            Message: <b>' . $errstr . '</b><br/>
            </p>
            <p style="font-style: italic; font-size: 12px; font-weight: normal;">
                Scriptshot Framework - developed by: <a href="https://scriptshot.ir" target="_blank">Vafa Karamzadegan</a> | PHP ' . PHP_VERSION . ', on ' . PHP_OS . ' (' . date("Y/m/d h:i:s") . ')
            </p>
        </div>
        ';

        return true;
    }
}