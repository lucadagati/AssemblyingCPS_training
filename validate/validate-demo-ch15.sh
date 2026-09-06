#!/usr/bin/env bash
# Module C — ch15 environmental publisher → metrics gateway → InfluxDB
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CH15="${SCRIPT_DIR}/repos/ch15"
LAB_PLUGIN="${SCRIPT_DIR}/ch15-lab/plugin_demo_lab.py"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

echo "=== Module C: ch15 environmental publisher ==="
echo "Host: ${HOST} · repo: github.com/AssemblingSmartCPS/ch15"

[[ -d "$CH15" ]] && ok "Repo ch15 present" || fail_msg "Repo ch15 missing"
[[ -f "$LAB_PLUGIN" ]] && ok "Lab plugin plugin_demo_lab.py present" || fail_msg "Lab plugin missing"

grep -q 'MetricsWriter' "$LAB_PLUGIN" 2>/dev/null \
  && ok "Lab plugin uses MetricsWriter SDK (metrics gateway)" \
  || warn_msg "Lab plugin may still use direct InfluxDB client"

docker ps --format '{{.Names}}' 2>/dev/null | grep -qx influxdb \
  && ok "InfluxDB container running" || fail_msg "InfluxDB not running"

docker ps --format '{{.Names}}' 2>/dev/null | grep -qx metrics-gateway \
  && ok "metrics-gateway container running" || warn_msg "metrics-gateway not running"

if curl -sf "http://${HOST}:8093/health" >/dev/null 2>&1; then
  ok "metrics-gateway /health OK"
else
  warn_msg "metrics-gateway /health unreachable"
fi

if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx influxdb; then
  docker exec influxdb influx -username admin -password admin -execute "SHOW DATABASES" 2>/dev/null | grep -q s4t_iot \
    && ok "Database s4t_iot exists" || warn_msg "Database s4t_iot missing — provision stream or start plugin with metrics"
  COUNT=$(docker exec influxdb influx -username admin -password admin -execute \
    'SELECT COUNT(*) FROM environmental_data' -database s4t_iot 2>/dev/null | grep -oE '[0-9]+' | tail -1 || echo "0")
  if [[ "${COUNT:-0}" -ge 1 ]]; then
    ok "environmental_data has ${COUNT} point(s) in InfluxDB (s4t_iot)"
  else
    warn_msg "No environmental_data yet — Start plugin with Enable cloud metrics"
  fi
fi

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
