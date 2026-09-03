#!/usr/bin/env bash
# Module D — multi-board + optional second/third LR (Cap. 13-14, 19)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOST="${1:-$(cat "${SCRIPT_DIR}/vm-ip.txt" 2>/dev/null || hostname -I | awk '{print $1}')}"
KEYSTONE_PORT="${KEYSTONE_PORT:-5000}"
HZ_USER="${S4T_HORIZON_USER:-admin}"
HZ_PASS="${S4T_HORIZON_PASS:-s4t}"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

keystone_token() {
  curl -s -X POST "http://${HOST}:${KEYSTONE_PORT}/v3/auth/tokens" \
    -H "Content-Type: application/json" \
    -d "{\"auth\":{\"identity\":{\"methods\":[\"password\"],\"password\":{\"user\":{\"name\":\"${HZ_USER}\",\"domain\":{\"name\":\"Default\"},\"password\":\"${HZ_PASS}\"}}},\"scope\":{\"project\":{\"name\":\"admin\",\"domain\":{\"name\":\"Default\"}}}}}" \
    -i 2>/dev/null | awk 'BEGIN{IGNORECASE=1} /^X-Subject-Token:/ {sub(/\r$/,""); sub(/^[^:]*:[ \t]*/,""); print; exit}'
}

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

TOKEN="$(keystone_token)"
if [[ -n "$TOKEN" ]]; then
  BOARDS=$(curl -s --connect-timeout 5 -H "X-Auth-Token: ${TOKEN}" "http://${HOST}:8812/v1/boards/" 2>/dev/null || echo "")
  if echo "$BOARDS" | grep -qiE 'uuid|boards|"name"'; then
    n=$(echo "$BOARDS" | grep -o '"uuid"' | wc -l)
    [[ "$n" -ge 1 ]] && ok "Conductor lists boards (count~${n})" || warn_msg "No boards registered yet — create in Horizon"
  else
    warn_msg "Conductor boards API returned no data — register manually in Horizon"
  fi
else
  warn_msg "Could not obtain Keystone token — register boards manually in Horizon"
fi

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
