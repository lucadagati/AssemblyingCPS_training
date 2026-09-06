# Browser access to the S4T lab

Replace `{{VM_IP}}` with **the IP you use to reach this VM** (LAN, Tailscale primary, or Tailscale secondary).  
Same services answer on all of them — see [`docs/LAB_NETWORK_ACCESS.md`](docs/LAB_NETWORK_ACCESS.md).

Examples on the conference lab VM:

| Ingress | Example IP |
|---------|------------|
| LAN | `192.168.100.11` |
| Tailscale primary (`asseblingcps`) | `100.74.114.23` |
| Tailscale secondary (`lab-secondary`) | `100.123.142.39` |

Copy `vm-ip.txt.example` → `vm-ip.txt` for scripts (`S4T_LAB_HOST`).

## Recommended: open Horizon on your ingress IP

| Service | URL |
|---------|-----|
| **Horizon UI** | `http://{{VM_IP}}/horizon` |
| **Lightning-Rod UI (alpha)** | `http://{{VM_IP}}:1474` |
| **IoTronic API** | `http://{{VM_IP}}:8812` |
| **InfluxDB** | `http://{{VM_IP}}:8086` |
| **Grafana** | `http://{{VM_IP}}:3000` |

Credentials: Horizon `admin` / `s4t` · Lightning-Rod `me` / `arancino` · InfluxDB/Grafana `admin` / `admin`

## WoT / WSTUN demos (direct host:port — preferred)

Use the **same host** you open Horizon with, plus the published WSTUN port
(same VM; no reverse-proxy path):

| Demo (typical) | URL |
|----------------|-----|
| wot-fritzing | `http://{{VM_IP}}:50006/` |
| weather-wot | `http://{{VM_IP}}:50064/` |
| lr-nginx-demo | `http://{{VM_IP}}:50008/` |

Do not use `127.0.0.1` from a remote browser. Horizon **Web Services (WoT)**
builds these URLs from your session Host header.

Optional: `/lab-ws/<port>/` on `:80` still works as a same-origin proxy.

## IoT dashboards

| Panel | URL |
|-------|-----|
| **Boards** | `http://{{VM_IP}}/horizon/iot/` |
| **Plugins** | `http://{{VM_IP}}/horizon/iot/plugins/` |
| **Services** | `http://{{VM_IP}}/horizon/iot/services/` |
| **Fleets** | `http://{{VM_IP}}/horizon/iot/fleets/` |
| **Federated Learning** | `http://{{VM_IP}}/horizon/iot/federated_learning/` |
| **Metrics** | `http://{{VM_IP}}/horizon/iot/metrics/` (live iframe `/horizon/metrics-live/`) |
| **Web Services (WoT)** | `http://{{VM_IP}}/horizon/iot/wot/` (path may vary by enabled panel) |

Lightning-Rod host ports (lab containers):

| Board | URL |
|-------|-----|
| alpha | `http://{{VM_IP}}:1474/` |
| beta | `http://{{VM_IP}}:1475/` |
| gamma | `http://{{VM_IP}}:1476/` |
| delta | `http://{{VM_IP}}:1477/` |
| epsilon | `http://{{VM_IP}}:1478/` |
| zeta | `http://{{VM_IP}}:1479/` |
| manuals (SWC) | `http://{{VM_IP}}:1482+` — see `swc2026/04-list-lr-dashboards.sh` |

Note: `/horizon/iot/boards/` returns **404** — Boards live at `/horizon/iot/`.

Quick check:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}:8812/
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}/horizon
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}/lab-ws/50006/
```

---

## Ports published on the VM

| Port | Service |
|-----:|---------|
| 80 | Horizon + `/lab-ws/` + FL/metrics live proxies |
| 1474–1479+ | Lightning-Rod UIs |
| 5000 | Keystone |
| 8080 | WSTUN |
| 8181 | Crossbar WAMP |
| 8812 | IoTronic Conductor |
| 50001–50100 | WSTUN public tunnels |
| 8086 / 3000 / 8090–8093 | Influx / Grafana / FL / metrics (lab overlay) |

---

## Alternative: Cursor port forwarding

| Port | Service |
|------|---------|
| 80 | Horizon |
| 1474 | Lightning-Rod UI |
| 8812 | IoTronic Conductor |
| 8086 | InfluxDB |

---

## Fallback: reverse proxy + Cloudflare tunnel

```bash
.venv/bin/python scripts/s4t_proxy.py --port 9080
cloudflared tunnel --url http://127.0.0.1:9080 | tee proxy-tunnel.log
# or: ./scripts/start_lab_proxy.sh
```

---

## Screenshots for slides (on the VM)

```bash
.venv/bin/python scripts/capture_horizon_authenticated.py
.venv/bin/python scripts/capture_screenshots.py
```

Assets under `assets/chapter13|14|15/`.
