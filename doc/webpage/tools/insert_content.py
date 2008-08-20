"""
insert_content template_file source_file

Replaces %{content} tag in template file with the contents from source files.
"""

import sys

template = open(sys.argv[1]).readlines()
content_blocks = []
for content_file in sys.argv[2:]:
    content_blocks.append(open(content_file).readlines())

out = []
for line in template:
    if not '%{content}' in line:
        out.append(line)
    else:
        out.extend(content_blocks[0])
        del content_blocks[0]

print ''.join(out)

