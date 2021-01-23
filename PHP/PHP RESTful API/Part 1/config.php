<?php

error_reporting(E_ERROR | E_WARNING | E_PARSE);

define('TIMEZONE', 'Asia/Tehran');

define('SCRIPTSHOT_DOCUMENT_ROOT', dirname(__FILE__) == '/' ? '' : dirname(__FILE__));

define('SCRIPTSHOT_CORE_DIR',        SCRIPTSHOT_DOCUMENT_ROOT . '/core');
define('SCRIPTSHOT_CONTROLLERS_DIR', SCRIPTSHOT_DOCUMENT_ROOT . '/application/controllers');

define('SCRIPTSHOT_VIEWS_DIR',       SCRIPTSHOT_DOCUMENT_ROOT . '/application/views');
define('SCRIPTSHOT_VIEWS_CACHE_DIR', SCRIPTSHOT_DOCUMENT_ROOT . '/application/_cache');
define('SCRIPTSHOT_VIEW_EXT',        '.svf');

define('SCRIPTSHOT_MODELS_DIR',      SCRIPTSHOT_DOCUMENT_ROOT . '/application/models');

define('SCRIPTSHOT_URI_PREFIX', '/api');

define('MAX_REQUESTS_PER_MINUTE', 20);

define('DATABASE_SETTINGS', array(
    'host' => 'localhost',
    'user' => '',
    'password' => '',
    'database' => 'api'
));
