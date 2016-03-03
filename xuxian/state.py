# coding: utf-8

from __future__ import absolute_import

import logging
import logging.handlers

from xuxian.log import apply_logger

def remember(uniqueid, data, filename, charset='utf-8'):
    """
    Save the state for a program.
    """
    with open(filename, 'wb') as f:
        if isinstance(data, unicode):
            data = data.decode(charset)

        f.write(data)
        f.close()

def recall(uniqueid, filename):
    with open(filename, 'rb') as f:
        data = f.read().rstrip()
        f.close()

    return data
    
