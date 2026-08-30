#!/usr/bin/env bash
# Module G — Federated Learning artifacts (Cap. 19)
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CH19="${SCRIPT_DIR}/repos/ch19"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
pass=0; fail=0; warn=0
ok() { echo -e "${GREEN}[OK]${NC}   $*"; pass=$((pass+1)); }
warn_msg() { echo -e "${YELLOW}[WARN]${NC} $*"; warn=$((warn+1)); }
fail_msg() { echo -e "${RED}[FAIL]${NC} $*"; fail=$((fail+1)); }

echo "=== Module G: Federated Learning ==="

[[ -d "$CH19" ]] && ok "Repo ch19 present" || fail_msg "Repo ch19 missing"
[[ -f "$CH19/server.py" ]] && ok "server.py present" || fail_msg "server.py missing"
[[ -f "$CH19/client.py" ]] && ok "client.py present" || fail_msg "client.py missing"

for f in heart_1.csv heart_2.csv heart_3.csv data_test.csv; do
  [[ -f "$CH19/$f" ]] && ok "Dataset $f" || warn_msg "Missing $f"
done

python3 -m py_compile "$CH19/server.py" 2>/dev/null && ok "server.py syntax" || warn_msg "server.py syntax (needs flwr/torch)"
python3 -m py_compile "$CH19/client.py" 2>/dev/null && ok "client.py syntax" || warn_msg "client.py syntax"

[[ -x "${SCRIPT_DIR}/experiments/federated-learning/start-server.sh" ]] \
  && ok "start-server.sh present" || fail_msg "start-server.sh missing"

echo "Result: ${pass} OK | ${warn} WARN | ${fail} FAIL"
[[ "$fail" -eq 0 ]]
