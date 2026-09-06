#!/usr/bin/env bash
# Wrapper: verify lab demo and heal what is broken.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/verify-demo.py" "$@"
