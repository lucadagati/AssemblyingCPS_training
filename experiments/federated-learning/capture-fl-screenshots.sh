#!/usr/bin/env bash
# Capture Module G Horizon FL panel screenshots for slide decks.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

export S4T_LAB_HOST="${S4T_LAB_HOST:-$(cat vm-ip.txt 2>/dev/null || hostname -I | awk '{print $1}')}"
export FL_CAPTURE_ONLY=1

echo "=== FL panel screenshots (host ${S4T_LAB_HOST}) ==="
.venv/bin/python scripts/capture_dashboards.py
echo "Assets: training/assets/chapter19/"
