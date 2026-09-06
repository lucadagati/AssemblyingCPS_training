#!/usr/bin/env bash
# Orchestrator — run all module validators (A–I) before a training session
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"
VALIDATE="${SCRIPT_DIR}/validate"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

run() {
  local name="$1" script="$2"
  echo ""
  echo "########################################"
  echo "# ${name}"
  echo "########################################"
  if bash "$script" "$HOST"; then
    echo -e "${GREEN}PASS${NC} ${name}"
    return 0
  else
    echo -e "${RED}FAIL${NC} ${name}"
    return 1
  fi
}

FAIL=0
run "Module A — Deploy (ch13)" "${SCRIPT_DIR}/validate-lab.sh" || FAIL=$((FAIL+1))
run "Module B — Plugins (ch14)" "${VALIDATE}/validate-demo-ch14.sh" || FAIL=$((FAIL+1))
run "Module C — Environmental (ch15)" "${VALIDATE}/validate-demo-ch15.sh" || FAIL=$((FAIL+1))
run "Module D — Multi-board" "${SCRIPT_DIR}/validate-lab-multiboard.sh" || FAIL=$((FAIL+1))
run "Module E — Virtual Networking (ch05)" "${SCRIPT_DIR}/validate-lab-vn.sh" || FAIL=$((FAIL+1))
run "Module F — WSTUN / Web Services" "${SCRIPT_DIR}/validate-lab-wstun.sh" || FAIL=$((FAIL+1))
run "Module G — Federated Learning (ch19)" "${SCRIPT_DIR}/validate-lab-fl.sh" || FAIL=$((FAIL+1))
run "Module H — Blueprint / K3s (ch11)" "${VALIDATE}/validate-demo-ch11.sh" || FAIL=$((FAIL+1))
run "Module I — IoT Metrics" "${SCRIPT_DIR}/validate-lab-metrics.sh" || FAIL=$((FAIL+1))

echo ""
echo "=============================================="
if [[ "$FAIL" -eq 0 ]]; then
  echo -e "${GREEN}All module validators passed${NC}"
  exit 0
else
  echo -e "${RED}${FAIL} module validator(s) failed${NC}"
  exit 1
fi
