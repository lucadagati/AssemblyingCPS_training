#!/usr/bin/env bash
# Clone AssemblingSmartCPS org repos required for modules A–I
set -euo pipefail

DEST="$(cd "$(dirname "$0")/.." && pwd)/repos"
mkdir -p "$DEST"
cd "$DEST"

clone() {
  local name="$1"
  if [[ -d "$name/.git" ]]; then
    echo "SKIP $name (exists)"
  else
    git clone --depth 1 "https://github.com/AssemblingSmartCPS/${name}.git"
  fi
}

clone ch13
clone ch14
clone ch15
clone ch05
clone ch19
clone ch11_s4t-k3s-deploy
clone ch11_xplane-provider-for-s4t

echo "Repos in $DEST"
