#!/usr/bin/env bash
# Federated Learning lab — Flower server + live S4T dashboard (Ch.19)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CH19="${ROOT}/repos/ch19"
FL_EXP="${ROOT}/experiments/federated-learning"
cd "$CH19"

export FL_ROUNDS="${FL_ROUNDS:-2}"
export FL_PORT="${FL_PORT:-8087}"
export FL_HOST="${FL_HOST:-0.0.0.0}"
export FL_DASHBOARD="${FL_DASHBOARD:-1}"
export FL_DASHBOARD_PORT="${FL_DASHBOARD_PORT:-8090}"
export FL_DASHBOARD_HOST="${FL_DASHBOARD_HOST:-0.0.0.0}"
export PYTHONPATH="${FL_EXP}:${PYTHONPATH:-}"

PY="${ROOT}/.venv/bin/python3"
[[ -x "$PY" ]] || PY=python3

if ! "$PY" -c "import flwr, flask" 2>/dev/null; then
  echo "Installing Flower + dashboard deps..."
  "$PY" -m pip install -q flwr torch pandas scikit-learn flask
fi

DASH_PID=""
cleanup() {
  [[ -n "$DASH_PID" ]] && kill "$DASH_PID" 2>/dev/null || true
}
trap cleanup EXIT

if [[ "$FL_DASHBOARD" != "0" ]]; then
  echo "Starting FL dashboard on :${FL_DASHBOARD_PORT} ..."
  FL_ROUNDS="$FL_ROUNDS" FL_DASHBOARD_PORT="$FL_DASHBOARD_PORT" FL_DASHBOARD_HOST="$FL_DASHBOARD_HOST" \
    "$PY" "${FL_EXP}/dashboard/app.py" &
  DASH_PID=$!
  sleep 1
  echo "  → http://127.0.0.1:${FL_DASHBOARD_PORT}/"
  echo "  → http://<VM_IP>/horizon/fl/  (after setup-fl-horizon.sh)"
fi

echo "Flower server on ${FL_HOST}:${FL_PORT} — ${FL_ROUNDS} round(s), waiting for 3 edge clients"
exec env FL_ROUNDS="$FL_ROUNDS" FL_PORT="$FL_PORT" FL_HOST="$FL_HOST" FL_DASHBOARD="$FL_DASHBOARD" \
  PYTHONPATH="$PYTHONPATH" "$PY" server.py
