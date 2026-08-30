#!/usr/bin/env bash
# Federated Learning lab — start Flower server (Ch.19) on VM host
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CH19="${ROOT}/repos/ch19"
cd "$CH19"

ROUNDS="${FL_ROUNDS:-2}"
PORT="${FL_PORT:-8087}"

if ! python3 -c "import flwr" 2>/dev/null; then
  echo "Installing Flower + deps for demo..."
  pip install -q flwr torch pandas scikit-learn
fi

echo "Starting FL server on 0.0.0.0:${PORT} (rounds=${ROUNDS})"
echo "Run client plugins on 3 Active boards after server is up"
exec python3 server.py
