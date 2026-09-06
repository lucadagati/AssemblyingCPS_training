# Assembling Smart CPS — Hands-on Training Lab

[![GitHub](https://img.shields.io/badge/repo-AssemblyingCPS__training-blue)](https://github.com/lucadagati/AssemblyingCPS_training)

Modular training material for **Assembling Smart Cyber-Physical Systems** (Elsevier), aligned with the [AssemblingSmartCPS](https://github.com/AssemblingSmartCPS) GitHub organization.

**417 slides** across 10 English PPTX decks (Modules A–I). Slide and handout URLs use the placeholder `{{VM_IP}}` — replace with your lab host address before presenting.

Lab networking and external boards: [`docs/LAB_NETWORK_ACCESS.md`](docs/LAB_NETWORK_ACCESS.md) · change history: [`docs/CHANGELOG.md`](docs/CHANGELOG.md).

---

## For students (reproducibility)

1. **Clone this repo** and set your lab host IP:
   ```bash
   git clone https://github.com/lucadagati/AssemblyingCPS_training.git
   cd AssemblyingCPS_training
   cp vm-ip.txt.example vm-ip.txt    # edit: address used to reach the lab host
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
   - [`GUIDA_SETUP.md`](GUIDA_SETUP.md) — setup guide (IT)
   - [`PORT_FORWARDING.md`](PORT_FORWARDING.md) — browser URLs
   - [`docs/LAB_NETWORK_ACCESS.md`](docs/LAB_NETWORK_ACCESS.md) — ports and external boards
   - [`docs/BOOK_DIFFERENCES.md`](docs/BOOK_DIFFERENCES.md) — book vs lab
   - [`lab-ops/`](lab-ops/) — manual Lightning-Rod create/destroy helpers
   - `slides/Module*.pptx` — decks (Find/Replace `{{VM_IP}}` if needed)

### Core path deliverables (3 h)

| Module | Deliverable |
|--------|-------------|
| A | Screenshot: board **Active** in Horizon + `curl` HTTP 200 on `:8812` |
| B | HelloName Plugin Call output + optional Docker alpine JSON |
| C | InfluxDB rows in `environmental_data` measurement |

### Demo URLs

Use the same host as Horizon plus the published WSTUN port:

```text
http://{{VM_IP}}:50006/   # wot-fritzing (example)
http://{{VM_IP}}/horizon  # Horizon
```

---

## For instructors (teaching)

| Resource | Purpose |
|----------|---------|
| [`slides/*.pptx`](slides/) | Ready-to-project decks with UML sequence diagrams |
| [`docs/MODULES.md`](docs/MODULES.md) | Module A–I map and prerequisites |
| [`docs/DEMO_VERIFICATION.md`](docs/DEMO_VERIFICATION.md) | Verified demo matrix |
| [`docs/CHANGELOG.md`](docs/CHANGELOG.md) | Lab overlay history |
| [`docs/LAB_NETWORK_ACCESS.md`](docs/LAB_NETWORK_ACCESS.md) | Lab host ports / external boards |
| [`decks/*.py`](decks/) | Slide source — edit and regenerate |
| [`assets/`](assets/) | Horizon/LR screenshots + architecture PNGs |
| [`lab-ops/`](lab-ops/) | Manual LR board create / port map |

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
| `vm-ip.txt` | Lab host IP for scripts (gitignored — use `vm-ip.txt.example`) |
| `S4T_LAB_HOST` | Override IP for scripts |
| `{{VM_IP}}` | Placeholder in slides and docs |
| Horizon | `admin` / `s4t` |
| Lightning-Rod | `me` / `arancino` |
| LR container SSH (`lab-ops`) | `root` / `arancino` (inside container only; no host port) |

---

## Book reference

[Assembling Smart CPS — Elsevier](https://shop.elsevier.com/books/assembling-smart-cyber-physical-systems/benomar/978-0-443-29837-0)

Companion repos: [github.com/AssemblingSmartCPS](https://github.com/AssemblingSmartCPS)

Future extensions: [docs/ROADMAP.md](docs/ROADMAP.md)

## License

Training material follows book companion repo licenses. ch13–ch19 repos are forks of MDSLab projects under their respective terms.
