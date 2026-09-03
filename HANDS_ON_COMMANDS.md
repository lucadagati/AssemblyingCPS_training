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
docker exec influxdb influx -username admin -password admin \
  -execute 'CREATE DATABASE IF NOT EXISTS secco'
docker exec -it lightning-rod pip install influxdb pandas requests
docker exec -it influxdb influx -username admin -password admin
```

Influx shell:

```sql
USE secco;
SHOW MEASUREMENTS;
SELECT * FROM environmental_data LIMIT 5;
```

Lab plugin: `training/ch15-lab/plugin_demo_lab.py` (host=`influxdb`)

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

## Extension — Module F (Web Services / WoT)

### Horizon "Web Services" panel
Horizon panel at `http://{{VM_IP}}/horizon/iot/` → **Web Services** shows all active WSTUN
tunnels; select one to embed its Thing UI.

### Demo A — WoT Fritzing Lab (interactive circuit)
Multi-component circuit (4 LEDs, servo, motor, relay, LCD, button, live sensors).

```bash
cd training
bash experiments/webservices/run-wot-fritzing-demo.sh
# Opens: http://{{VM_IP}}:<wstun_port>/
```

Embedded at: `Horizon → Web Services` (tunnel auto-selected as "wot-fritzing").

### Demo B — Weather Station Dashboard
Rich dark-theme dashboard with board sensors (temp, humidity, pressure, lux, UV, CO₂),
LED control, trend chart, Messina Open Data (Open-Meteo), and interactive WoT API console.

```bash
bash experiments/webservices/run-weather-demo.sh
# Cloud URL written to experiments/webservices/weather-state.json
```

Board HTTP endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Dashboard UI |
| GET | `/sensors` | Board sensor data (JSON) |
| GET | `/led/status` | LED state |
| POST | `/led/toggle` | Toggle LED |
| POST | `/led/on` | Turn ON |
| POST | `/led/off` | Turn OFF |
| GET | `/opendata` | Messina meteo (Open-Meteo) |
| GET | `/history?n=30` | Rolling sensor history |

### Demo C — SSH Remote Access via S4T

All Lightning Rod containers run OpenSSH (credentials: **root / arancino**).
SSH is registered as a catalog service and tunnelled through WSTUN for remote access.

```bash
bash experiments/webservices/run-ssh-service.sh
# State written to experiments/webservices/ssh-state.json
```

Connect to a board:

```bash
ssh root@{{VM_IP}} -p <public_port>   # password: arancino
# Ports are listed in ssh-state.json; example defaults:
#   board-alpha   → -p 50078
#   board-beta    → -p 50025
#   board-gamma   → -p 50022
#   board-delta   → -p 50094
#   board-epsilon → -p 50026
#   board-zeta    → -p 50016
```

### Manual WSTUN API flow

```bash
# 1) Create service (port must NOT be 0)
curl -X POST http://{{VM_IP}}:8812/v1/services \
  -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"my-service","port":8080,"protocol":"TCP"}'

# 2) Enable on board → assigns public cloud port
curl -X POST http://{{VM_IP}}:8812/v1/boards/<BOARD_UUID>/services/my-service/action \
  -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \
  -d '{"action":"ServiceEnable"}'

# 3) Verify
curl -v http://{{VM_IP}}:<cloud_port>/
```

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

Open `http://<IP>/horizon/iot/federated_learning/` → Lab parameters → Create plugin **fl-client** → Inject on alpha/beta/gamma → **Start Flower server** → **Start all clients** → Live topology.

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

Single shared async plugin **`fl-client`** on each board; per-board JSON sets `csv_file` and `board_name` (`machine_1/2/3.csv` — CNC / conveyor / pump line).

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
