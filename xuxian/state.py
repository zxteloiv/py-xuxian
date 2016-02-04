# coding: utf-8

from __future__ import absolute_import

import logging
import logging.handlers

from xuxian.log import apply_logger

def _remember(uniqueid, data, filename):
    """
    Save the state for a program.
    """
    with open(filename, 'wb') as f:
        f.write(data)
    
