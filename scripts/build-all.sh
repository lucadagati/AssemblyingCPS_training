#!/usr/bin/env bash
# Full training material build + lab validation (standalone GitHub repo).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

HOST="${1:-$(cat vm-ip.txt 2>/dev/null || hostname -I | awk '{print $1}')}"
export S4T_LAB_HOST="${S4T_LAB_HOST:-$HOST}"

echo "=============================================="
echo " S4T Training — build-all workflow"
echo " Host: ${S4T_LAB_HOST}"
echo "=============================================="

step() { echo ""; echo ">>> $*"; }

step "1/7 Generate UML architecture + sequence diagrams"
python3 scripts/generate_diagrams.py 2>/dev/null || .venv/bin/python scripts/generate_diagrams.py

step "2/7 Generate English PPTX from decks/*.py"
python3 generate_slides_modular_en.py 2>/dev/null || .venv/bin/python generate_slides_modular_en.py

CH13="${ROOT}/repos/ch13"
PATCH="${ROOT}/patches/docker-compose.lab.yml"

if [[ ! -d "$CH13" ]]; then
  echo "WARN: repos/ch13 missing — run scripts/clone-repos.sh first"
  echo "Skipping deploy steps 3–7"
  exit 0
fi

step "3/7 Clean lab deployment (docker compose down)"
cd "$CH13"
docker compose -f docker-compose.yml -f "$PATCH" down --remove-orphans 2>/dev/null || true
cd "$ROOT"

step "4/7 Start fresh lab deployment"
cd "$CH13"
docker compose -f docker-compose.yml -f "$PATCH" up -d
echo "Waiting for Conductor + Crossbar (up to 3 min)..."
for i in $(seq 1 36); do
  if curl -sf --connect-timeout 3 "http://${S4T_LAB_HOST}:8812/" >/dev/null 2>&1; then
    echo "Conductor ready after $((i * 5))s"
    break
  fi
  sleep 5
done
cd "$ROOT"

step "4b/7 Onboard boards (board-alpha/beta/gamma)"
python3 scripts/onboard_multiboard.py 2>/dev/null || .venv/bin/python scripts/onboard_multiboard.py || echo "WARN: onboard manually in Horizon"

step "4c/7 Module G — FL Horizon panel + board dependencies"
chmod +x experiments/federated-learning/*.sh 2>/dev/null || true
./experiments/federated-learning/setup-fl-horizon.sh || echo "WARN: setup-fl-horizon skipped"
./experiments/federated-learning/install-fl-on-boards.sh || echo "WARN: install-fl-on-boards skipped"
./experiments/federated-learning/setup-fl-demo-plugins.sh || echo "WARN: setup-fl-demo-plugins skipped (need online boards)"

step "5/7 Run post-demo scripts (weather + nginx WSTUN)"
chmod +x experiments/webservices/run-weather-demo.sh validate/*.sh 2>/dev/null || true
./experiments/webservices/run-weather-demo.sh || echo "WARN: weather demo skipped"
python3 experiments/webservices/setup-wstun-demo.py 2>/dev/null || .venv/bin/python experiments/webservices/setup-wstun-demo.py || echo "WARN: wstun demo skipped"

step "6/7 Validate all modules"
./validate/validate-all.sh "$S4T_LAB_HOST"

echo ""
echo "=============================================="
echo " Build-all complete"
echo " Slides:  slides/Module*.pptx"
echo "=============================================="
