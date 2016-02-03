# coding: utf-8

from __future__ import absolute_import

import sys

import xuxian.options
import xuxian.log

args = None
unknown = []

def get_parser():
    return xuxian.options.parser

def get_args():
    global args
    global unknown

    if args is None:
        args = xuxian.options.parser.parse_args()

    return (args, unknown)

def run(func):
    global args

    log_level = xuxian.log.str2level(args.log_level)


    system_logger = xuxian.log.acquireLogger('xuxian', args.sys_log_path + '/xuxian.info.log', log_level)

    system_logger.info('script started')
    rtn = func(args)

    system_logger.info('script ended')
    sys.exit(rtn)

