#!/usr/bin/env bash
# Fix iotronic-conductor crash: MultipleResultsFound on wampagents (stale online rows).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CH13="${ROOT}/repos/ch13"
# shellcheck source=/dev/null
source "${CH13}/.env" 2>/dev/null || true

DB_PASS="${MYSQL_ROOT_PASSWORD:-unime}"

echo "=== Fix duplicate WAMP agent registrations ==="

CURRENT_WAGENT=$(docker inspect -f '{{.Config.Hostname}}' iotronic-wagent 2>/dev/null || echo "")
CURRENT_COND=$(docker inspect -f '{{.Config.Hostname}}' iotronic-conductor 2>/dev/null || echo "")

if [[ -z "$CURRENT_WAGENT" ]]; then
  echo "iotronic-wagent not running — start the stack first"
  exit 1
fi

docker exec iotronic-db mysql -uroot -p"${DB_PASS}" iotronic -e "
DELETE FROM wampagents WHERE hostname != '${CURRENT_WAGENT}';
UPDATE wampagents SET online=1, ragent=1 WHERE hostname='${CURRENT_WAGENT}';
DELETE FROM conductors WHERE hostname != '${CURRENT_COND}' AND '${CURRENT_COND}' != '';
UPDATE conductors SET online=1 WHERE hostname='${CURRENT_COND}';
UPDATE boards SET agent='${CURRENT_WAGENT}' WHERE agent IS NULL OR agent != '${CURRENT_WAGENT}';
SELECT id, hostname, ragent, online FROM wampagents;
SELECT id, hostname, online FROM conductors;
SELECT name, status, agent FROM boards;
"

echo "Restarting iotronic-wagent and iotronic-conductor..."
docker restart iotronic-wagent
sleep 6
docker restart iotronic-conductor
sleep 12

code=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 http://127.0.0.1:8812/ || echo "000")
if [[ "$code" == "200" ]]; then
  echo "OK — Conductor API HTTP $code (Horizon boards list should work)"
else
  echo "WARN — Conductor API HTTP $code — check docker logs iotronic-conductor"
  exit 1
fi

echo "Sync stale WAMP agent id in LR settings.json (board-alpha volume)..."
for c in lightning-rod lightning-rod-2 lightning-rod-3; do
  if docker ps --format '{{.Names}}' | grep -qx "$c"; then
    docker exec "$c" sed -i "s/\"agent\": \"[^\"]*\"/\"agent\": \"${CURRENT_WAGENT}\"/" /etc/iotronic/settings.json 2>/dev/null \
      && docker restart "$c" >/dev/null 2>&1 || true
  fi
done
sleep 15
echo "Board status:"
docker exec iotronic-db mysql -uroot -p"${DB_PASS}" iotronic -N -e "SELECT name, status FROM boards;" 2>/dev/null || true
