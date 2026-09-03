#!/usr/bin/env bash
# Install FL Python deps + predictive-maintenance datasets inside LR containers.
# Installs one board at a time to avoid OOM on small VMs.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CH19="${ROOT}/repos/ch19"
PIP_OPTS="--no-cache-dir -q"
GEN="${ROOT}/experiments/federated-learning/generate_pm_datasets.py"

if [[ ! -f "${CH19}/machine_1.csv" ]]; then
  echo "Generating machine_*.csv datasets..."
  python3 "$GEN" --out "$CH19" 2>/dev/null || "${ROOT}/.venv/bin/python" "$GEN" --out "$CH19"
fi

install_board() {
  local c="$1"
  if ! docker ps --format '{{.Names}}' | grep -qx "$c"; then
    echo "SKIP $c — not running"
    return 0
  fi
  echo "=== $c ==="
  docker exec "$c" mkdir -p /opt/fl
  for f in machine_1.csv machine_2.csv machine_3.csv; do
    docker cp "${CH19}/${f}" "$c:/opt/fl/${f}"
  done
  docker cp "${ROOT}/experiments/federated-learning/fl_client_plugin.py" "$c:/opt/fl/fl_client_plugin.py"

  if docker exec "$c" python3 -c "import flwr, torch, pandas, sklearn" 2>/dev/null; then
    echo "OK $c — deps already present"
  else
    echo "Installing Python deps in $c (isolated, no system upgrades)..."
    docker exec "$c" pip install ${PIP_OPTS} --upgrade-strategy only-if-needed pandas scikit-learn flwr
    docker exec "$c" pip install ${PIP_OPTS} --upgrade-strategy only-if-needed torch \
      --index-url https://download.pytorch.org/whl/cpu \
      || docker exec "$c" pip3 install ${PIP_OPTS} --upgrade-strategy only-if-needed torch \
      --index-url https://download.pytorch.org/whl/cpu
  fi
  docker exec "$c" python3 -c "import flwr, torch; print('flwr', flwr.__version__, 'torch', torch.__version__)"
  echo "OK $c — /opt/fl/machine_*.csv + fl_client_plugin.py"
}

for c in lightning-rod lightning-rod-2 lightning-rod-3; do
  install_board "$c"
  sleep 3
done

GW=$(docker network inspect ch13_s4t -f '{{range .IPAM.Config}}{{.Gateway}}{{end}}' 2>/dev/null || echo "172.18.0.1")
echo ""
echo "Predictive maintenance FL — plugin params per board:"
echo "  board-alpha (CNC spindle):     csv_file=/opt/fl/machine_1.csv  server_address=${GW}:8087  dashboard_url=http://${GW}:8090"
echo "  board-beta  (conveyor motor):  csv_file=/opt/fl/machine_2.csv  server_address=${GW}:8087  dashboard_url=http://${GW}:8090"
echo "  board-gamma (pump line):       csv_file=/opt/fl/machine_3.csv  server_address=${GW}:8087  dashboard_url=http://${GW}:8090"
echo ""
echo "FL live dashboard: http://<VM_IP>/horizon/fl-live/"
