#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import re

endLen = len("[task 2023-11-02T16:59:39.586Z] 16:59:39     INFO - ")
splitRe = re.compile("WARNING: rejected message: (.*)$")

for l in sys.stdin:
    print(l[endLen:-1])
    continue

    m = splitRe.search(l)
    if not m:
        continue
    print(m.group(1)[:-endLen])


