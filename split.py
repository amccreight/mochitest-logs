#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# Echo all output starting with the line after the line that starts with splitStart.


import sys


splitStart = "QQQQQQQQQ"


foundLine = False

for l in sys.stdin:
    if foundLine:
        print l,
        continue

    if l.startswith(splitStart):
        foundLine = True


