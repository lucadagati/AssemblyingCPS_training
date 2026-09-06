#!/bin/bash
# Fix Python3 bug in iotronic conductor: "except exception:" catches the module.
set -euo pipefail
TARGET="${1:-/usr/local/lib/python3.6/dist-packages/iotronic/conductor/endpoints.py}"
python3 - <<PY
from pathlib import Path
p = Path("$TARGET")
text = p.read_text()
text2 = text.replace('except exception:\n                return exception',
                     'except Exception:\n                pass')
text2 = text2.replace('except exception:\n            return exception',
                      'except Exception:\n            pass')
text2 = text2.replace('except exception:', 'except Exception:')
p.write_text(text2)
print("patched", p)
PY
