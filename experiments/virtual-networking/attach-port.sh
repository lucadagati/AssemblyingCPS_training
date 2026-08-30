#!/usr/bin/env bash
# IoTronic networking API helpers — Ch.5 virtual networking lab
# Usage: source training/experiments/virtual-networking/env.sh
#        ./attach-port.sh list [BOARD_UUID]
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VM_IP_FILE="${ROOT}/vm-ip.txt"
HOST="${S4T_LAB_HOST:-$(cat "$VM_IP_FILE" 2>/dev/null || hostname -I | awk '{print $1}')}"
CONDUCTOR="http://${HOST}:8812"
KEystone="${S4T_KEYSTONE:-http://${HOST}:5000/v3}"

list_boards() {
  curl -s "${CONDUCTOR}/v1/boards/" | python3 -m json.tool 2>/dev/null || curl -s "${CONDUCTOR}/v1/boards/"
}

list_ports() {
  local board_uuid="${1:-}"
  if [[ -n "$board_uuid" ]]; then
    curl -s "${CONDUCTOR}/v1/boards/${board_uuid}/ports/" | python3 -m json.tool 2>/dev/null || true
  else
    curl -s "${CONDUCTOR}/v1/ports/" | python3 -m json.tool 2>/dev/null || true
  fi
}

attach_port() {
  local board_uuid="$1"
  local network_uuid="${2:-}"
  if [[ -z "$network_uuid" ]]; then
    echo "Usage: attach-port.sh attach <BOARD_UUID> <NETWORK_UUID>" >&2
    exit 1
  fi
  curl -s -X POST "${CONDUCTOR}/v1/boards/${board_uuid}/ports/" \
    -H "Content-Type: application/json" \
    -d "{\"network\": \"${network_uuid}\"}" | python3 -m json.tool 2>/dev/null || true
}

cmd="${1:-list}"
case "$cmd" in
  boards) list_boards ;;
  list)   list_ports "${2:-}" ;;
  attach) attach_port "${2:-}" "${3:-}" ;;
  *)
    echo "Commands: boards | list [BOARD_UUID] | attach BOARD_UUID NETWORK_UUID"
    echo "Conductor: ${CONDUCTOR}"
    ;;
esac
