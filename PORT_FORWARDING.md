# Browser access to the S4T lab

Replace `{{VM_IP}}` with your machine's public or LAN IP (set in `vm-ip.txt`).

## Recommended: VM public IP

| Service | URL |
|---------|-----|
| **Horizon UI** | `http://{{VM_IP}}/horizon` |
| **Lightning-Rod UI** | `http://{{VM_IP}}:1474` |
| **IoTronic API** | `http://{{VM_IP}}:8812` |
| **InfluxDB** | `http://{{VM_IP}}:8086` |

Credentials: Horizon `admin` / `s4t` · Lightning-Rod `me` / `arancino` · InfluxDB `admin` / `admin`

## IoT dashboards (browser extension / live demo)

After Horizon login, open these paths directly:

| Panel | URL |
|-------|-----|
| **Boards** | `http://{{VM_IP}}/horizon/iot/` |
| **Plugins** | `http://{{VM_IP}}/horizon/iot/plugins/` |
| **Fleets** | `http://{{VM_IP}}/horizon/iot/fleets/` |
| **Web Services** | `http://{{VM_IP}}/horizon/iot/webservices/` |

Lightning-Rod (login `me` / `arancino` first):

| Panel | URL |
|-------|-----|
| Home | `http://{{VM_IP}}:1474/` |
| Status | `http://{{VM_IP}}:1474/status` |
| Configuration | `http://{{VM_IP}}:1474/config` |

Note: `/horizon/iot/boards/` returns **404** — the correct Boards URL is `/horizon/iot/`.

Quick check from any machine:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}:8812/
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}/horizon
```

---

## Alternative: Cursor port forwarding

If you prefer `localhost`, forward these ports in the **Cursor Ports** panel:

| Port | Service |
|------|---------|
| 80 | Horizon |
| 1474 | Lightning-Rod UI |
| 8812 | IoTronic Conductor |
| 8086 | InfluxDB |

Then open `http://localhost/horizon`, etc.

---

## Fallback: reverse proxy + Cloudflare tunnel

Use only when the VM IP is not reachable (firewall, no VPN). Single entry point on port **9080**:

```bash
# Terminal 1
.venv/bin/python scripts/s4t_proxy.py --port 9080

# Terminal 2 — copy the https://*.trycloudflare.com URL
cloudflared tunnel --url http://127.0.0.1:9080 | tee proxy-tunnel.log
```

| Service | URL via tunnel |
|---------|----------------|
| Horizon | `https://TUNNEL/horizon` |
| Lightning-Rod | `https://TUNNEL/lr/` |
| IoTronic API | `https://TUNNEL/conductor/` |
| InfluxDB | `https://TUNNEL/influx/` |

Or use the helper script:

```bash
./scripts/start_lab_proxy.sh
```

---

## Screenshots for slides (on the VM)

Playwright runs locally on the VM and does not need browser extension access:

```bash
.venv/bin/python scripts/capture_horizon_authenticated.py
.venv/bin/python scripts/capture_screenshots.py
```

Assets are saved under `assets/chapter13|14|15/`.
