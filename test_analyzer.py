#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Figure out which tests ran, and which had any failures.

import sys
import re


testOkPatt = re.compile('..:..:..     INFO -  \d+ INFO TEST-OK \| ([^ ]*)')
testFailPatt = re.compile('TEST-UNEXPECTED-FAIL \| ([^ ]*)')



def analyzeMochitestLog(mlog, disabledTestsFile):
    runningTests = set([])
    failedTests = set([])

    # Parse log for tests that ran and/or failed.
    for l in mlog:
        m = testOkPatt.match(l)
        if m:
            runningTests.add(m.group(1))
            continue

        m = testFailPatt.search(l)
        if m:
            failedTests.add(m.group(1))
            continue

    if 'leakcheck' in failedTests:
        print 'Some test leaked.'

    # Get the known list of tests that don't run in e10s.
    disabledTests = set([])
    for l in disabledTestsFile:
        disabledTests.add(l[:-1])

    okTests = []
    stillFailedTests = []

    for x in disabledTests:
        if not x in runningTests:
            continue
        if x in failedTests:
            stillFailedTests.append(x)
        else:
            okTests.append(x)

    okTests.sort()
    stillFailedTests.sort()

    print
    print 'Maybe could enable these tests:'
    for t in okTests:
        print ' ', t

    print
    print 'Still broken:'
    for t in stillFailedTests:
        print ' ', t




if len(sys.argv) < 3:
    sys.stderr.write('Not enough arguments.\n')
    exit()


f1 = open(sys.argv[1], 'r')
f2 = open(sys.argv[2], 'r')
analyzeMochitestLog(f1, f2)
f1.close()
f2.close()
