import logging
from logging.handlers import RotatingFileHandler
from dbapp import *

LOG_FORMAT = logging.Formatter("%(levelname)s - %(asctime)s - %(funcName)s - %(message)s")
log_file = "/var/www/kwasny.yao.cl/public_html/mess2/mess2/log/mess.log"

my_handler = RotatingFileHandler(log_file, mode = "a", encoding = None,
                    delay = 0, maxBytes = 1024*1024*5, backupCount = 20)
                    
my_handler.setFormatter(LOG_FORMAT)
my_handler.setLevel(logging.INFO)

logger = logging.getLogger('root')
logger.setLevel(logging.INFO)

logger.addHandler(my_handler)

#import routes2