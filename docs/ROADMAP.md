# Content extensions backlog (book → slides)

Items not yet fully covered in deck source. Regenerate after edits:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/generate_diagrams.py
.venv/bin/python generate_slides_modular_en.py
```

## High priority

| Topic | Book | Module | Notes |
|-------|------|--------|-------|
| Ch.4 latency migration study | Ch.4 §Performance impact | A | JMeter/FFT experiment figures |
| Crossplane CRD hands-on | Ch.11 | H | `kubectl apply` Board/Fleet CRD |
| CEP echo runtime demo | Ch.11 | H | Deploy echo pods on K3s |
| Ch.16 MACM / WSTUNServer deep dive | Ch.16 | F | Architecture beyond lab script |

## Medium priority

| Topic | Book | Module |
|-------|------|--------|
| Grafana hands-on dashboard | Ch.15 | C |
| CKAN open-data portal workflow | Ch.15 | C |
| Neutron L3 advanced features | Ch.5 | E |
| Dirichlet α NIID simulation detail | Ch.19 | G |
| PluginExec hands-on exercise | Ch.15 | C |

## Documentation

- Setup guide (IT): `GUIDA_SETUP.md`
- English commands: `HANDS_ON_COMMANDS.md`
- Module map and timing: `docs/MODULES.md`
