#!/usr/bin/env bash
# Validazione demo laboratorio S4T (Cap. 13-15)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CH13_DIR="${CH13_DIR:-${SCRIPT_DIR}/repos/ch13}"
PATCH_FILE="${SCRIPT_DIR}/patches/docker-compose.lab.yml"
HOST_IP="${1:-$(hostname -I | awk '{print $1}')}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass=0
fail=0
warn=0

ok()   { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass + 1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail + 1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn + 1)); }

echo "=============================================="
echo " Validazione laboratorio S4T"
echo " Host: ${HOST_IP} | CH13: ${CH13_DIR}"
echo "=============================================="

echo ""
echo "=== SLOT 1: Stack4Things (Cap. 13) ==="

if [[ -d "${CH13_DIR}" ]]; then ok "Repo ch13 presente"; else fail_msg "Directory ch13 non trovata"; fi
command -v docker >/dev/null 2>&1 && ok "Docker: $(docker --version | head -1)" || fail_msg "Docker non installato"
docker compose version >/dev/null 2>&1 && ok "Docker Compose v2" || fail_msg "Docker Compose assente"

if [[ -d "${CH13_DIR}" ]]; then
  cd "${CH13_DIR}" || exit 1
  COMPOSE_ARGS=(-f docker-compose.yml)
  [[ -f "${PATCH_FILE}" ]] && COMPOSE_ARGS+=(-f "${PATCH_FILE}")

  RUNNING=$(docker compose "${COMPOSE_ARGS[@]}" ps --status running -q 2>/dev/null | wc -l)
  if [[ "${RUNNING}" -ge 8 ]]; then ok "Container running: ${RUNNING}"; else warn_msg "Container running: ${RUNNING} (atteso >= 8)"; fi

  HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://${HOST_IP}:8812/" 2>/dev/null || echo "000")
  [[ "${HTTP_CODE}" != "000" ]] && ok "Conductor :8812 (HTTP ${HTTP_CODE})" || warn_msg "Conductor :8812 non raggiungibile"

  UI_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://${HOST_IP}/" 2>/dev/null || echo "000")
  [[ "${UI_CODE}" =~ ^(200|301|302|401|403)$ ]] && ok "Horizon UI :80 (HTTP ${UI_CODE})" || warn_msg "Horizon UI :80 (HTTP ${UI_CODE})"

  LR_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://${HOST_IP}:1474/" 2>/dev/null || echo "000")
  [[ "${LR_CODE}" =~ ^(200|301|302|401|403)$ ]] && ok "Lightning-Rod UI :1474 (HTTP ${LR_CODE})" || warn_msg "LR UI :1474 (HTTP ${LR_CODE})"
fi

echo ""
echo "=== SLOT 2: Plugin (Cap. 14) ==="

HELLO="${SCRIPT_DIR}/ch14-fixed/plugins/synchronous/hello_name_plugin.py"
if [[ -f "${HELLO}" ]]; then
  grep -q "class Worker" "${HELLO}" && ok "hello plugin: class Worker" || fail_msg "hello plugin: manca Worker"
  python3 -m py_compile "${HELLO}" 2>/dev/null && ok "hello plugin: sintassi OK" || fail_msg "hello plugin: sintassi KO"
else
  fail_msg "hello plugin non trovato"
fi

if [[ -S /var/run/docker.sock ]]; then
  ok "Docker socket host presente"
  if docker ps --format '{{.Names}}' 2>/dev/null | grep -q lightning-rod; then
    docker exec lightning-rod test -S /var/run/docker.sock 2>/dev/null \
      && ok "Docker socket montato in lightning-rod" \
      || warn_msg "Docker socket non montato in lightning-rod"
  fi
fi

if python3 -c "import docker; docker.from_env().ping()" 2>/dev/null; then
  ok "Docker SDK: ping OK"
  RUN_OUT=$(python3 <<'PY'
import docker, time
client = docker.from_env()
try:
    c = client.containers.get("lab_test_alpine")
    c.remove(force=True)
except docker.errors.NotFound:
    pass
container = client.containers.run(
    "alpine", name="lab_test_alpine",
    command="echo Hello from plugin!", detach=True
)
time.sleep(2)
logs = container.logs(tail=5).decode()
container.remove(force=True)
print("OK" if "Hello from plugin" in logs else "FAIL")
PY
  )
  [[ "${RUN_OUT}" == "OK" ]] && ok "Docker plugin logic verificata" || fail_msg "Docker plugin logic fallita"
else
  warn_msg "Docker SDK non disponibile (pip install docker)"
fi

echo ""
echo "=== SLOT 3: Environmental publisher (Cap. 15) ==="

PLUGIN_DEMO="${SCRIPT_DIR}/repos/ch15/plugin_demo"
if [[ -f "${PLUGIN_DEMO}" ]]; then
  python3 -m py_compile "${PLUGIN_DEMO}" 2>/dev/null && ok "plugin_demo: sintassi OK" || fail_msg "plugin_demo: sintassi KO"
  grep -q "class Worker" "${PLUGIN_DEMO}" && ok "plugin_demo: class Worker" || fail_msg "plugin_demo: manca Worker"
else
  fail_msg "plugin_demo non trovato"
fi

if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx influxdb; then
  ok "InfluxDB container attivo"
  docker exec influxdb influx -username admin -password admin -execute "CREATE DATABASE secco" 2>/dev/null || true
  docker exec influxdb influx -username admin -password admin -execute "SHOW DATABASES" 2>/dev/null | grep -q secco \
    && ok "Database secco presente" || warn_msg "Database secco assente"
  STANDALONE=$(PYTHONPATH="${SCRIPT_DIR}/tests" python3 -c "
from test_env_plugin import run_single_point_test
run_single_point_test()
print('OK')
" 2>&1) || STANDALONE="FAIL:${STANDALONE}"
  [[ "${STANDALONE}" == *OK* ]] && ok "Scrittura punto InfluxDB verificata" || warn_msg "Test Influx: ${STANDALONE}"
else
  warn_msg "InfluxDB non attivo"
fi

echo ""
echo "=============================================="
echo " Risultato: ${pass} OK | ${warn} WARN | ${fail} FAIL"
echo "=============================================="
exit $(( fail > 0 ? 1 : 0 ))
