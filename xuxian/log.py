# coding: utf-8

from __future__ import absolute_import

import logging
import logging.handlers

SEP_WILDCARD = '__comma__'
STANDARD_FORMAT = '%(asctime)-15s@%(process)d:%(filename)s:%(lineno)d:%(levelno)d$$ %(message)s'

def acquireLogger(logger_name='public', filename=None, level=logging.INFO):
    global STANDARD_FORMAT

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    handler = logging.handlers.WatchedFileHandler(filename if filename else './' + logger_name + '.log')
    formatter = logging.Formatter(STANDARD_FORMAT)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

class LogDict(dict):
    def __str__(self):
        global SEP_WILDCARD
        return ",".join('='.join(str(x).replace(',', SEP_WILDCARD) for x in pair)
                        for pair in self.iteritems())

def get_options(options=None):
    if options is None:
        import xuxian.options
        options = xuxian.options

    return options

system_logger = logging.getLogger('xuxian')

def str2level(level_string):
    if level_string == 'INFO':
        return logging.INFO
    elif level_string == 'DEBUG':
        return logging.DEBUG
    elif level_string == 'WARNING':
        return logging.WARNING
    elif level_string == 'ERROR':
        return logging.ERROR
    else:
        raise ValueError('cannot recognize the level: %s' % str(level_string))

