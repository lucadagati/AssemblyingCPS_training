#!/usr/bin/env bash
# K3s prerequisite check for Ch.11 Blueprint module (same VM as S4T Docker stack)
set -euo pipefail

MIN_RAM_GB="${MIN_RAM_GB:-8}"
FREE_KB=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
FREE_GB=$((FREE_KB / 1024 / 1024))

echo "=== Blueprint / K3s prerequisites ==="
echo "MemAvailable: ${FREE_GB} GB (recommended >= ${MIN_RAM_GB} GB with S4T running)"

if [[ "$FREE_GB" -lt "$MIN_RAM_GB" ]]; then
  echo "WARN: low free RAM — stop optional containers or run Blueprint on a fresh boot"
  exit 1
fi

if command -v k3s >/dev/null 2>&1; then
  echo "k3s: $(k3s --version 2>/dev/null | head -1)"
  sudo k3s kubectl get nodes 2>/dev/null || true
else
  echo "k3s not installed. Install (instructor pre-step):"
  echo "  curl -sfL https://get.k3s.io | sh -"
  echo "  export KUBECONFIG=/etc/rancher/k3s/k3s.yaml"
fi

REPO="$(cd "$(dirname "$0")/../.." && pwd)/repos/ch11_xplane-provider-for-s4t"
if [[ -d "$REPO" ]]; then
  echo "Crossplane provider repo: $REPO"
else
  echo "Missing repo — git clone https://github.com/AssemblingSmartCPS/ch11_xplane-provider-for-s4t"
  exit 1
fi

echo "OK prerequisites checked"
