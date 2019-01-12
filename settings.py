import os
import tornado
from tornado.options import define, options, parse_config_file 
from handlers.base import ErrorHandler


# Define file paths
ROOT = os.path.join(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(ROOT, "static")
TEMPLATE_ROOT = os.path.join(ROOT, "templates")


# Define global options
define("port", default=9080, help="server port", type=int)
define("debug", default=True, help="debug mode")
define("dbhost", default="localhost", help="db host")
define("dbport", default=27017, help="db port", type=int)
define("dbname", default="coloredlistdb", help="name of db")
define("cookie_secret", default=None, help="secret cookie")
define("config", default="config.conf", help="secret config")


# Read config file
if options.config:
    if os.path.exists(options.config):
        parse_config_file(options.config)


# Define application settings
settings = {}
settings['debug'] = options.debug
settings['static_path'] = STATIC_ROOT
settings['template_path'] = TEMPLATE_ROOT
settings['cookie_secret'] = options.cookie_secret
settings['default_handler_class'] = ErrorHandler


