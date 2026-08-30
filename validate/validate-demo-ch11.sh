#!/usr/bin/env bash
# Module H — ch11 K3s + Crossplane provider (light smoke test)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
K3S_REPO="${SCRIPT_DIR}/repos/ch11_s4t-k3s-deploy"
XP_REPO="${SCRIPT_DIR}/repos/ch11_xplane-provider-for-s4t"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

echo "=== Module H: ch11 Blueprint / K3s ==="

[[ -d "$K3S_REPO" ]] && ok "ch11_s4t-k3s-deploy present" || fail_msg "ch11_s4t-k3s-deploy missing"
[[ -d "$XP_REPO" ]] && ok "ch11_xplane-provider-for-s4t present" || fail_msg "ch11_xplane-provider missing"
[[ -f "$K3S_REPO/README.md" ]] && ok "K3s deploy README present" || warn_msg "K3s README missing"

YAML_COUNT=$(find "$K3S_REPO/yaml_file" -name '*.yaml' 2>/dev/null | wc -l)
[[ "$YAML_COUNT" -ge 5 ]] && ok "K3s YAML manifests (${YAML_COUNT})" || warn_msg "Few K3s YAML files"

if command -v k3s >/dev/null 2>&1; then
  ok "k3s binary installed"
  if sudo k3s kubectl get nodes >/dev/null 2>&1; then
    ok "kubectl get nodes succeeds"
  else
    warn_msg "k3s installed but cluster not ready — instructor pre-step required"
  fi
else
  warn_msg "k3s not installed — Module H theory + manifest review only"
fi

[[ -x "${SCRIPT_DIR}/experiments/blueprint/k3s-prereq.sh" ]] \
  && ok "k3s-prereq.sh helper present" || warn_msg "k3s-prereq.sh missing"

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
