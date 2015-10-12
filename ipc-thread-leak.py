#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import re


# Simple script to report the name of leaked threads, with the
# addition of some custom logging.

threadPatt = re.compile('^..:..:..     INFO -  METHREAD (0x[a-f0-9]*) (a\+\+|b\-\-)')
clipAt = len('17:05:48     INFO -  METHREAD 0x7f96a0df4f80 a++ ')


def reportLeakedThread(f):
    live = {}

    for l in sys.stdin:
        threadMatch = threadPatt.match(l)
        if not threadMatch:
            continue
        addr = threadMatch.group(1)
        if threadMatch.group(2).startswith('b'):
            assert addr in live
            del live[addr]
        else:
            threadName = l[clipAt:-1]
            # It is possible we leaked a thread in a previous run at the
            # same address, which would make this assertion trigger.
            assert not addr in live
            live[addr] = threadName

    nameCounts = {}
    for _, name in live.iteritems():
        nameCounts[name] = nameCounts.setdefault(name, 0) + 1

    print 'Name\t\t\tNum leaked'
    for name, count in nameCounts.iteritems():
        print name, '\t', count


reportLeakedThread(sys.stdin)

