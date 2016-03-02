# coding: utf-8

from __future__ import absolute_import

import logging
import logging.handlers

STANDARD_FORMAT = '%(asctime)-15s@%(process)d:%(filename)s:%(lineno)d:%(levelno)d$$ %(message)s'

logger_memory = set()

def apply_logger(logger_name='public', filename=None, level=logging.INFO, format=STANDARD_FORMAT,
        writing_mode='a'):
    global logger_memory 
    logger = logging.getLogger(logger_name)

    if logger_name in logger_memory:
        return logger

    logger_memory.add(logger_name)

    logger.setLevel(level)

    handler = logging.handlers.WatchedFileHandler(filename if filename else './' + logger_name + '.log',
            writing_mode)
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger

class LogDict(dict):
    def __str__(self):
        global SEP_WILDCARD
        return ";".join('='.join(str(x).replace(';', ',') for x in pair)
                        for pair in self.iteritems())

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

def apply_dump_file(name, filename):
    logger = apply_logger(name, filename, logging.INFO, '%(message)s')
    return logger

