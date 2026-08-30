# Book ↔ lab differences (verified)

| Topic | Book | Training lab | Mitigation |
|-------|------|--------------|------------|
| IoTronic API | `:8888` in some figures | `:8812` | Slides + HANDS_ON use :8812 |
| HelloName plugin class | `HelloNamePlugin` in upstream ch14 | Must be `Worker` | Use `ch14-fixed/plugins/synchronous/hello_name_plugin.py` |
| Ch.15 InfluxDB host | `localhost:8086` in upstream ch15 | `influxdb:8086` in Docker network | Use `ch15-lab/plugin_demo_lab.py` |
| Weather server port | `:8080` on hardware board | `:8088` inside LR compose image | `:8080` reserved in LR container; run-weather-demo.sh uses 8088 |
| WSTUN public URL | Designate DNS subdomain | `http://{{VM_IP}}:5000x/` | Same ServiceEnable API; different client URL |
| Horizon boards URL | varies in older docs | `/horizon/iot/` | Validated in capture_dashboards.py |
| FL datasets | book listing | `heart_1.csv`, `heart_2.csv`, `heart_3.csv` | ch19 repo |

All divergences are documented on **warn** slides and in demo verification scripts.
