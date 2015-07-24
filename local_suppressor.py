#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Parse in the leak results of an LSAN run, and a local suppression
# file, and print out the residual leaks, after taking into account
# the suppression file.

import sys
import re
import clean_lsan
import parse_suppressions
import argparse


# Argument parsing.

argsParser = argparse.ArgumentParser(description='Simulate the effect of an LSan suppression file on a set of traces.')

argsParser.add_argument('suppression_file_name',
                    help='suppression file name')

argsParser.add_argument('leak_traces_file_name',
                    help='leak traces file name')

argsParser.add_argument('--show-matched', '-sm', dest='showMatched', action='store_true',
                    default=False,
                    help='Show information about how traces were matched.')

argsParser.add_argument('--hide-unmatched', '-hu', dest='showUnmatched', action='store_false',
                    default=True,
                    help='Don\'t display residual traces that weren\'t matched by the suppression file.')


# Do stuff.

args = argsParser.parse_args()
suppressions = parse_suppressions.load_suppressions(sys.argv[1])
leaks = clean_lsan.load_log(sys.argv[2])

anySuppressions = len(suppressions) > 0

if anySuppressions:
    suppPatt = re.compile('(' + '|'.join([re.escape(s) for s in suppressions]) + ')')

matchedLeaks = []
unmatchedLeaks = []

for l in leaks:
    anyMatched = False
    if anySuppressions:
        for frame in l[3]:
            sm = suppPatt.search(frame)
            if sm:
                matchedLeaks.append([sm.group(1), frame])
                anyMatched = True
                break
    if not anyMatched:
        unmatchedLeaks.append(l)



sys.stderr.write('Local suppression file matched ' + str(len(matchedLeaks)) + ' stacks and failed to match ' + str(len(unmatchedLeaks)) + ' stacks.\n')

if args.showMatched and len(matchedLeaks) != 0:
    sys.stderr.write('Warning: this will only show the first matching frame.\n')
    for [m, leak] in matchedLeaks:
        print 'Matched', m, 'on frame', leak.strip()
    print

if args.showUnmatched and len(unmatchedLeaks) != 0:
    clean_lsan.print_traces(unmatchedLeaks)
