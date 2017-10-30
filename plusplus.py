#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Analyze the ++/-- DOMWINDOW in a TBPL log.

import re
import sys

winPatt = re.compile('\d\d:\d\d:\d\d\W+INFO -  GECKO\(\d+\) \| (..)DOMWINDOW == (\d+).*\[pid = (\d+)\] \[serial = (\d+)\]')

#13:42:33     INFO -  GECKO(1652) | ++DOMWINDOW == 1 (0D89C800) [pid = 1652] [serial = 1] [outer = 00000000]



def findLeakers():
    live = set([])

    for l in sys.stdin:
        m = winPatt.match(l)
        if not m:
            continue
        isNew = m.group(1) == '++'
        assert isNew or m.group(1) == '--'

        numLive = int(m.group(2))
        pid = int(m.group(3))
        serial = int(m.group(4))

        #print isNew, 'XXX serial=' , serial, 'XXX pid=', pid, 'XXX', l[:-1]

        winId = (pid, serial)

        if isNew:
            live.add(winId)
        else:
            assert winId in live
            live.remove(winId)


    # Print out information about leaking windows.
    for x in live:
        print "[pid = {0}] [serial = {1}]".format(x[0], x[1])


findLeakers()
