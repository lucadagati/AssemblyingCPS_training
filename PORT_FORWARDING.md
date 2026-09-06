# Browser access to the S4T lab

Replace `{{VM_IP}}` with the address participants use to reach the lab host
(LAN, VPN, or other routable IP). Set the same value in `vm-ip.txt` (see
`vm-ip.txt.example`) and optionally `export S4T_LAB_HOST=$(cat vm-ip.txt)`.

Details: [`docs/LAB_NETWORK_ACCESS.md`](docs/LAB_NETWORK_ACCESS.md).

## Core services

| Service | URL |
|---------|-----|
| **Horizon UI** | `http://{{VM_IP}}/horizon` |
| **Lightning-Rod UI (alpha)** | `http://{{VM_IP}}:1474` |
| **IoTronic API** | `http://{{VM_IP}}:8812` |
| **InfluxDB** | `http://{{VM_IP}}:8086` |
| **Grafana** | `http://{{VM_IP}}:3000` |

Credentials: Horizon `admin` / `s4t` · Lightning-Rod `me` / `arancino` · InfluxDB/Grafana `admin` / `admin`

## WoT / WSTUN demos

Use the **same host** as Horizon plus the published WSTUN port:

| Demo (typical) | URL |
|----------------|-----|
| wot-fritzing | `http://{{VM_IP}}:50006/` |
| weather-wot | `http://{{VM_IP}}:50064/` |
| lr-nginx-demo | `http://{{VM_IP}}:50008/` |

Do not use `127.0.0.1` from a remote browser. The Horizon **Web Services (WoT)**
panel builds these URLs from the session Host header.

## IoT dashboards

| Panel | URL |
|-------|-----|
| **Boards** | `http://{{VM_IP}}/horizon/iot/` |
| **Plugins** | `http://{{VM_IP}}/horizon/iot/plugins/` |
| **Services** | `http://{{VM_IP}}/horizon/iot/services/` |
| **Fleets** | `http://{{VM_IP}}/horizon/iot/fleets/` |
| **Federated Learning** | `http://{{VM_IP}}/horizon/iot/federated_learning/` |
| **Metrics** | `http://{{VM_IP}}/horizon/iot/metrics/` (live iframe `/horizon/metrics-live/`) |
| **Web Services (WoT)** | see enabled IoT panels under `/horizon/iot/` |

Lightning-Rod host ports (lab containers):

| Board | URL |
|-------|-----|
| alpha | `http://{{VM_IP}}:1474/` |
| beta | `http://{{VM_IP}}:1475/` |
| gamma | `http://{{VM_IP}}:1476/` |
| delta | `http://{{VM_IP}}:1477/` |
| epsilon | `http://{{VM_IP}}:1478/` |
| zeta | `http://{{VM_IP}}:1479/` |
| manual LR boards | `http://{{VM_IP}}:1482+` — see `lab-ops/04-list-lr-dashboards.sh` |

Note: `/horizon/iot/boards/` returns **404** — Boards live at `/horizon/iot/`.

Quick check:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}:8812/
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}/horizon
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}:50006/
```

---

## Ports published on the lab host

| Port | Service |
|-----:|---------|
| 80 | Horizon (+ FL/metrics live proxies under `/horizon/…`) |
| 1474–1479+ | Lightning-Rod UIs |
| 5000 | Keystone |
| 8080 | WSTUN |
| 8181 | Crossbar WAMP |
| 8812 | IoTronic Conductor |
| 50001–50100 | WSTUN public tunnels |
| 8086 / 3000 / 8090–8093 | Influx / Grafana / FL / metrics (lab overlay) |

---

## Optional: IDE port forwarding

If you develop on the lab host via an IDE that can forward ports:

| Port | Service |
|------|---------|
| 80 | Horizon |
| 1474 | Lightning-Rod UI |
| 8812 | IoTronic Conductor |
| 8086 | InfluxDB |

---

## Optional: reverse proxy + public tunnel

When the lab host IP is not reachable from participant networks:

```bash
.venv/bin/python scripts/s4t_proxy.py --port 9080
# then expose 127.0.0.1:9080 with your preferred tunnel tool
# or: ./scripts/start_lab_proxy.sh
```

---

## Screenshots for slides (on the lab host)

```bash
.venv/bin/python scripts/capture_horizon_authenticated.py
.venv/bin/python scripts/capture_screenshots.py
```

Assets under `assets/chapter13|14|15/`.
