# Book ↔ lab differences (verified)

| Topic | Book | Training lab | Mitigation |
|-------|------|--------------|------------|
| IoTronic API | `:8888` in some figures | `:8812` | Slides + HANDS_ON use :8812 |
| HelloName plugin class | `HelloNamePlugin` in upstream ch14 | Must be `Worker` | Use `ch14-fixed/plugins/synchronous/hello_name_plugin.py` |
| Ch.15 InfluxDB host | `localhost:8086` in upstream ch15 | `influxdb:8086` in Docker network | Use `ch15-lab/plugin_demo_lab.py` |
| Weather server port | `:8080` on hardware board | `:8088` inside LR compose image | `:8080` reserved in LR container; run-weather-demo.sh uses 8088 |
| Weather server UI | minimal HTML in book | full dark-theme dashboard (sensors, trend chart, LED ctrl, Open-Meteo) | `repos/ch14/demos/weather_web_server.py` — tabs: Board Sensors, Trend, LED, Open Data, WoT API |
| Web Services panel | book shows original empty panel | lab: panel replaced with functional WoT console | `patches/iotronic_ui_lab/`, `patches/horizon-enabled/_6080_iot_wot_panel.py` |
| Fritzing WoT demo | book describes concept | lab: interactive circuit (4 LEDs, servo, motor, relay, LCD, button, sensors) | `experiments/webservices/wot-fritzing/` — run with `run-wot-fritzing-demo.sh` |
| SSH on boards | physical board has SSH | LR containers: OpenSSH installed, root/arancino, forwarded via WSTUN | `experiments/webservices/run-ssh-service.sh` — service `ssh-remote` port 22 |
| WSTUN public URL | Designate DNS subdomain | `http://{{VM_IP}}:5000x/` | Same ServiceEnable API; different client URL |
| Horizon boards URL | varies in older docs | `/horizon/iot/` | Validated in capture_dashboards.py |
| FL datasets | book listing (`heart_*.csv`) | lab: `machine_*.csv` (predictive maintenance) | `generate_pm_datasets.py`; book CSVs kept in ch19 for reference |

All divergences are documented on **warn** slides and in demo verification scripts.
