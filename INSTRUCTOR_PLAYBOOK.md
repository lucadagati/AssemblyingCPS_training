# S4T Modular Training — Instructor Playbook

English modular curriculum for Longo + Merlino co-teaching on a **single lab VM** (`training/vm-ip.txt`).

## Training paths

| Path | Duration | Modules | Decks |
|------|----------|---------|-------|
| **Minimum** | 3 h | A + B + C | Course Map + Slot 1–3 EN |
| **Standard** | 6 h | Core + D + E + F | + ModuleD–F EN |
| **Full** | 9 h | Core + all extensions | + ModuleG–I EN |

Slides are tagged in speaker notes: `[CORE]`, `[EXT]`, `[ADV]` (timing only — co-teaching split in this playbook).

## Module timing matrix

| ID | Module | Lead | Minutes | Skip if short? |
|----|--------|------|---------|----------------|
| A | Deploy Ch.13 | Longo | 60 | — |
| B | Plugins Ch.14 | Longo | 60 | Docker plugin optional (−15) |
| C | Environmental Ch.15 | Merlino | 60 | — |
| D | Multi-board & Fleet | Longo | 45–60 | Fleet inject (−15) |
| E | Virtual Networking Ch.5 | Longo | 45–60 | WAgent log fallback (−20) |
| F | Web Services Ch.14 | Longo | 30–45 | — |
| G | Federated Learning Ch.19 | Merlino | 60–90 | Use `FL_ROUNDS=2` |
| H | Blueprint Ch.11 | Longo | 45–60 | K3s pre-provisioned only |
| I | FaaS / Deviceless Ch.7 | Merlino | 30–45 | Theory-only (−15) |

## Co-teaching split

- **Longo:** Modules A, B, D, E, F, H — infrastructure, deploy, plugins, networking, Blueprint.
- **Merlino:** Modules C, G, I — environmental dataflow, FL, FaaS contrast.
- **Both:** Course Map (5 min), wrap-up, Q&A.

Handoff after Slot 2 (Module B): confirm board Active + Hello plugin works before Merlino starts Module C.

## Pre-class checklist (instructor)

```bash
cd training/repos/ch13
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d
cd ../../
./validate-lab.sh                    # core 18/18
./validate-lab-multiboard.sh         # LR :1474–1476
./validate-lab-vn.sh
./validate-lab-fl.sh
.venv/bin/python scripts/generate_diagrams.py
.venv/bin/python scripts/capture_dashboards.py
.venv/bin/python generate_slides_modular_en.py
```

For **Module D/G:** also start extra LR containers:

```bash
docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d lightning-rod-2 lightning-rod-3
```

Onboard **three boards** (alpha/beta/gamma) before FL module.

## RAM gates (same VM)

| Combination | Rule |
|-------------|------|
| S4T + K3s (Module H) | ≥ 8 GB free recommended; run `experiments/blueprint/k3s-prereq.sh` |
| S4T + FL (Module G) | CPU-light with `FL_ROUNDS=2`; do **not** run with K3s |
| 9 h full day | Use **menu** — not all modules sequential if time tight |

## Book ↔ repo corrections (repeat on slide)

- API port: book `:8888` → lab `:8812`
- Boards URL: `/horizon/iot/` (not `/horizon/iot/boards/`)
- LR class name: must be `Worker` (use `training/ch14-fixed/`)
- Ch.15 InfluxDB host: `influxdb` not `localhost`
- ch19 datasets: `heart_1.csv`, `heart_2.csv`, `heart_3.csv` (not heart_0)

## Validation per module

| Script | Pass criteria |
|--------|---------------|
| `validate-lab.sh` | 18/18 core checks |
| `validate-lab-multiboard.sh` | LR :1474–1476 reachable; boards listed |
| `validate-lab-vn.sh` | Conductor + WSTUN + WAgent up |
| `validate-lab-wstun.sh` | WSTUN tunnel HTTP 200 on cloud port |
| `validate-lab-fl.sh` | ch19 artifacts + syntax OK |

## Slide decks

| File | Module |
|------|--------|
| `slides/00_Course_Map_EN.pptx` | Overview |
| `slides/ModuleA_Deploy_IOcloud_EN.pptx` | A |
| `slides/ModuleB_Plugin_Services_EN.pptx` | B |
| `slides/ModuleC_IoT_Computation_EN.pptx` | C |
| `slides/ModuleD_MultiBoard_EN.pptx` | D |
| `slides/ModuleE_VirtualNetworking_EN.pptx` | E |
| `slides/ModuleF_WebServices_WoT_EN.pptx` | F |
| `slides/ModuleG_FederatedLearning_EN.pptx` | G |
| `slides/ModuleH_Blueprint_K3s_EN.pptx` | H |
| `slides/ModuleI_FaaS_Deviceless_EN.pptx` | I |

Copy-paste command reference: [HANDS_ON_COMMANDS.md](HANDS_ON_COMMANDS.md).

## Troubleshooting quick reference

| Symptom | Action |
|---------|--------|
| 404 in slide images | Re-run `capture_dashboards.py`; never embed stale captures |
| Board not Active | Re-enter LR config; check Crossbar logs |
| Port 50052 conflict | `docker compose down`; retry `up -d` |
| FL client fails | Server running? Board Active? Correct CSV per board |
| K3s OOM | Stop FL or extra LR; `free -h` |
