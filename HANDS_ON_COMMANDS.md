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

```bash
cd training/repos/ch19
pip install flwr torch pandas scikit-learn
FL_ROUNDS=2 python3 server.py
# separate terminal:
cd training && ./validate-lab-fl.sh
```

Or:

```bash
training/experiments/federated-learning/start-server.sh
```

Deploy `client.py` from ch19 as async plugin on each of 3 boards with `heart_1.csv`, `heart_2.csv`, `heart_3.csv`.

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
