#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Extract LSAN results from a Mochitest log.

import sys
import re


prefixPatt1 = re.compile('^\d\d:\d\d:\d\d\s+INFO -  (.*)$')
prefixPatt2 = re.compile('^\d\d:\d\d:\d\d\s+INFO -\s+\d+ INFO (.*)$')
prefixPatt3 = re.compile('^[ 0-9]\d:\d\d\.\d\d (.*)')
prefixPatt4 = re.compile('^[ 0-9]\d:\d\d:\d\d     INFO -  (.*)')

# prefixPatt1 works with the structured log format, circa Fx33.  The other patterns may be needed for older log output.
prefixPatt = prefixPatt1


lsanPatt = re.compile('^(?:SUMMARY: AddressSanitizer|LeakSanitizer|Indirect leak of|Direct leak of|$|    #\d|#\d)')
# the last case is for crash test logs, which don't have leading spaces for some reason.

stackHeaderPatt = re.compile('^(Indirect|Direct) leak of (\d+) byte\(s\) in (\d+) object\(s\) allocated from:$')


def load_log(fname):

    try:
        f = open(fname, 'r')
    except:
        sys.stderr.write('Error opening file ' + fname + '\n')
        exit(-1)

    traces = []

    for l in f:
        lm = prefixPatt.match(l)
        if lm:
            l2 = lm.group(1)
        else:
            l2 = l[:-1]

        lsm = lsanPatt.match(l2)
        if not lsm:
            continue

        # Remove some build cruft.
        l2 = l2.replace('/builds/slave/try-l64-asan-00000000000000000/build/', '')
        l2 = l2.replace('/builds/slave/try-l64-asan-00000000000000000', '')
        l2 = l2.replace('/tools/gcc-4.7.3-0moz1/lib/gcc/x86_64-unknown-linux-gnu/4.7.3/../../../../include', '')
        if len(l2) == 0:
            continue

        if l2[0] == 'I' or l2[0] == 'D':
            hm = stackHeaderPatt.match(l2)
            if not hm:
                print 'Bad stack trace header:', l
                exit(0)
            isDirect = (hm.group(1) == 'Direct')
            leakBytes = int(hm.group(2))
            numLeaked = int(hm.group(3))
            traces.append((isDirect, leakBytes, numLeaked, []))
            continue

        if len(traces) == 0:
            # We're probably iterating over a SIGSEV or something, so just ignore it.
            continue

        traces[-1][3].append(l2)

    f.close()

    return traces


def print_trace_header(h):
    (isDirect, leakBytes, numLeaked, _) = h
    print ('%s leak of %d byte(s) in %d object(s).' % ('Direct' if isDirect else 'Indirect', leakBytes, numLeaked))

def print_traces(traces):
    sort_traces(traces)
    for t in traces:
        print_trace_header(t)
        for f in t[3]:
            print f
        print

def sort_traces(traces):
    traces.sort(reverse=True, key=lambda t: (t[0], t[1]))

if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.stderr.write('Not enough arguments. Pass in the name of the input file.\n')
        exit()

    print_traces(load_log(sys.argv[1]))




