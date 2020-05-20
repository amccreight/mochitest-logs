#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Analyze the ++/-- DOMWINDOW in a TBPL log.

import re
import sys

winPatt = re.compile('INFO -\W+GECKO\(\d+\) \| (..)DOMWINDOW == (\d+).*\[pid = (\d+)\] \[serial = (\d+)\]')

def findLeakers():
    live = set([])
    foundAny = False

    for l in sys.stdin:
        m = winPatt.search(l)
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
            foundAny = True
        else:
            assert winId in live
            live.remove(winId)


    if not foundAny:
        print("Didn't find any windows in the log.")

    # Print out information about leaking windows.
    for x in live:
        print "[pid = {0}] [serial = {1}]".format(x[0], x[1])


findLeakers()
