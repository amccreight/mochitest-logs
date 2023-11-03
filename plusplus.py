#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Analyze the ++/-- DOMWINDOW in a TBPL log.

import re
import sys

winPatt = re.compile('.*I/DocShellAndDOMWindowLeak (..)DOMWINDOW == (\d+).*\[pid = (\d+)\] \[serial = (\d+)\] \[[^\]]+\].?(\[url = [^\]]+)?')
urlLen = len('[url = ')

#[task 2020-05-19T14:19:44.223Z] 14:19:44     INFO - GECKO(1230) | [(null) 1230: Main Thread]: I/DocShellAndDOMWindowLeak ++DOMWINDOW == 1 (0x7fc8cc397520) [pid = 1230] [serial = 1] [outer = (nil)]

#[task 2020-05-19T14:19:59.248Z] 14:19:59     INFO - GECKO(1230) | [Child 1308: Main Thread]: I/DocShellAndDOMWindowLeak --DOMWINDOW == 3 (0x7f4be4689400) [pid = 1308] [serial = 2] [outer = (nil)] [url = about:blank]

def findLeakers():
    live = {}
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
        url = m.group(5)
        if url:
            url = url[urlLen:]

        if url:
            print("URL ME " + url)

        winId = (pid, serial)

        if isNew:
            assert not winId in live
            assert url is None
            live[winId] = url
            foundAny = True
        else:
            assert winId in live
            del live[winId]


    if not foundAny:
        print("Didn't find any windows in the log.")

    # Print out information about leaking windows.
    for x, url in live.items():
        print("[pid = {0}] [serial = {1}] URL was {2}".format(x[0], x[1], url))


findLeakers()
