__author__ = 'erik'

import logging


class Logger:
    def __init__(self):
        self.logger = logging
        self.logger.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S',
                                filename='log.txt', level=logging.DEBUG)

    def get_logger(self):
        return self.logger
