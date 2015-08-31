#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This file analyzes the output of running with MOZ_IPC_MESSAGE_LOG=1

import sys
import re

msgPatt = re.compile('^\[time:(\d+)\]\[(\d+)(->|<-)(\d+)\]\[([^\]]+)\] (Sending|Received)((?: reply)?) ([^\(]+)\(\[TODO\]\)$')

#[time:1441041587246153][9641->9647][PPluginScriptableObjectParent] Sending reply Reply_NPN_Evaluate([TODO])


matchCount = 0
notMatchCount = 0

msgCounts = {}

for l in sys.stdin:
    mm = msgPatt.match(l)
    if not mm:
        notMatchCount += 1
        continue
    timeStamp = mm.group(1)
    pid1 = mm.group(2)
    arrow = mm.group(3)
    pid2 = mm.group(4)
    actor = mm.group(5)
    sendRecv = mm.group(6)
    sendRecvExtra = not not mm.group(7)
    msg = mm.group(8)

    p = (actor, msg)
    msgCounts[p] = msgCounts.setdefault(p, 0) + 1

    #print timeStamp, pid1, arrow, pid2, actor, sendRecv, sendRecvExtra, msg

    matchCount += 1


# Resort the data a bit.

counts = []
for p, count in msgCounts.iteritems():
    counts.append((count, p))

counts.sort()
counts.reverse()

for (count, (actor, msg)) in counts:
    print count, actor, msg





