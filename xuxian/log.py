#!/usr/bin/env python

from __future__ import absolute_import

import logging
import logging.handlers

import xuxian.script 
import xuxian.options


def acquireLogger(logger_name = 'public', filename = 'log/public/public.log'):
    logger = logger.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.WatchedFileHandler(filename)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

SEP_WILDCARD = '__comma__'

class LogDict(dict):
    def __str__(self):
        global SEP_WILDCARD
        return ",".join('='.join(str(x).replace(',', SEP_WILDCARD) for x in pair)
                        for pair in self.iteritems())

content = LogDict({"a":1, "b":2})

"""
FORMAT = '%(asctime)-15s %(levelno)d %(message)s'
logging.basicConfig(format=FORMAT, level=20)

logger = logging.getLogger('tcpserver')
logger.warning('Protocol problem: %s', 'connection reset')

access_log = logging.getLogger("xuxian.access")
access_log.info(content)
"""


#xuxian_logger = acquireLogger('xuxian', 
