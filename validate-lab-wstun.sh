#!/usr/bin/env bash
# Module F — WSTUN port forwarding / web service exposure
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"
STATE="${SCRIPT_DIR}/experiments/webservices/wstun-state.json"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

echo "=== Module F: WSTUN / Web Services ==="

docker ps --format '{{.Names}}' 2>/dev/null | grep -q iotronic-wstun \
  && ok "iotronic-wstun running" || fail_msg "iotronic-wstun not running"

c=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "http://${HOST}:8080/" 2>/dev/null || echo "000")
[[ "$c" != "000" ]] && ok "WSTUN control :8080 reachable (HTTP ${c})" || warn_msg "WSTUN :8080 not reachable"

SVC_PORT=$(python3 - <<PY 2>/dev/null || echo "0"
import json, urllib.request, os
os.chdir("${SCRIPT_DIR}")
HOST=open("vm-ip.txt").read().strip()
body=json.dumps({"auth":{"identity":{"methods":["password"],"password":{"user":{"name":"admin","domain":{"name":"Default"},"password":"s4t"}}},"scope":{"project":{"name":"admin","domain":{"name":"Default"}}}}}).encode()
req=urllib.request.Request(f"http://{HOST}:5000/v3/auth/tokens",data=body,headers={"Content-Type":"application/json"},method="POST")
with urllib.request.urlopen(req) as r: t=r.headers["X-Subject-Token"]
req=urllib.request.Request(f"http://{HOST}:8812/v1/services/",headers={"X-Auth-Token":t})
with urllib.request.urlopen(req) as r:
    for s in json.loads(r.read()).get("services",[]):
        if s.get("name")=="lr-nginx-demo":
            print(int(s.get("port") or 0)); break
PY
)
[[ "$SVC_PORT" -ge 1 ]] && ok "Service lr-nginx-demo port=${SVC_PORT}" || fail_msg "Service port=0 or missing — fix Create Service form"

CLOUD_PORT=""
if [[ -f "$STATE" ]]; then
  CLOUD_PORT=$(python3 -c "import json; print(json.load(open('$STATE')).get('cloud_port',''))" 2>/dev/null || true)
fi
if [[ -z "$CLOUD_PORT" ]]; then
  warn_msg "No wstun-state.json — run experiments/webservices/setup-wstun-demo.py"
else
  tc=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://${HOST}:${CLOUD_PORT}/" || echo "000")
  [[ "$tc" == "200" ]] && ok "Cloud tunnel :${CLOUD_PORT} → board HTTP 200" || warn_msg "Tunnel :${CLOUD_PORT} HTTP ${tc}"
fi

[[ -f "${SCRIPT_DIR}/assets/chapter14/horizon-boards-with-services.png" ]] \
  && ok "Screenshot horizon-boards-with-services.png" || warn_msg "Missing filled boards screenshot"

[[ -x "${SCRIPT_DIR}/experiments/webservices/setup-wstun-demo.py" ]] \
  && ok "setup-wstun-demo.py present" || fail_msg "setup-wstun-demo.py missing"

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
