# coding: utf-8

from __future__ import absolute_import

import sys
import os
import traceback

import xuxian.options
import xuxian.log
import xuxian.state

from xuxian.log import LogDict, apply_logger, apply_dump_file

args = None

def get_parser():
    return xuxian.options.parser

def get_args():
    global args

    if args is None:
        args = xuxian.options.parser.parse_args()

    return args

def parse_args():
    global args

    if args is None:
        args = xuxian.options.parser.parse_args()

def remember(uniqueid, data):
    """
    Remeber the state of a program

    :param uniqueid, an id string that can identify a task independently with
                    a process after that process died it will restart with the
                    same uniqueid.
    :param data, a string that needs to be remembered and later to restore its
                state.

    :return nothing
    """
    global args

    xuxian.state._remember(uniqueid, data, args.state_path + '/' + uniqueid)

def recall(uniqueid):
    """
    Fetch the saved state of a program after it is restarted.

    :param uniqueid, an id string that can independently identify a task
    :return the data saved last time
    """
    global args
    return open(args.state_path + '/' + uniqueid, 'rb').read().strip()

def run(func):
    global args

    # init arguments, logs, state
    parse_args()
    log_level = xuxian.log.str2level(args.log_level)

    # start the script
    system_logger = xuxian.log.apply_logger('xuxian', args.sys_log_path + '/xuxian.info.log', log_level)
    system_logger.info('script started')

    try:
        rtn = func(args)
    except Exception as e:
        system_logger.error(traceback.format_exc())
        sys.exit(1)

    # script ends
    system_logger.info('script ended')
    sys.exit(rtn)

