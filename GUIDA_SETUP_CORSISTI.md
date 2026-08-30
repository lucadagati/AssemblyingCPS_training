# Guida di Setup — Laboratorio Stack4Things (3–9 ore)

**Corso:** Part II del libro *Assembling Smart Cyber-Physical Systems*  
**Core (3 h):** Cap. 13, 14, 15  
**Estensioni (6–9 h):** multi-board, Ch.5 VN, web services, Ch.19 FL, Ch.11 Blueprint, Ch.7 FaaS  
**Docenti:** Francesco Longo (Slot 1–2 + estensioni infra), Giovanni Merlino (Slot 3 + FL/FaaS)

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

### Onboarding virtual board

1. Horizon → IoT → **Create Board** → copiare board code
2. Aprire `http://<IP>:1474`
3. WAMP endpoint: `wss://crossbar:8181`
4. Incollare board code → Submit
5. Verificare stato **Active** in Horizon

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
| 8181 | Crossbar WAMP |
| 8812 | IoTronic Conductor API |

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
docker exec -it influxdb influx -username admin -password admin -execute "CREATE DATABASE secco"
```

### Plugin environmental (async)

- File: `training/repos/ch15/plugin_demo`
- Modalità: **async** (callable OFF)
- **Fix host InfluxDB** nel plugin se LR è in container:

```python
self.host = 'influxdb'   # stessa rete Docker s4t
```

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
USE secco;
SHOW MEASUREMENTS;
SELECT * FROM environmental_data LIMIT 5;
```

---

## E. Validazione automatica

```bash
chmod +x training/validate-lab.sh
./training/validate-lab.sh
./training/validate-lab-multiboard.sh
./training/validate-lab-vn.sh
./training/validate-lab-fl.sh
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

### Module E — Virtual Networking (Ch.5)

```bash
training/experiments/virtual-networking/attach-port.sh boards
training/experiments/virtual-networking/attach-port.sh list
```

### Module F — Web Services

Horizon: `http://<IP>/horizon/iot/webservices/`

### Module G — Federated Learning (Ch.19)

Richiede 3 board Active. Dataset: `heart_1.csv`, `heart_2.csv`, `heart_3.csv` in `training/repos/ch19`.

```bash
cd training/repos/ch19 && FL_ROUNDS=2 python3 server.py
```

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

---

## G. Teardown

```bash
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml down
# Aggiungere -v solo se si vogliono cancellare i volumi (dati persi)
```
