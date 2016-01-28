#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Print out each tab process created during a test run, and the test it was created during.

import sys
import re
import time


procStartPatt = re.compile('^\d\d:\d\d:\d\d\W+INFO -  ### XPCOM\_MEM\_BLOAT\_LOG defined -- logging bloat\/leaks to .+runtests\_leaks\_tab\_pid(\d+)\.log')


def testDir(testName):
    return currTest.rsplit('/', 1)[0] + '/'

# Parse the input looking for when tests run.

pidTests = {}

currTest = None

for l in sys.stdin:
    if l.find("TEST-START") > -1:
        currTest = l.split('|')[1].strip()
    m = procStartPatt.match(l)
    if not m:
        continue
    currProc = int(m.group(1))
    if currProc in pidTests and testDir(currTest) == testDir(pidTests[currProc]):
        # This assumes run-by-dir.
        print('WARNING! Possible replay of pid ' + str(currProc) + ' in test dir ' + testDir(currTest))
    pidTests.setdefault(currProc, []).append(currTest)
    print 'Found proc start:', currProc, currTest




