#!/usr/bin/env python
"""
Strip class="something" from tags.
"""

import sys
import re
data = sys.stdin.readlines()

class_re = re.compile('class=".*"')

out = []
for line in data:
    out.append(class_re.sub('', line))

print ''.join(out)
