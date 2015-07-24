#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This prints out the tests that open the most windows.

import sys
import re

winPatt = re.compile('\d\d:\d\d:\d\d\W+INFO -  (..)DOMWINDOW == (\d+).*\[pid = (\d+)\] \[serial = (\d+)\]')

# XXX count the number of live windows at once. just do it manually.

test = None
numLive = 0

count = 0
peakNumLive = 0

counts = {}
peaks = {}

for l in sys.stdin:
    if l.find("TEST-START") > -1:
        if test:
            counts.setdefault(count, []).append(test)
            peaks.setdefault(peakNumLive, []).append(test)
        count = 0
        peakNumLive = numLive
        test = l.split('|')[1].strip()
    m = winPatt.match(l)
    if not m:
        continue
    if m.group(1) == '++':
        count += 1
        numLive += 1
        if numLive > peakNumLive:
            peakNumLive = numLive
    else:
        assert m.group(1) == '--'
        assert numLive > 0
        numLive -= 1




keys = sorted(counts.keys())
keys.reverse()

for k in keys[:10]:
    print k, ', '.join(counts[k])

print

keys = sorted(peaks.keys())
keys.reverse()

for k in keys[:10]:
    print k, ', '.join(peaks[k])

