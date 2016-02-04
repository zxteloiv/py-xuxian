# coding: utf-8

import xuxian

# add any param by user
parser = xuxian.get_parser()
parser.add_argument('--test', required=True)
parser.add_argument('--test-optional')

def main(arguments):
    # arguments from framework
    print "arguments from framework:", arguments

    # get argument, test xuxian api
    print "test xuxian get_args:", xuxian.get_args()

    print "now save state: ..."
    xuxian.remember('hakurei', 'reimu')
    print 'check saved state[reimu@hakurei]:', ('reimu' == xuxian.recall('hakurei'))

if __name__ == "__main__":
    xuxian.run(main)

