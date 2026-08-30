#!/usr/bin/env bash
# Start S4T reverse proxy (optional) + Cloudflare quick tunnel.
# Prefer direct VM IP access — see training/PORT_FORWARDING.md and training/vm-ip.txt
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="${ROOT}/.venv/bin/python"
PROXY="${ROOT}/scripts/s4t_proxy.py"
PORT="${S4T_PROXY_PORT:-9080}"
LOG="${ROOT}/proxy-tunnel.log"
URL_FILE="${ROOT}/proxy-url.txt"

if [[ ! -x "$VENV" ]]; then
  echo "Missing venv: ${ROOT}/.venv" >&2
  exit 1
fi

# Proxy in background if not already listening
if ! curl -sf "http://127.0.0.1:${PORT}/horizon" -o /dev/null 2>/dev/null; then
  echo "Starting reverse proxy on :${PORT}..."
  nohup "$VENV" "$PROXY" --port "$PORT" > "${ROOT}/proxy.log" 2>&1 &
  sleep 1
fi

if ! command -v cloudflared >/dev/null 2>&1 && [[ -x /tmp/cloudflared ]]; then
  export PATH="/tmp:$PATH"
fi

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared not found. Install or place binary at /tmp/cloudflared" >&2
  echo "Direct VM IP may still work — see training/vm-ip.txt" >&2
  exit 1
fi

echo "Starting Cloudflare tunnel → http://127.0.0.1:${PORT}"
echo "Log: ${LOG}"
cloudflared tunnel --url "http://127.0.0.1:${PORT}" 2>&1 | tee "$LOG" &
TUNNEL_PID=$!

for i in $(seq 1 30); do
  if grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' "$LOG" | head -1 > "$URL_FILE"; then
    URL=$(cat "$URL_FILE")
    if [[ -n "$URL" ]]; then
      echo ""
      echo "Tunnel URL saved to ${URL_FILE}:"
      echo "  Horizon:  ${URL}/horizon"
      echo "  LR UI:    ${URL}/lr/"
      echo "  Conductor:${URL}/conductor/"
      echo ""
      echo "Prefer VM IP if reachable — see training/vm-ip.txt"
      wait $TUNNEL_PID
      exit 0
    fi
  fi
  sleep 1
done

echo "Timeout waiting for tunnel URL" >&2
kill $TUNNEL_PID 2>/dev/null || true
exit 1
