#!/usr/bin/env python
"""
Return everything inside <body></body>.

"""

import sys
data = sys.stdin.readlines()

out = []

inside = False
for line in data:
    if '<body>' in line:
        inside = True
        continue
    elif '</body>' in line:
        inside = False

    if inside:
        out.append(line)

print ''.join(out)
