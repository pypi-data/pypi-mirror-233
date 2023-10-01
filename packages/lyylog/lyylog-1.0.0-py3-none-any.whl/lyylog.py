

from datetime import datetime

import logging
from logging.handlers import TimedRotatingFileHandler
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = None

class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def lyyf_logger(log_filename_prefix, message, if_print=False):
    if if_print:
        print(message)
    global handler
    if handler is None:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        handler = CustomTimedRotatingFileHandler(f'lyylog_{log_filename_prefix}_{today}.log', when='midnight', interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    with handler:
        logger.info(message)