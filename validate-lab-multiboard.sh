#!/usr/bin/env bash
# Module D — multi-board + optional second/third LR (Cap. 13-14, 19)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

echo "=== Module D: Multi-board ==="
echo "Host: ${HOST}"

for port in 1474 1475 1476; do
  c=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "http://${HOST}:${port}/" || echo "000")
  if [[ "$c" =~ ^(200|302)$ ]]; then ok "LR UI :${port} HTTP ${c}"
  else warn_msg "LR UI :${port} HTTP ${c}"; fi
done

docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^lightning-rod-2$' \
  && ok "Container lightning-rod-2" || warn_msg "lightning-rod-2 not running (optional until Module D)"

docker ps --format '{{.Names}}' 2>/dev/null | grep -q '^lightning-rod-3$' \
  && ok "Container lightning-rod-3" || warn_msg "lightning-rod-3 not running (optional until Module D)"

# Conductor boards list (may need auth in production; lab often open)
BOARDS=$(curl -s --connect-timeout 5 "http://${HOST}:8812/v1/boards/" 2>/dev/null || echo "")
if echo "$BOARDS" | grep -qi 'uuid\|boards'; then
  n=$(echo "$BOARDS" | grep -o '"uuid"' | wc -l)
  [[ "$n" -ge 1 ]] && ok "Conductor lists boards (count~${n})" || warn_msg "No boards registered yet — create in Horizon"
else
  warn_msg "Could not list boards via API — register manually in Horizon"
fi

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
