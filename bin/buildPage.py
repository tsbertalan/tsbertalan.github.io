#!/usr/var/env python
'''
@author:     Tom Bertalan
@contact:    tom@tombertalan.com
'''

import sys
import json

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from projectPageView import makePage
import utils

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    # Setup argument parser
    parser = ArgumentParser(description='buildPage', formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('descriptionFile')
    parser.add_argument('--destination', default='/tmp/test.html')
    
    # Process arguments
    args = parser.parse_args()
    
    print 'Got descriptionFile %s.' % args.descriptionFile
    data = json.load(open(args.descriptionFile, 'r'))
    print 'Got data: %s' % data
    
    print 'Generating page.'
    html = makePage(data['project name'], data['project description'])
    
    print 'Saving to %s.' % args.destination
    utils.writePage(html, args.destination)
    
    return args


if __name__ == "__main__":
    DEBUG = True
    if DEBUG:
        args = main(argv=['test.json'])
        utils.showPage(args.destination)
        
    else:
        main()