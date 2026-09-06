# S4T Lab — Hands-on Commands (all modules)

Replace `{{VM_IP}}` with your lab host IP (see `vm-ip.txt.example` — copy to `vm-ip.txt` locally).

Credentials: Horizon `admin/s4t` · Lightning-Rod `me/arancino` · InfluxDB `admin/admin`

---

## Core — Module A (Ch.13 Deploy)

```bash
docker --version && docker compose version
groups | grep docker
free -h
git clone https://github.com/AssemblingSmartCPS/ch13.git
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml ps
curl -s -o /dev/null -w '%{http_code}\n' http://{{VM_IP}}:8812/
```

Browser: `http://{{VM_IP}}/horizon` · `http://{{VM_IP}}:1474`

Horizon **Boards** → **Create LR Container** auto-creates a virtual board + Lightning-Rod (port ≥1480). Manual Cap.13 flow remains **Create Board**.


```bash
cd training && ./validate-lab.sh
```

---

## Core — Module B (Ch.14 Plugins)

Use fixed Hello plugin: `training/ch14-fixed/plugins/synchronous/hello_name_plugin.py`

Plugin Call JSON:

```json
{"name": "Messina"}
```

```bash
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml logs -f lightning-rod
docker exec lightning-rod ls /var/run/docker.sock
```

Docker plugin call (optional):

```json
{
  "operation": "run",
  "image": "alpine",
  "command": "echo hello from alpine"
}
```

---

## Core — Module C (Ch.15 Environmental)

```bash
curl http://{{VM_IP}}:8086/ping
curl http://{{VM_IP}}:8093/health
docker exec influxdb influx -username admin -password admin \
  -execute 'CREATE DATABASE IF NOT EXISTS s4t_iot'
docker exec -it lightning-rod pip install pandas requests
docker exec -it influxdb influx -username admin -password admin
```

Start plugin in Horizon with **Enable cloud metrics** checked (auto-provisions gateway token).

Influx shell:

```sql
USE s4t_iot;
SHOW MEASUREMENTS;
SELECT * FROM environmental_data LIMIT 5;
```

Lab plugin: `training/ch15-lab/plugin_demo_lab.py` (uses `MetricsWriter` + `/opt/lab/s4t_metrics.py`)

---

## Extension — Module I (IoT Metrics)

```bash
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d \
  influxdb grafana metrics-gateway iotronic-ui
python3 ../../experiments/metrics/verify-metrics-lab.py
./../../validate-lab-metrics.sh
```

| URL | Purpose |
|-----|---------|
| `http://{{VM_IP}}:8093/health` | Metrics gateway |
| `http://{{VM_IP}}:3000` | Grafana |
| `http://{{VM_IP}}/horizon/iot/iot_metrics/` | Horizon Metrics panel |
| `http://{{VM_IP}}/horizon/metrics-live/` | Grafana iframe proxy |

Provision + write (API):

```bash
curl -s -X POST http://{{VM_IP}}:8093/v1/streams/provision \
  -H 'Content-Type: application/json' \
  -d '{"board_uuid":"...","board_name":"board-alpha","plugin_uuid":"...","plugin_name":"env","measurement":"environmental_data"}'
```

---

## Extension — Module D (Multi-board)

```bash
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d lightning-rod-2 lightning-rod-3
training/experiments/multiboard/check-endpoints.sh
cd training && ./validate-lab-multiboard.sh
curl -s http://{{VM_IP}}:8812/v1/boards/ | python3 -m json.tool
```

| Board | LR URL |
|-------|--------|
| board-alpha | `http://{{VM_IP}}:1474` |
| board-beta | `http://{{VM_IP}}:1475` |
| board-gamma | `http://{{VM_IP}}:1476` |

Horizon boards: `http://{{VM_IP}}/horizon/iot/`  
Fleets: `http://{{VM_IP}}/horizon/iot/fleets/`

---

## Extension — Module E (Virtual Networking Ch.5)

```bash
cd training
./experiments/virtual-networking/attach-port.sh boards
./experiments/virtual-networking/attach-port.sh list
./experiments/virtual-networking/attach-port.sh list <BOARD_UUID>
./validate-lab-vn.sh
```

Attach port (when network UUID known):

```bash
curl -X POST http://{{VM_IP}}:8812/v1/boards/<BOARD_UUID>/ports/ \
  -H "Content-Type: application/json" \
  -d '{"network": "<NETWORK_UUID>"}'
```

Fallback logs:

```bash
docker logs iotronic-wagent 2>&1 | tail -30
docker logs iotronic-wstun 2>&1 | tail -30
```

---

## Extension — Module F (Web Services / WSTUN)

Automated demo (creates service + enables tunnel + captures screenshots):

```bash
cd training
.venv/bin/python experiments/webservices/setup-wstun-demo.py
./validate-lab-wstun.sh
```

Manual API flow:

```bash
# 1) Create service — Porta MUST be 50000 (NOT 0 — Horizon form default!)
curl -X POST http://{{VM_IP}}:8812/v1/services \
  -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"lr-nginx-demo","port":50000,"protocol":"TCP"}'

# 2) Enable on Active board → assigns cloud port on WSTUN
curl -X POST http://{{VM_IP}}:8812/v1/boards/<BOARD_UUID>/services/lr-nginx-demo/action \
  -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -d '{"action":"ServiceEnable"}'

# 3) Verify cloud endpoint (example port 50002)
curl -v http://{{VM_IP}}:50002/
```

Horizon UI: `http://{{VM_IP}}/horizon/iot/services/` · `http://{{VM_IP}}/horizon/iot/webservices/`

Logs:

```bash
docker logs iotronic-wstun 2>&1 | tail -20
docker logs lightning-rod 2>&1 | grep -i 'Cloud service'
```

---

## Advanced — Module G (Federated Learning Ch.19)

### Horizon panel (recommended)

```bash
cd training
./experiments/federated-learning/install-fl-on-boards.sh
./experiments/federated-learning/setup-fl-horizon.sh
./experiments/federated-learning/setup-fl-demo-plugins.sh   # optional demo-ready
```

Open `http://<IP>/horizon/iot/federated_learning/`:

1. **Parameters** (optional) → Save (auto-restarts Flower server if already running)
2. **Select plugin** — `fl-client-heart` or `fl-client-pm` (auto start/restart server + clients)
3. **Start server** / **Stop server**
4. **Inject on all boards** (if needed)
5. **Start all clients** (edge only; server must be running)
6. **Live topology** iframe

IoT sidebar notes: **Boards** = `/horizon/iot/` (not `/horizon/iot/boards/`). **Fleets** — create fleet, pick members (Members tab), run plugin ops on all members (Operations tab). **Web Services** empty until Module F WSTUN demo. FL uses **board-alpha/beta/gamma** only.

Validate:

```bash
cd training && ./validate-lab-fl.sh
```

Capture slide screenshots (Module G deck):

```bash
cd training && ./experiments/federated-learning/capture-fl-screenshots.sh
```

### CLI / local simulation (debug)

```bash
cd training/repos/ch19
pip install flwr torch pandas scikit-learn
FL_ROUNDS=2 python3 server.py
```

Or: `training/experiments/federated-learning/fl-server-ctl.sh start`

Two cloud plugins: **`fl-client-heart`** (heart_*.csv) and **`fl-client-pm`** (machine_*.csv). Per-board JSON sets `csv_file`, `board_name`, `fl_scenario`; server/dashboard from Parameters.

---

## Advanced — Module H (Blueprint Ch.11)

```bash
free -h
training/experiments/blueprint/k3s-prereq.sh
curl -sfL https://get.k3s.io | sh -
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
kubectl get nodes
```

Repos: `training/repos/ch11_xplane-provider-for-s4t` · `training/repos/ch11_s4t-k3s-deploy`

---

## Advanced — Module I (FaaS / Deviceless Ch.7)

Theory + on-lab contrast:

1. HelloName Plugin Call (one-shot): `{"name": "FaaS-demo"}`
2. Start environmental async plugin (continuous loop)

---

## Asset regeneration

```bash
cd training
.venv/bin/python scripts/generate_diagrams.py
.venv/bin/python scripts/capture_dashboards.py
.venv/bin/python generate_slides_modular_en.py
```
