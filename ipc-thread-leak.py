#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import re


# Simple script to report the name of leaked threads, with the
# addition of some custom logging.

threadPatt = re.compile('^..:..:..     INFO -  METHREAD (0x[a-f0-9]*) (a\+\+|b\-\-)')
clipAt = len('17:05:48     INFO -  METHREAD 0x7f96a0df4f80 a++ ')


mochiPatt = re.compile('^..:..:..     INFO -  \d+ INFO TEST-([^ ]+) | (.+)$')

def reportLeakedThread(f, printLeakAddrs=False):
    live = {}
    currTest = 'Unknown'

    for l in f:
        threadMatch = threadPatt.match(l)
        if not threadMatch:
            mm = mochiPatt.match(l)
            if mm:
                if mm.group(1) == 'START':
                    currTest = l.split('|')[1][1:-1]
                elif mm.group(1) == 'OK':
                    currTest = 'Unknown'
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
            live[addr] = (threadName, currTest + ' ' + addr)

    nameCounts = {}
    for addr, (name, test) in live.iteritems():
        # Ignore ImageBridgeChild: there are too many.
        if name == 'ImageBridgeChild':
            continue
        if printLeakAddrs:
            print name, addr, test
        nameCounts.setdefault(name, []).append(test)

    return nameCounts


def extractTestName(fileName):
    startLen = len('try_ubuntu64_vm-debug_test-')
    return fileName[startLen:].split('-bm')[0]


onlyMochitests = True

def analyzeAllFiles():
    for (base, _, files) in os.walk('.'):
        for fileName in files:
            testName = extractTestName(fileName)

            if onlyMochitests and not testName.startswith('mochitest'):
                continue

            if not base.endswith("/"):
                base += "/"
            fullFileName = base + fileName

            f = open(fullFileName, 'r')
            leakedThreadCounts = reportLeakedThread(f)
            f.close()

            if not leakedThreadCounts:
                continue

            for threadName, tests in leakedThreadCounts.iteritems():
                print threadName, '\t', tests, '\t', testName


if False:
    f = open('try_ubuntu64_vm-debug_test-mochitest-e10s-2-bm121-tests1-linux64-build657.txt', 'r')
    reportLeakedThread(f, printLeakAddrs = True)
    f.close()
else:
    analyzeAllFiles()
