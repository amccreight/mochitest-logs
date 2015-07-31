#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This prints out the tests that open the most windows.

import sys
import re
import time

winPatt = re.compile('(\d\d:\d\d:\d\d)\W+INFO -  (..)DOMWINDOW == (\d+).*\[pid = (\d+)\] \[serial = (\d+)\]')

def timeFromString(t):
    [hr, mi, se] = t.split(':')
    return ((60 * int(hr)) + int(mi)) * 60 + int(se)

def stringFromTime(t0):
    se = t0 % 60
    t = t0 / 60
    mi = t % 60
    h = t / 60
    return '{:0>2}:{:0>2}:{:0>2}'.format(h, mi, se)


def windowsPerSecondChart(windowsPerSecond):
    keys = sorted(windowsPerSecond.keys())
    prevKey = keys[0] - 1
    for k in keys:
        while prevKey + 1 < k:
            prevKey += 1
            print stringFromTime(prevKey)
        count = windowsPerSecond.get(k, 0)
        sys.stdout.write(stringFromTime(k) + ' ')
        i = 0
        while i < count:
            sys.stdout.write('*')
            i += 1
        print

        prevKey = k



test = None
numLive = 0

count = 0
peakNumLive = 0

counts = {}
peaks = {}

windowsPerSecond = {}

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
    if m.group(2) == '++':
        count += 1
        numLive += 1
        t = timeFromString(m.group(1))
        windowsPerSecond[t] = windowsPerSecond.setdefault(t, 1) + 1
        if numLive > peakNumLive:
            peakNumLive = numLive
    else:
        assert m.group(2) == '--'
        assert numLive > 0
        numLive -= 1



windowsPerSecondChart(windowsPerSecond)
exit(0)

keys = sorted(counts.keys())
keys.reverse()

print 'Number of windows opened in each test.'
for k in keys[:10]:
    print k, ', '.join(counts[k])
print


keys = sorted(peaks.keys())
keys.reverse()

print 'Peak number of live windows in each test.'
for k in keys[:10]:
    print k, ', '.join(peaks[k])

