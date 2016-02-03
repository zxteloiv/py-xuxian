# coding: utf-8

import argparse

parser = argparse.ArgumentParser(description='xuxian script')

def define_logging_arguments(parser):
    parser.add_argument('--sys-log-path', metavar='/path/to/system/log', dest='sys_log_path',
                        default='./', help='The path to system logging')

    parser.add_argument('--log-level', dest='log_level', metavar='[DEBUG|INFO|WARNING|ERROR]',
                        default='INFO', help='choose the debug level')

define_logging_arguments(parser)


