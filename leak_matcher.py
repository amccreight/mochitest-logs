#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import re

# If you add a line like this to the ctor for a class:
#   printf_stderr("ZZZ CREATE %p\n", this);
# and a line line this to the dtor for a class:
#   printf_stderr("ZZZ DESTROY %p\n", this);
# then this log will process the resulting mochitest log
# and give you the mochitest that was running when any such
# objects were allocated that had no matching dtor.

cdMatch = re.compile('^.* ZZZ (CREATE|DESTROY) ([0-9A-F]+)\r?$')
anyUnknown = False

live = {}

currTest = None

for l in sys.stdin:
    if not 'ZZ' in l:
        if l.find("TEST-START") > -1:
            currTest = l.split('|')[1].strip()
        continue

    cdm = cdMatch.match(l)
    if not cdm:
        print 'Unknown line: ', l,
        anyUnknown = True
        continue
    isCreate = cdm.group(1) == 'CREATE'
    assert isCreate or cdm.group(1) == 'DESTROY'
    addr = cdm.group(2)
    if len(addr) != 8:
        print 'Not enough characters in address:', addr, l,

    if isCreate:
        if addr in live:
            print 'Duplicate creation of', addr
        assert currTest
        live[addr] = currTest
    else:
        assert addr in live
        del live[addr]


if anyUnknown:
    exit(-1)

testCounts = {}
for liveAddr, inTest in live.iteritems():
    testCounts[inTest] = testCounts.setdefault(inTest, 0) + 1

for t, n in testCounts.iteritems():
    print n, t

