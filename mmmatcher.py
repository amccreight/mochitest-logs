#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re
import sys

addPatt = re.compile("QQQ AddMessageListener (.+)$")
addWeakPatt = re.compile("QQQ AddWeakMessageListener (.+)$")
recvPatt = re.compile("QQQ ReceiveMessage (.+)$")

def mmMatcher():
    added = set([])
    recv = set([])

    sys.stdin.reconfigure(encoding='latin1')
    for l in sys.stdin:
        recvMatch = recvPatt.search(l)
        if recvMatch:
            r = recvMatch.group(1).rstrip()
            recv.add(r)
            continue
        a = None
        addMatch = addPatt.search(l)
        if addMatch:
            a = addMatch.group(1).rstrip()
        else:
            addMatch = addWeakPatt.search(l)
            if addMatch:
                a = recvMatch.group(1).rstrip()
            else:
                continue
        added.add(a)

    print("Listener added without any received message:")
    print(", ".join(sorted(added - recv)))
    print()
    print("Message received but no listener added:")
    print(", ".join(sorted(recv - added)))


mmMatcher()

