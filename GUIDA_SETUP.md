# Guida di Setup — Laboratorio Stack4Things (3–9 ore)

**Corso:** Part II del libro *Assembling Smart Cyber-Physical Systems*  
**Core (3 h):** Cap. 13, 14, 15  
**Estensioni (6–9 h):** multi-board, Ch.5 VN, web services, Ch.19 FL, Ch.11 Blueprint, Ch.7 FaaS  
**Setup:** lab VM + Docker Compose overlay (`patches/docker-compose.lab.yml`)

Vedi anche: [HANDS_ON_COMMANDS.md](HANDS_ON_COMMANDS.md) (EN) · [docs/MODULES.md](docs/MODULES.md)

---

## A. Requisiti hardware/software

| Requisito | Valore |
|-----------|--------|
| OS | Ubuntu 20.04+ o equivalente Linux |
| RAM | ≥ 4 GB (8 GB consigliati; 8+ GB se Module H K3s o Module G FL) |
| CPU | ≥ 2 vCPU |
| Docker Engine | 20+ |
| Docker Compose | v2 (`docker compose`) |
| Python | 3.8+ |
| Rete | Accesso GitHub + Docker Hub + Google Drive (CSV ch15) |

### Verifica ambiente

```bash
docker --version
docker compose version
groups | grep docker    # utente nel gruppo docker
git --version
python3 --version
free -h
```

### Clone repository

```bash
git clone https://github.com/AssemblingSmartCPS/ch13.git
git clone https://github.com/AssemblingSmartCPS/ch14.git
git clone https://github.com/AssemblingSmartCPS/ch15.git
# Estensioni (già in training/repos/ se usate slide modulari):
git clone https://github.com/AssemblingSmartCPS/ch05.git
git clone https://github.com/AssemblingSmartCPS/ch19.git
git clone https://github.com/AssemblingSmartCPS/ch11_xplane-provider-for-s4t.git
git clone https://github.com/AssemblingSmartCPS/ch11_s4t-k3s-deploy.git
```

Oppure usare i repo già in `training/repos/`.

---

## B. Slot 1 — Stack4Things (Cap. 13)

### Avvio stack (con overlay laboratorio)

```bash
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d
```

**Attesa:** 15–25 minuti al primo avvio (pull immagini, init DB, certificati CA).

### Verifica (porta corretta: 8812, non 8888 del libro)

```bash
HOST_IP=$(hostname -I | awk '{print $1}')
curl -s -o /dev/null -w "Conductor HTTP %{http_code}\n" "http://${HOST_IP}:8812/"
curl -s -o /dev/null -w "Horizon HTTP %{http_code}\n" "http://${HOST_IP}/"
curl -s -o /dev/null -w "LR UI HTTP %{http_code}\n" "http://${HOST_IP}:1474/"
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml ps
```

### Credenziali

**Lab host:** set your IP in `vm-ip.txt` (see `vm-ip.txt.example`) and `PORT_FORWARDING.md`.

| Servizio | URL | Username | Password |
|----------|-----|----------|----------|
| Horizon UI | `http://{{VM_IP}}/horizon` | admin | s4t |
| Lightning-Rod UI | `http://{{VM_IP}}:1474` | me | arancino |
| IoTronic API | `http://{{VM_IP}}:8812` | — | — |
| InfluxDB | `http://{{VM_IP}}:8086` | admin | admin |
| Grafana (lab) | `http://{{VM_IP}}:3000` | admin | admin |
| Metrics gateway | `http://{{VM_IP}}:8093` | — | Bearer token (auto) |

### Onboarding virtual board

1. Horizon → IoT → **Create Board** → copiare board code
2. Aprire `http://<IP>:1474`
3. WAMP endpoint: `wss://crossbar:8181`
4. Incollare board code → Submit
5. Verificare stato **Active** in Horizon

**Scorciatoia lab:** IoT → Boards → **Create LR Container** crea board + container Lightning-Rod (volumi e porta da 1480) e registra su Crossbar in automatico. Non tocca alpha–zeta. Login LR: `me` / `arancino`.

### Porte esposte

| Porta | Servizio |
|-------|----------|
| 80 | Horizon UI |
| 1474 | Lightning-Rod config (board-alpha) |
| 1475 | Lightning-Rod-2 (board-beta, overlay lab) |
| 1476 | Lightning-Rod-3 (board-gamma, overlay lab) |
| 5000 | Keystone |
| 8080 | WSTUN |
| 8086 | InfluxDB (overlay lab) |
| 8093 | Metrics gateway (overlay lab) |
| 3000 | Grafana (overlay lab) |
| 8181 | Crossbar WAMP |
| 8812 | IoTronic Conductor API |
| 80 (+ `/lab-ws/<port>/`) | Horizon + proxy demo WoT/WSTUN (indipendente dall'IP Tailscale) |

Vedi anche: [`docs/LAB_NETWORK_ACCESS.md`](docs/LAB_NETWORK_ACCESS.md) · [`docs/CHANGELOG.md`](docs/CHANGELOG.md) · [`lab-ops/README.md`](lab-ops/README.md)

---

## C. Slot 2 — Plugin (Cap. 14)

### Plugin HelloName (sync) — classe `Worker` obbligatoria

Usare il file corretto: `training/ch14-fixed/plugins/synchronous/hello_name_plugin.py`

```python
from iotronic_lightningrod.modules.plugins import Plugin
from oslo_log import log as logging
LOG = logging.getLogger(__name__)

class Worker(Plugin.Plugin):
    def __init__(self, uuid, name, q_result, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)
    def run(self):
        person_name = self.params.get('name', 'User')
        message = f"Hello {person_name}"
        LOG.info(message)
        self.q_result.put(message)
```

- Horizon → Plugins → **Create Plugin**
- Flag **callable** = ON (sync)
- Plugin Call JSON: `{"name": "Messina"}`

### Docker lifecycle plugin

**Prerequisito:** overlay lab monta `/var/run/docker.sock` in lightning-rod.

PluginCall JSON (run):

```json
{
  "operation": "run",
  "image": "alpine",
  "container_name": "test_alpine",
  "command": "echo Hello from plugin!",
  "auto_remove": false
}
```

Codice plugin: `training/repos/ch14/docker_lifecycle_plugin.py` o listing Cap. 14 lst:plugin.

---

## D. Slot 3 — Environmental publisher (Cap. 15)

### Stack metriche cloud (lab)

Con l'overlay lab, i plugin **non scrivono più direttamente** su InfluxDB con credenziali admin. Il flusso è:

1. **IoT → Plugins → Start** — **Enable cloud metrics** is on by default (for EnvironmentalDemo credentials are always injected)
2. Horizon provisiona stream + token via `metrics-gateway:8093`
3. Il plugin usa `MetricsWriter` (`s4t_metrics.py` montato su LR in `/opt/lab/`)
4. **IoT → Metrics** → dashboard Grafana embedded + lista stream

Database Influx: `s4t_iot` (non più `secco` nel lab aggiornato).

### InfluxDB (incluso in overlay lab)

Se avviato separatamente:

```bash
docker run -d --name=influxdb --restart unless-stopped -p 8086:8086 \
  -e INFLUXDB_HTTP_AUTH_ENABLED=true \
  -e INFLUXDB_ADMIN_USER=admin \
  -e INFLUXDB_ADMIN_PASSWORD=admin \
  -v influxdb_data:/var/lib/influxdb influxdb:1.8
```

```bash
docker exec -it influxdb influx -username admin -password admin -execute "CREATE DATABASE s4t_iot"
```

### Plugin environmental (async)

- File lab: `training/ch15-lab/plugin_demo_lab.py`
- Modalità: **async** (callable OFF)
- **Start** injecta sempre i params metrics per EnvironmentalDemo:

```json
{
  "metrics_url": "http://metrics-gateway:8093/v1/metrics/write",
  "metrics_token": "<token>",
  "metrics_stream": "environmental_data"
}
```

Senza `metrics_url`/`metrics_token` il plugin **si ferma subito** (non gira a vuoto).

### Dipendenze nel container LR

```bash
docker exec -it lightning-rod pip install influxdb pandas requests
docker exec -it lightning-rod mkdir -p /opt/data
```

### Validazione dati

```bash
docker exec -it influxdb influx -username admin -password admin
```

```sql
USE s4t_iot;
SHOW MEASUREMENTS;
SELECT * FROM environmental_data LIMIT 5;
```

### Panel IoT Metrics + Grafana

- Horizon: **IoT → Metrics** (`/horizon/iot/iot_metrics/`)
- Grafana diretto: `http://{{VM_IP}}:3000`
- Proxy Horizon (iframe): `http://{{VM_IP}}/horizon/metrics-live/`

```bash
curl http://{{VM_IP}}:8093/health
python3 training/experiments/metrics/verify-metrics-lab.py
./training/validate-lab-metrics.sh
```

---

## E. Validazione automatica

```bash
chmod +x training/validate-lab.sh
./training/validate-lab.sh
./training/validate-lab-multiboard.sh
./training/validate-lab-vn.sh
./training/validate-lab-fl.sh
./training/validate-lab-metrics.sh
```

---

## E2. Moduli estensione (6–9 h)

### Module D — Multi-board (3 LR)

```bash
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d lightning-rod-2 lightning-rod-3
training/experiments/multiboard/check-endpoints.sh
```

Board: `board-alpha` → :1474, `board-beta` → :1475, `board-gamma` → :1476

**IoT → Fleets** (`/horizon/iot/fleets/`):

1. **Create Fleet** — nome, descrizione e selezione multipla delle board online
2. Apri il **dettaglio fleet** → tab **Members** → **Manage members** per aggiungere/rimuovere board
3. Tab **Operations** — **Inject / Start / Stop / Call / Remove plugin** su **tutte** le board della fleet in parallelo (stesse operazioni del pannello Plugins, pre-filtrate sulla fleet)

Esempio Module D: fleet con alpha/beta/gamma → **Inject** plugin HelloName → **Call** con `{"name": "fleet-demo"}`.

### Module E — Virtual Networking (Ch.5)

```bash
training/experiments/virtual-networking/attach-port.sh boards
training/experiments/virtual-networking/attach-port.sh list
```

### Module F — Web Services

Horizon: `http://<IP>/horizon/iot/webservices/`

La tabella **Web Services** puo restare vuota (*No items to display*) finche non si abilita il Web Services Manager su una board (demo: `training/experiments/webservices/setup-wstun-demo.py`).

### Module G — Federated Learning (Ch.19)

Architettura come nel libro: **server Flower sulla VM cloud**, **3 board client** via plugin async Lightning-Rod (non una board come server).

Richiede 3 board **online** (`board-alpha`, `board-beta`, `board-gamma`). Il pannello **Boards** (`/horizon/iot/`, non `/horizon/iot/boards/`) puo elencare anche altre board registrate (delta/epsilon/zeta): il lab FL usa solo alpha/beta/gamma.

Due scenari demo via plugin cloud:
- **fl-client-heart** — heart_1/2/3.csv (Cap. 19)
- **fl-client-pm** — machine_1/2/3.csv (predictive maintenance)

Dataset in `training/repos/ch19` (generati con `generate_pm_datasets.py`).

#### Setup una tantum (shell sulla VM)

```bash
cd training

# Dipendenze flwr/torch + CSV sui 3 container Lightning-Rod
./experiments/federated-learning/install-fl-on-boards.sh

# Pannello Horizon nativo + servizio fl-control (:8091) + proxy live topology
./experiments/federated-learning/setup-fl-horizon.sh

# Registra fl-client-heart + fl-client-pm e inietta sulle board online
./experiments/federated-learning/setup-fl-demo-plugins.sh
```

#### Lab da Horizon (flusso consigliato)

Apri **IoT → Federated Learning**: `http://<IP>/horizon/iot/federated_learning/`

1. **Parameters** (opzionale) — round, host/port server e dashboard → **Save**
2. **Select plugin** — `fl-client-heart` o `fl-client-pm` → aggiorna scenario/parametri UI (**non** avvia automaticamente il run)
3. **Start server** — avvia/riavvia Flower + client alpha/beta/gamma
4. **Inject on all boards** — se i plugin non sono ancora sulle edge board
5. **Start all clients** — avvia solo i client edge (il server deve essere gia in esecuzione)
6. **Live topology** — iframe su `/horizon/fl-live/?embed=1`

Porte lab: Flower gRPC **8087** (WSTUN usa :8080), dashboard **8090**, control API **8091**.

**Note IoT dashboard:** **Fleets** si gestisce dal pannello IoT (create + Members + Operations). Menu Horizon in inglese di default sul lab VM. Plugin Call: i log `LOG.info` compaiono nel pannello log board (file LR, non solo `docker logs`).

**Demo WoT (URL indipendenti dall'IP Tailscale):** `http://<IP>/lab-ws/<porta>/` — vedi [`docs/LAB_NETWORK_ACCESS.md`](docs/LAB_NETWORK_ACCESS.md) e [`PORT_FORWARDING.md`](PORT_FORWARDING.md).

CLI alternativa (debug): `./experiments/federated-learning/fl-server-ctl.sh start|stop|restart`

Se Horizon mostra **"Unable to retrieve boards list"**:

```bash
./scripts/fix-iotronic-wampagents.sh
```

### Lab ops — board manuali + accesso rete

```bash
cd training/lab-ops
./00-verify-demo.sh
./04-list-lr-dashboards.sh
BOARD_NAME=lab-edge-1 ./01-run-manual-lr.sh   # installa anche sshd in-container (no porta host)
```

Registrazione: WAMP `wss://crossbar:8181` (solo container Docker). Board **esterne** su Tailscale: `/etc/hosts` → VM IP per `crossbar` / `iotronic-wstun`, CA lab, vedi `docs/LAB_NETWORK_ACCESS.md`.

Create Fleet: se compare *Unable to create fleet* / `uuid` su `None`, l'entrypoint UI applica già il `return` su `fleet_create`. Prima di Delete Fleet, scollega i membri (FK su `boards.fleet`).

### Module H — Blueprint (Ch.11)

```bash
training/experiments/blueprint/k3s-prereq.sh   # RAM ≥ 8 GB
# Non eseguire insieme a Module G sulla stessa VM
```

---

## F. Correzioni libro ↔ repo (importante)

1. **Cap. 13 riga 229:** il libro indica porta `8888`; il repo ch13 usa **`8812`**
2. **Cap. 14 repo ch14:** `hello_name_plugin.py` usa `HelloNamePlugin` invece di `Worker` — usare `ch14-fixed/`
3. **Cap. 13 compose:** immagine LR placeholder `@sha256:<resolved-image-digest>` — overlay usa `mdslab/lrod:compose`
4. **Cap. 15:** `localhost:8086` non raggiunge InfluxDB da LR container — usare hostname `influxdb`
5. **Cap. 19 riga 727:** rimanda a Cap. 12 per install S4T; procedura corretta è **Cap. 13**
6. **Cap. 19 FL:** server Flower sulla VM host; lab con plugin **`fl-client-heart`** (heart_*.csv) o **`fl-client-pm`** (machine_*.csv). Porta lab **8087**. Dataset PM: `machine_*.csv` (estensione lab; libro usa heart_*.csv)

---

## G. Teardown

```bash
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml down
# Aggiungere -v solo se si vogliono cancellare i volumi (dati persi)
```
