#!/usr/bin/python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import re

endLen = len(": file /builds/worker/checkouts/gecko/dom/ipc/jsactor/JSActorManager.cpp:214") + 1
splitRe = re.compile("WARNING: rejected message: (.*)$")

# [task 2023-03-07T22:45:40.818Z] 22:45:40     INFO - PID 29233 | [Parent 29233, Main Thread] WARNING: useless message: MarionetteEvents : MarionetteEventsChild:PageLoadEvent: file /builds/worker/checkouts/gecko/dom/ipc/jsactor/JSActorManager.cpp:214

for l in sys.stdin:
    m = splitRe.search(l)
    if not m:
        continue
    print(m.group(1)[:-endLen])


