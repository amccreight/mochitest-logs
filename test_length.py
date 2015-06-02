#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Print out the total number of bytes in each test.

import sys
import re



preludeRegexp = re.compile('INFO -  0 INFO SimpleTest START')
testStartRegexp = re.compile('INFO TEST-START \| (.*)')

inPrelude = True
currTest = None
currSize = 0
testSizes = {}

for l in sys.stdin:
    currSize += len(l)

    if inPrelude and preludeRegexp.search(l):
        inPrelude = False
        testSizes['prelude'] = currSize
        currSize = 0
        continue

    m = testStartRegexp.search(l)
    if m:
        newTest = m.group(1)
        if currTest:
            testSizes[currTest] = currSize - len(l)
            currSize = len(l)
        else:
            # Previous section was the prelude
            assert currSize == len(l)
        currTest = newTest


totalSize = 0

for t, size in testSizes.iteritems():
    print '{0:10} bytes from test {1}'.format(size, t)
    totalSize += size

totalSize += currSize

print '{0:10} bytes from the end'.format(currSize)

print 'total size of', totalSize, 'bytes.'
