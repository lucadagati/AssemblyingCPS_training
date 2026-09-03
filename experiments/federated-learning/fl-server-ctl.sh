#!/usr/bin/env bash
# Wrapper kept for CLI; Horizon uses control_server.py HTTP API.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PY="${ROOT}/.venv/bin/python3"
[[ -x "$PY" ]] || PY=python3
exec "$PY" "$(dirname "$0")/fl_server_manager.py" "${1:-status}"
