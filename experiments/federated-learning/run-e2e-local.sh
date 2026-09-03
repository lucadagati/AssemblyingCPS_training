#!/usr/bin/env bash
# Local FL smoke test — 3 clients on VM host (same logic as board plugins).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CH19="${ROOT}/repos/ch19"
PY="${ROOT}/.venv/bin/python3"
[[ -x "$PY" ]] || PY=python3

export FL_ROUNDS="${FL_ROUNDS:-2}"
export FL_PORT="${FL_PORT:-8087}"
export FL_HOST="127.0.0.1"
export FL_SERVER="127.0.0.1:${FL_PORT}"

cd "$CH19"
"$PY" -m pip install -q flwr torch pandas scikit-learn 2>/dev/null || true

# Free port if leftover
fuser -k "${FL_PORT}/tcp" 2>/dev/null || true

echo "Starting server..."
env FL_ROUNDS="$FL_ROUNDS" FL_PORT="$FL_PORT" FL_HOST="0.0.0.0" "$PY" server.py &
SRV=$!
sleep 3

cleanup() { kill "$SRV" 2>/dev/null || true; wait "$SRV" 2>/dev/null || true; }
trap cleanup EXIT

echo "Starting 3 clients..."
FL_SERVER="$FL_SERVER" "$PY" client.py 0 &
FL_SERVER="$FL_SERVER" "$PY" client.py 1 &
FL_SERVER="$FL_SERVER" "$PY" client.py 2 &
wait

echo "E2E FL smoke test finished."
