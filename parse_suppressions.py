#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Crude parser for an LSAN suppression file.


import sys


def load_suppressions(fname):
    try:
        f = open(fname, 'r')
    except:
        sys.stderr.write('Error opening file ' + fname + '\n')
        exit(-1)

    supps = []

    for l in f:
        if len(l) == 1:
            # blank line
            continue
        if l[0] == '#':
            # comment
            continue

        if not l.startswith('leak:'):
            print 'Expected line to start with "#" or "leak:":', l[:-1]
            exit(-1)
        supps.append(l[5:-1])

    f.close()

    return supps


def print_suppressions(supps):
    for s in supps:
        print s


if __name__ == "__main__":

    if len(sys.argv) < 2:
        sys.stderr.write('Not enough arguments.\n')
        exit()

    print_suppressions(load_suppressions(sys.argv[1]))
