<?php

error_reporting(E_ERROR | E_WARNING | E_PARSE);

define('TIMEZONE', 'Asia/Tehran');

define('SCRIPTSHOT_DOCUMENT_ROOT', dirname(__FILE__) == '/' ? '' : dirname(__FILE__));

define('SCRIPTSHOT_CORE_DIR',        SCRIPTSHOT_DOCUMENT_ROOT . '/core');
define('SCRIPTSHOT_CONTROLLERS_DIR', SCRIPTSHOT_DOCUMENT_ROOT . '/application/controllers');
