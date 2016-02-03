# coding: utf-8

import xuxian

# if any command to add
parser = xuxian.get_parser()
parser.add_argument('--test', nargs='+')

def main(arguments):
    print arguments

if __name__ == "__main__":
    args, unknown = xuxian.get_args()
    xuxian.run(main)

