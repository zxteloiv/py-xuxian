# coding: utf-8

import argparse

parser = argparse.ArgumentParser(description='xuxian script')

def define_logging_arguments(parser):
    parser.add_argument('--sys-log-path', metavar='/path/to/system/log', dest='sys_log_path',
                        default='./', help='The path to system logging')

    parser.add_argument('--log-level', dest='log_level', metavar='[DEBUG|INFO|WARNING|ERROR]',
                        default='INFO', help='choose the debug level')

def define_state_arguments(parser):
    parser.add_argument('--state-path', metavar='/path/to/parser', default='./',
                        help='The path to remember state')

define_logging_arguments(parser)
define_state_arguments(parser)

