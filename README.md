# MDEX
Markdown Expansion Compiler

# Requirements
- Latest Python3 over Python 3.6

# Usage:
`mdex [filename]`
	
# Support Symbol
## @@ file_name
Dual atmark extends source code.
### Before
```markdown:
Threre is code.
@@ mdex.py
↑That's my code.
```
### After
```markdown:
There is code.
｀｀｀python:
#!/usr/bin/env python3
import sys
import mimetypes
︙
︙
｀｀｀
↑That's my code.
```
