#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Analyze the ++/-- DOMWINDOW in a TBPL log.

import re
import sys

winPatt = re.compile('I/DocShellAndDOMWindowLeak (..)DOMWINDOW == (\d+).*\[pid = (\d+)\] \[serial = (\d+)\] \[[^\]]+\].?(\[url = [^\]]+)?')
urlLen = len('[url = ')


leakLogCreatePatt = re.compile('### XPCOM_MEM_BLOAT_LOG defined -- logging bloat/leaks to (.+)$')

leakLogReadPatt = re.compile('INFO \- leakcheck \| Processing leak log file (.+)$')

bloatViewPatt = re.compile('BloatView: ALL \(cumulative\) LEAK AND BLOAT STATISTICS\, ([a-zA-Z]+) process (\d+)')

failPatt = re.compile('TEST-UNEXPECTED-FAIL \| leakcheck large nsGlobalWindowInner \| (.+)$')

testPatt = re.compile('INFO \- TEST-(START|SKIP|OK) \| (\S+)')

windowCountPatt = re.compile('INFO \- TEST-INFO \| leakcheck \| [a-zA-Z]+ leaked ([0-9]+) (nsGlobalWindowInner|nsGlobalWindowOuter)')

def findLeakers():
    live = {}
    hiddenLive = {}
    foundAny = False
    lastLeakLog = None
    currTest = None
    inSkip = False
    currBloatPid = 0
    pidLeaks = {}
    testsForLogs = {}
    leakingLogs = {}

    sys.stdin.reconfigure(encoding='latin1')

    for l in sys.stdin:
        tp = testPatt.search(l)
        if tp:
            state = tp.group(1)
            t = tp.group(2)
            if state == "START":
                if t == "Shutdown":
                    continue
                assert (currTest is None) or inSkip
                currTest = t
                inSkip = False
            elif state == "SKIP":
                assert currTest == t
                inSkip = True
            elif state == "OK":
                assert currTest == t
                currTest = None
                inSkip = False
            continue

        m = winPatt.search(l)
        if m:
            isNew = m.group(1) == '++'
            assert isNew or m.group(1) == '--'

            # XXX m.group(1) is the window pointer.
            # Could use that to disambiguate.
            numLive = int(m.group(2))
            pid = int(m.group(3))
            serial = int(m.group(4))
            url = m.group(5)
            if url:
                url = url[urlLen:]

            winId = (pid, serial)

            if isNew:
                assert url is None

                if winId in live:
                    assert not winId in hiddenLive
                    hiddenLive[winId] = live[winId]
                live[winId] = currTest
                foundAny = True
            else:
                assert winId in live
                del live[winId]
            continue

        f = failPatt.search(l)
        if f:
            leakLog = f.group(1)
            assert not leakLog in leakingLogs
            leakingLogs[lastLeakLog] = f.group(1)
            continue

        llc = leakLogCreatePatt.search(l)
        if llc:
            leakLog = llc.group(1)
            t = currTest if currTest else "NONE"
            testsForLogs.setdefault(leakLog, []).append(t)
            continue

        llr = leakLogReadPatt.search(l)
        if llr:
            lastLeakLog = llr.group(1)
            continue

        bv = bloatViewPatt.search(l)
        if bv:
            # bv.group(1) is the log file.
            currBloatPid = int(bv.group(2))

            # XXX Hopefully if a PID is reused, both won't leak.
            assert not currBloatPid in pidLeaks
            pidLeaks[currBloatPid] = {}

            continue

        wc = windowCountPatt.search(l)
        if wc:
            count = int(wc.group(1))
            which = wc.group(2)
            m = pidLeaks[currBloatPid]
            assert not which in m
            m[which] = count
            continue


    if not foundAny:
        print("Didn't find any windows in the log.")

    pidToWindows = {}
    for x, currTest in hiddenLive.items():
        pid = x[0]
        pidToWindows.setdefault(pid, []).append([x[0], x[1], currTest])
    for x, currTest in live.items():
        pid = x[0]
        pidToWindows.setdefault(pid, []).append([x[0], x[1], currTest])

    for pid, m in pidLeaks.items():
        print(f'pid:{pid}')
        print('  leaked: ', end='')
        x = []
        for which, count in m.items():
            x.append(f'{count} {which}')
        print(', '.join(x))
        for [x, y, z] in pidToWindows.get(pid, []):
            print(f'  [pid = {x}] [serial = {y}] during {z}')
    print()

    for log, reported in leakingLogs.items():
        print(f'log: {log}')
        print(f'  reported test directory: {reported}')
        print(f'  actual test: {", ".join(testsForLogs.get(log, ["NONE"]))}')
    print()

    dupeCount = 0
    nonDupeCount = 0
    for log, tests in testsForLogs.items():
        nonDupeCount += 1
        if len(tests) <= 1:
            continue
        dupeCount += len(tests) - 1
        if False:
            tstring = "\n  ".join(tests)
            print(f'Duplicate logs {log}:\n  {tstring}')
    print(f'Number of non-overridden logs: {nonDupeCount}')
    print(f'Number of overridden logs: {dupeCount}')
    print()


findLeakers()
