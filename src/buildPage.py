#!/usr/local/bin/python2.7
# encoding: utf-8
'''
buildPage -- Make a project description page from a set of input files.
@author:     Tom Bertalan
@contact:    tom@tombertalan.com
'''

import sys
import json

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    try:
        # Setup argument parser
        parser = ArgumentParser(description='buildPage', formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('descriptionFile')
        
        # Process arguments
        args = parser.parse_args()
        
        print 'Got descriptionFile %s.' % args.descriptionFile
        data = json.load(open(args.descriptionFile, 'r'))
        print 'Got data: %s' % data

        return 0
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        sys.exit(main(argv=['test.json']))
    else:
        sys.exit(main())