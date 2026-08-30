#!/usr/bin/env bash
# Module E — virtual networking API (Cap. 5)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"
CONDUCTOR="http://${HOST}:8812"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

echo "=== Module E: Virtual Networking ==="

c=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "${CONDUCTOR}/" || echo "000")
[[ "$c" != "000" ]] && ok "Conductor reachable" || fail_msg "Conductor unreachable"

docker ps --format '{{.Names}}' 2>/dev/null | grep -q iotronic-wstun \
  && ok "WSTUN agent running" || warn_msg "iotronic-wstun not running"

docker ps --format '${{.Names}}' 2>/dev/null | grep -q iotronic-wagent \
  && ok "WAgent running" || warn_msg "iotronic-wagent not running"

PORTS=$(curl -s --connect-timeout 5 "${CONDUCTOR}/v1/ports/" 2>/dev/null || echo "")
if echo "$PORTS" | grep -qi 'VIF\|ports\|uuid'; then
  ok "Ports API responds"
else
  warn_msg "Ports API empty or needs board attach — use attach-port.sh after board Active"
fi

[[ -x "${SCRIPT_DIR}/experiments/virtual-networking/attach-port.sh" ]] \
  && ok "attach-port.sh helper present" || fail_msg "missing attach-port.sh"

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
