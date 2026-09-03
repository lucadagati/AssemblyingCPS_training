# Assembling Smart CPS — Hands-on Training Lab

[![GitHub](https://img.shields.io/badge/repo-AssemblyingCPS__training-blue)](https://github.com/lucadagati/AssemblyingCPS_training)

Modular training material for **Assembling Smart Cyber-Physical Systems** (Elsevier), aligned with the [AssemblingSmartCPS](https://github.com/AssemblingSmartCPS) GitHub organization.

**417 slides** across 10 English PPTX decks (Modules A–I). Slide URLs use placeholder `{{VM_IP}}` — replace with your lab host IP before presenting.

---

## For students (reproducibility)

1. **Clone this repo** and set your lab IP:
   ```bash
   git clone https://github.com/lucadagati/AssemblyingCPS_training.git
   cd AssemblyingCPS_training
   cp vm-ip.txt.example vm-ip.txt    # edit: your machine IP
   export S4T_LAB_HOST=$(cat vm-ip.txt)
   ```

2. **Clone book repos** and start Stack4Things:
   ```bash
   chmod +x scripts/clone-repos.sh && ./scripts/clone-repos.sh
   cd repos/ch13
   docker compose -f docker-compose.yml -f ../../patches/docker-compose.lab.yml up -d
   ```

3. **Validate** the environment:
   ```bash
   cd ../..
   ./validate/validate-all.sh
   ```

4. **Follow the lab** using:
   - [`HANDS_ON_COMMANDS.md`](HANDS_ON_COMMANDS.md) — copy-paste commands (EN)
   - [`GUIDA_SETUP_CORSISTI.md`](GUIDA_SETUP_CORSISTI.md) — setup guide (IT)
   - [`PORT_FORWARDING.md`](PORT_FORWARDING.md) — browser URLs
   - [`docs/BOOK_DIFFERENCES.md`](docs/BOOK_DIFFERENCES.md) — book vs lab (ports, Worker class, InfluxDB host)
   - `slides/Module*.pptx` — presentation decks (replace `{{VM_IP}}` in Find/Replace if needed)

### Core path deliverables (3 h)

| Module | Deliverable |
|--------|-------------|
| A | Screenshot: board **Active** in Horizon + `curl` HTTP 200 on `:8812` |
| B | HelloName Plugin Call output + optional Docker alpine JSON |
| C | InfluxDB rows in `environmental_data` measurement |

---

## For instructors (teaching)

| Resource | Purpose |
|----------|---------|
| [`slides/*.pptx`](slides/) | Ready-to-project decks with UML sequence diagrams |
| [`docs/MODULES.md`](docs/MODULES.md) | Module A–I map and prerequisites |
| [`docs/DEMO_VERIFICATION.md`](docs/DEMO_VERIFICATION.md) | Verified demo matrix |
| [`decks/*.py`](decks/) | Slide source — edit and regenerate |
| [`assets/`](assets/) | Horizon/LR screenshots + architecture PNGs |

### Regenerate slides after editing `decks/*.py`

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/generate_diagrams.py
.venv/bin/python generate_slides_modular_en.py
```

Optional full lab pipeline (deploy + validate): `./scripts/build-all.sh`

---

## Slide decks (`slides/`)

| File | Module | Topic |
|------|--------|-------|
| `00_Course_Map_EN.pptx` | Overview | Paths 3h / 6h / 9h |
| `ModuleA_Deploy_IOcloud_EN.pptx` | A | Ch.4 + Ch.13 deploy |
| `ModuleB_Plugin_Services_EN.pptx` | B | Ch.14 plugins |
| `ModuleC_IoT_Computation_EN.pptx` | C | Ch.15 environmental |
| `ModuleD_MultiBoard_EN.pptx` | D | Multi-board + fleet |
| `ModuleE_VirtualNetworking_EN.pptx` | E | Ch.5 VN (optional) |
| `ModuleF_WebServices_WoT_EN.pptx` | F | Ch.6 + Ch.14 WoT/WSTUN |
| `ModuleG_FederatedLearning_EN.pptx` | G | Ch.19 FL |
| `ModuleH_Blueprint_K3s_EN.pptx` | H | Ch.11 Blueprint |
| `ModuleI_FaaS_Deviceless_EN.pptx` | I | Ch.7 Deviceless |

See [slides/README.md](slides/README.md) for sequence diagram mapping.

---

## Configuration

| Item | Description |
|------|-------------|
| `vm-ip.txt` | Your lab IP (gitignored — use `vm-ip.txt.example`) |
| `S4T_LAB_HOST` | Override IP for scripts |
| `{{VM_IP}}` | Placeholder in slides and docs |
| Horizon | `admin` / `s4t` |
| Lightning-Rod SSH | `root` / `arancino` |

### Module F — Web Services / WoT demos

| Demo | Script | Description |
|------|--------|-------------|
| WoT Fritzing Lab | `experiments/webservices/run-wot-fritzing-demo.sh` | Interactive circuit (4 LEDs, servo, motor, relay, LCD, sensors) via WSTUN |
| Weather Station | `experiments/webservices/run-weather-demo.sh` | Rich dashboard: board sensors, trend chart, LED ctrl, Messina Open-Meteo data |
| SSH via S4T | `experiments/webservices/run-ssh-service.sh` | OpenSSH on all LR containers, forwarded via WSTUN (`root`/`arancino`) |

Horizon **Web Services** panel: `http://{{VM_IP}}/horizon/iot/` → Web Services (lists tunnels, embeds Thing UI).

---

## Book reference

[Assembling Smart CPS — Elsevier](https://shop.elsevier.com/books/assembling-smart-cyber-physical-systems/benomar/978-0-443-29837-0)

Companion repos: [github.com/AssemblingSmartCPS](https://github.com/AssemblingSmartCPS)

Future extensions: [docs/ROADMAP.md](docs/ROADMAP.md)

## License

Training material follows book companion repo licenses. ch13–ch19 repos are forks of MDSLab projects under their respective terms.
