<?php

use Scriptshot\Core;

header('X-Powered-By: Scriptshot Framework / scriptshot.ir');

require('../config.php');
require(SCRIPTSHOT_CORE_DIR . '/Core.php');

$app = new Core();
