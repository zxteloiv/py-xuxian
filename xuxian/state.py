# coding: utf-8

from __future__ import absolute_import

import logging
import logging.handlers

from xuxian.log import apply_logger

def _remember(uniqueid, data, filename):
    """
    Save the state for a program.
    """
    logger = apply_logger('_xuxian_state_' + uniqueid, filename=filename,
            format='%(message)s', writing_mode='wb')

    logger.info(data)
    
