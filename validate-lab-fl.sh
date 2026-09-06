#!/usr/bin/env bash
# Module G — Federated Learning (Cap. 19): artifacts, Horizon panel mounts, optional E2E.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CH19="${SCRIPT_DIR}/repos/ch19"
FL_EXP="${SCRIPT_DIR}/experiments/federated-learning"
PATCHES="${SCRIPT_DIR}/patches"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

PY="${SCRIPT_DIR}/.venv/bin/python3"
[[ -x "$PY" ]] || PY=python3

echo "=== Module G: Federated Learning (host ${HOST}) ==="

[[ -d "$CH19" ]] && ok "Repo ch19 present" || fail_msg "Repo ch19 missing"
[[ -f "$CH19/server.py" ]] && ok "server.py present" || fail_msg "server.py missing"
[[ -f "$CH19/client.py" ]] && ok "client.py present" || fail_msg "client.py missing"
[[ -f "${FL_EXP}/fl_client_plugin.py" ]] && ok "fl_client_plugin.py (LR plugin)" || fail_msg "fl_client_plugin.py missing"

for f in machine_1.csv machine_2.csv machine_3.csv heart_1.csv heart_2.csv heart_3.csv data_test_heart.csv data_test_pm.csv; do
  [[ -f "$CH19/$f" ]] && ok "Dataset $f" || warn_msg "Missing $f — run generate_pm_datasets.py"
done

"$PY" -m py_compile "$CH19/server.py" 2>/dev/null && ok "server.py syntax" || warn_msg "server.py syntax"
"$PY" -m py_compile "$CH19/client.py" 2>/dev/null && ok "client.py syntax" || warn_msg "client.py syntax"
"$PY" -m py_compile "${FL_EXP}/fl_client_plugin.py" 2>/dev/null && ok "plugin syntax" || warn_msg "plugin syntax"

for script in start-server.sh install-fl-on-boards.sh setup-fl-demo-plugins.sh setup-fl-horizon.sh fl-server-ctl.sh; do
  [[ -x "${FL_EXP}/${script}" ]] && ok "${script} present" || warn_msg "${script} missing or not executable"
done

# Horizon panel patch artifacts (host)
for f in \
  iotronic_ui_lab/iotronic_ui_lab/iot/federated_learning/views.py \
  horizon-enabled/_6060_iot_federated_learning_panel.py \
  apache-fl-live-proxy.conf \
  iotronic-ui-lab-entrypoint.sh; do
  [[ -f "${PATCHES}/${f}" ]] && ok "Patch ${f}" || fail_msg "Missing patch ${f}"
done

grep -q 'fl-control:' "${PATCHES}/docker-compose.lab.yml" 2>/dev/null \
  && ok "docker-compose.lab.yml defines fl-control" \
  || fail_msg "docker-compose.lab.yml missing fl-control service"

for lr in lightning-rod lightning-rod-2 lightning-rod-3; do
  if docker ps --format '{{.Names}}' | grep -qx "$lr" 2>/dev/null; then
    if docker exec "$lr" test -f /opt/fl/heart_1.csv 2>/dev/null; then
      ok "/opt/fl datasets on $lr"
    else
      warn_msg "/opt/fl missing on $lr — remount compose + run install-fl-on-boards.sh"
    fi
    if docker exec "$lr" python3 -c "import flwr" 2>/dev/null; then
      ok "flwr on $lr"
    else
      warn_msg "flwr missing on $lr — run install-fl-on-boards.sh"
    fi
  fi
done

code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 3 "http://127.0.0.1:8812/" 2>/dev/null || echo "000")
[[ "$code" == "200" ]] && ok "Conductor :8812 (boards API)" || warn_msg "Conductor :8812 HTTP $code — run scripts/fix-iotronic-wampagents.sh"

if docker ps --format '{{.Names}}' | grep -qx fl-control 2>/dev/null; then
  ok "fl-control container running"
else
  warn_msg "fl-control not running — run setup-fl-horizon.sh"
fi

code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 3 http://127.0.0.1:8091/health 2>/dev/null || echo "000")
[[ "$code" == "200" ]] && ok "FL control API :8091" || warn_msg "FL control :8091 HTTP $code — docker compose up fl-control"

if docker ps --format '{{.Names}}' | grep -qx iotronic-ui 2>/dev/null; then
  ok "iotronic-ui container running"
  for path in \
    /usr/share/openstack-dashboard/openstack_dashboard/enabled/_6060_iot_federated_learning_panel.py \
    /usr/local/lib/python2.7/dist-packages/iotronic_ui_lab/iot/federated_learning/views.py \
    /opt/fl_lab/fl_client_plugin.py \
    /etc/apache2/conf-available/fl-live-proxy.conf; do
    if docker exec iotronic-ui test -f "$path" 2>/dev/null; then
      ok "Mounted in iotronic-ui: ${path##*/}"
    else
      warn_msg "Missing in iotronic-ui: $path"
    fi
  done
else
  warn_msg "iotronic-ui not running — Horizon panel mounts not checked"
fi

# Horizon routes (login redirect or OK both acceptable for panel URL)
panel_code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 \
  "http://${HOST}/horizon/iot/federated_learning/" 2>/dev/null || echo "000")
case "$panel_code" in
  200|302|301) ok "Horizon FL panel URL HTTP $panel_code" ;;
  *) warn_msg "Horizon FL panel HTTP $panel_code — check iotronic-ui / Apache" ;;
esac

live_code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 \
  "http://${HOST}/horizon/fl-live/" 2>/dev/null || echo "000")
case "$live_code" in
  200) ok "Live topology proxy /horizon/fl-live/ HTTP 200" ;;
  502|503) warn_msg "Live topology proxy HTTP $live_code — start Flower server for dashboard" ;;
  404) warn_msg "Live topology proxy HTTP 404 — check apache-fl-live-proxy.conf" ;;
  *) warn_msg "Live topology proxy HTTP $live_code" ;;
esac

if [[ "${FL_SKIP_E2E:-0}" != "1" ]] && "$PY" -c "import flwr" 2>/dev/null; then
  echo "--- Local E2E (3 clients on VM, server :8087) ---"
  if FL_ROUNDS=1 "${FL_EXP}/run-e2e-local.sh" >/tmp/fl-e2e.log 2>&1; then
    ok "E2E FedAvg round (host simulation)"
  else
    warn_msg "E2E failed — see /tmp/fl-e2e.log"
  fi
else
  warn_msg "E2E skipped (install flwr or set FL_SKIP_E2E=1)"
fi

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
