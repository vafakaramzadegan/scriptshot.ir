#include "php.h"

extern zend_module_entry scriptshot_module_entry;

PHP_FUNCTION(scriptshot_execute)
{
    char *arg = NULL;
    size_t arg_len;

    if (zend_parse_parameters(ZEND_NUM_ARGS(), "s", &arg, &arg_len) == FAILURE) {
        return;
    }

    php_printf(arg);
    
}

PHP_MINFO_FUNCTION(scriptshot)
{
    php_info_print_table_start();
    php_info_print_table_header(2, "Scriptshot", "enabled");
    php_info_print_table_row(2, "Description", "A guide to PHP extension development");
    php_info_print_table_row(2, "Author", "Vafa Karamzadegan/scriptshot.ir");
    php_info_print_table_row(2, "More information on", "github.com/vafakaramzadegan/scriptshot.ir");
    php_info_print_table_end();
}

const zend_function_entry scriptshot_functions[] = {
    PHP_FE(scriptshot_execute, NULL)

    PHP_FE_END
};

zend_module_entry scriptshot_module_entry = {
    STANDARD_MODULE_HEADER,
    "Scriptshot",
    scriptshot_functions,
    NULL,
    NULL,
    NULL,
    NULL,
    PHP_MINFO(scriptshot),
    "1.0.0",
    STANDARD_MODULE_PROPERTIES
};

#ifdef COMPILE_DL_SCRIPTSHOT
#ifdef ZTS
ZEND_TSRMLS_CACHE_DEFINE()
#endif
ZEND_GET_MODULE(scriptshot)
#endif
