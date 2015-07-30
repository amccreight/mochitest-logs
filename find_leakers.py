#!/usr/bin/python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This script finds objects that are leaking, and objects that are anti-leaking.

import sys
import re


print "This is a very early prototype version that isn't well tested."

ctorDtorPatt = re.compile('^\<(.+)\> (0x[0-9a-f]+ \d+) (Ctor|Dtor) \(\d+\)\n$')
createDestroyPatt = re.compile('^\<(.+)\> (0x[0-9a-f]+ \d+) (Create|Destroy)\n')

#<WJSWJS> 0x11470a800 1 Ctor (120)
#<nsXPCWrappedJS> 0x110ddb800 4 Create
#<nsXPCWrappedJS> 0x110fb4800 16 Destroy
#<WJSWJS> 0x1147a7d80 35 Dtor (120)


# XXX This may not work if the class name is somehow needed to distinguish things.

alives = set([])

for l in sys.stdin:
    m = createDestroyPatt.match(l)
    if m:
        className = m.group(1)
        ident = m.group(2)
        isCtor = m.group(3) == 'Ctor'
        continue
    m = ctorDtorPatt.match(l)
    if m:
        className = m.group(1)
        ident = m.group(2)
        if m.group(3) == 'Ctor':
            if ident in alives:
                print 'Error: double Ctor of object', ident, 'with class', className
            else:
                alives.add(ident)
        else:
            if ident in alives:
                alives.remove(ident)
            else:
                print 'Error: Dtor of unseen object', ident, 'with class', className
        continue
    if l == '\n':
        continue
    if l.startswith('    #'):
        continue
    print 'Unknown line:', l[:-1]
    exit(-1)

print alives



