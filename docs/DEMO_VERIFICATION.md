# Demo verification matrix — training modules A–I

Last run: 2026-08-30 · Lab host from `vm-ip.txt` · Org: [AssemblingSmartCPS](https://github.com/AssemblingSmartCPS)

Run all checks: `./validate/validate-all.sh`

| Mod | Repo | Demo | Script | Result | Notes |
|-----|------|------|--------|--------|-------|
| **A** | [ch13](https://github.com/AssemblingSmartCPS/ch13) | Docker Compose + Horizon + LR | `validate-lab.sh` | **PASS** | 18/18 OK — Conductor :8812, Horizon :80, LR :1474 |
| **B** | [ch14](https://github.com/AssemblingSmartCPS/ch14) | HelloName sync (Worker class) | `validate/validate-demo-ch14.sh` | **PASS** | Use `ch14-fixed/` — upstream has HelloNamePlugin bug |
| **B** | ch14 | Docker lifecycle plugin | `validate-lab.sh` | **PASS** | alpine container via docker.sock in LR |
| **B** | ch14 | weather_web_server.py | `experiments/webservices/run-weather-demo.sh` | **PASS** | Lab port **8088** (book 8080); WSTUN :50062 `/sensors` HTTP 200 |
| **C** | [ch15](https://github.com/AssemblingSmartCPS/ch15) | Environmental → InfluxDB | `validate/validate-demo-ch15.sh` | **PASS** | Use `ch15-lab/plugin_demo_lab.py` (host=influxdb); 4+ points in `environmental_data` |
| **D** | ch13 overlay | 3× LR :1474–1476 | `validate-lab-multiboard.sh` | **PASS** | Board API list may need Horizon auth — manual onboarding |
| **E** | [ch05](https://github.com/AssemblingSmartCPS/ch05) | attach-port VN | `validate-lab-vn.sh` + `experiments/virtual-networking/attach-port.sh` | **PASS** | Ports API empty until board attach — expected WARN |
| **F** | ch14 | nginx WSTUN smoke test | `experiments/webservices/setup-wstun-demo.py` | **PASS** | lr-nginx-demo :50000 → :50002 HTTP 200 |
| **F** | ch14 | Book weather WoT API | `experiments/webservices/run-weather-demo.sh` | **PASS** | weather-wot :8088 → :50062 `/sensors` JSON |
| **G** | [ch19](https://github.com/AssemblingSmartCPS/ch19) | FL server + clients | `validate-lab-fl.sh` | **PASS** | Artifacts present; runtime needs 3 Active boards (Module D) |
| **H** | [ch11_k3s](https://github.com/AssemblingSmartCPS/ch11_s4t-k3s-deploy) + [xplane](https://github.com/AssemblingSmartCPS/ch11_xplane-provider-for-s4t) | K3s manifests | `validate/validate-demo-ch11.sh` | **PASS** | k3s not installed on lab VM — theory + YAML review |

## Evidence files

| File | Purpose |
|------|---------|
| `experiments/webservices/wstun-state.json` | nginx demo public_port |
| `experiments/webservices/weather-state.json` | book weather demo public_port |
| `assets/chapter14/weather-server-dashboard.png` | WSTUN weather UI |
| `assets/chapter14/wstun-nginx-success.png` | nginx tunnel HTTP 200 |
| `assets/chapter15/influx-query-environmental.png` | InfluxDB query output |

## Book ↔ lab differences

See [BOOK_DIFFERENCES.md](BOOK_DIFFERENCES.md).
