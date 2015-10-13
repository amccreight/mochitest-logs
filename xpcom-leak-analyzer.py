#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import os
import re

bloatStartPatt = re.compile('^..:..:..     INFO -       \|<----------------Class--------------->\|<-----Bytes------>\|<----Objects---->\|$')
bloatMidPatt = re.compile('^..:..:..\s+INFO -[^|]+\|([^|]+)\|([^|]+)\|([^|]+)\|$')
bloatEndPatt = re.compile('^..:..:..     INFO -  nsTraceRefcnt::DumpStatistics: \d+ entries$')


def checkNumLeaked(numLeaked):
    if not 'PImageBridgeChild' in numLeaked:
        assert not 'base::Thread' in numLeaked
        return

    assert numLeaked['PImageBridgeChild'] == 1
    assert numLeaked['base::Thread'] == 1


def checkBloatReports(f):
    inBloat = False
    numLeaked = None

    for l in f:
        bspm = bloatStartPatt.match(l)
        if bspm:
            assert not inBloat
            inBloat = True
            numLeaked = {}
            continue
        bepm = bloatEndPatt.match(l)
        if bepm:
            assert inBloat
            inBloat = False
            checkNumLeaked(numLeaked)
            numLeaked = None
            continue

        if not inBloat:
            continue

        bmpm = bloatMidPatt.match(l)
        assert bmpm
        leakedClass = bmpm.group(1).strip()
        if leakedClass == '' or leakedClass == 'TOTAL':
            continue
        nl = int(bmpm.group(3).split()[1])

        if leakedClass == 'base::Thread' or leakedClass == 'PImageBridgeChild':
            assert not leakedClass in numLeaked
            numLeaked[leakedClass] = nl


def extractTestName(fileName):
    startLen = len('try_ubuntu64_vm-debug_test-')
    return fileName[startLen:].split('-bm')[0]


def analyzeAllFiles():
    for (base, _, files) in os.walk('.'):
        for fileName in files:
            testName = extractTestName(fileName)

            if not testName.startswith('mochitest'):
                continue

            if not base.endswith("/"):
                base += "/"
            fullFileName = base + fileName

            f = open(fullFileName, 'r')
            print 'checking', testName
            checkBloatReports(f)
            f.close()


analyzeAllFiles()
