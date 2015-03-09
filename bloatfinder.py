#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This prints out the tests that open the most windows.

import sys


test = None
count = 0

counts = {}

for l in sys.stdin:
    if l.find("TEST-START") > -1:
        if test:
            counts.setdefault(count, []).append(test)
        count = 0
        test = l.split('|')[1].strip()
    if l.find("++DOMWINDOW") > -1:
        count += 1




keys = sorted(counts.keys())
keys.reverse()


for k in keys[:10]:
    print k, ', '.join(counts[k])

