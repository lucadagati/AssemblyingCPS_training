#!/usr/bin/env bash
# Module B — ch14 plugin demos (HelloName, Docker, async weather_station)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CH14="${SCRIPT_DIR}/repos/ch14"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

echo "=== Module B: ch14 plugin demos ==="
echo "Host: ${HOST} · repo: github.com/AssemblingSmartCPS/ch14"

[[ -d "$CH14" ]] && ok "Repo ch14 present" || fail_msg "Repo ch14 missing"

HELLO_FIXED="${SCRIPT_DIR}/ch14-fixed/plugins/synchronous/hello_name_plugin.py"
HELLO_UP="${CH14}/plugins/synchronous/hello_name_plugin.py"
[[ -f "$HELLO_FIXED" ]] && grep -q "class Worker" "$HELLO_FIXED" \
  && ok "HelloName fixed plugin (class Worker)" || fail_msg "HelloName fixed plugin missing/invalid"

if [[ -f "$HELLO_UP" ]]; then
  if grep -q "class HelloNamePlugin" "$HELLO_UP"; then
    warn_msg "Upstream ch14 hello_name_plugin.py still uses HelloNamePlugin — use ch14-fixed/"
  else
    ok "Upstream hello_name_plugin.py uses Worker"
  fi
fi

DOCKER="${CH14}/plugins/synchronous/docker_lifecycle_plugin.py"
[[ -f "$DOCKER" ]] && python3 -m py_compile "$DOCKER" 2>/dev/null \
  && ok "docker_lifecycle_plugin.py syntax" || warn_msg "docker_lifecycle_plugin.py check skipped"

WEATHER_ASYNC="${CH14}/plugins/asynchronous/weather_station_plugin.py"
[[ -f "$WEATHER_ASYNC" ]] && ok "weather_station_plugin.py (async) present" \
  || warn_msg "weather_station_plugin.py missing"

WEATHER_DEMO="${CH14}/demos/weather_web_server.py"
[[ -f "$WEATHER_DEMO" ]] && python3 -m py_compile "$WEATHER_DEMO" 2>/dev/null \
  && ok "weather_web_server.py syntax (Module F book demo)" \
  || fail_msg "weather_web_server.py missing or invalid"

# Optional: weather server running inside LR (lab port 8088 — book uses 8080)
WEATHER_PORT="${S4T_WEATHER_PORT:-8088}"
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx lightning-rod; then
  CODE=$(docker exec lightning-rod sh -c "curl -s -o /dev/null -w '%{http_code}' --connect-timeout 2 http://127.0.0.1:${WEATHER_PORT}/sensors 2>/dev/null" || echo "000")
  if [[ "$CODE" == "200" ]]; then
    ok "weather_web_server responding inside LR :${WEATHER_PORT}/sensors"
  else
    warn_msg "weather_web_server not running — run experiments/webservices/run-weather-demo.sh"
  fi
fi

WEATHER_STATE="${SCRIPT_DIR}/experiments/webservices/weather-state.json"
if [[ -f "$WEATHER_STATE" ]]; then
  python3 -c "import json; s=json.load(open('$WEATHER_STATE')); exit(0 if s.get('verified') else 1)" 2>/dev/null \
    && ok "weather WSTUN tunnel verified (cloud :$(python3 -c "import json; print(json.load(open('$WEATHER_STATE'))['cloud_port'])"))" \
    || warn_msg "weather-state.json present but tunnel not verified"
fi

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
