"""Module C — Slot 3: IoT-hosted computation (Ch.15). Hand-authored theory + demo slides."""


def slides() -> list:
    return [
        ("title", "IoT-hosted Computation & Smart-City Services",
         "Module C — IoT-hosted Computation · Ch.15 · 60 min\nLab VM: {{VM_IP}}",
         "Assembling Smart CPS · Part II"),

        ("section", "Chapter 15 overview", "From middleware to urban observability"),

        ("theory", "Chapter 15 scope — abstract and positioning", [
            "Chapter 15 moves from platform deployment (Ch.13) and edge plugins (Ch.14) to an observable urban service.",
            "Environmental monitoring demonstrates an end-to-end workflow: edge acquisition → time-series storage → dashboards.",
            "The chapter frames IoT nodes as software-defined infrastructure — programmable and remotely managed assets.",
            "Chapter 15 emphasizes design principles, three-layer architecture, and real smart-city replication.",
            "The TOO(L)SMART national project provides two deployment models validated across five Italian pilot cities.",
            "Today's lab reproduces the core data path with CSV replay instead of physical sensors on Raspberry Pi hardware.",
        ], "Ch.15 abstract · IoT-hosted computation"),

        ("content", "Module C — 60-minute timeline", [
            "0–12 min  — Design principles, firmware vs plugins, three-layer architecture",
            "12–18 min — Environmental publisher theory, JSON schema, InfluxDB networking",
            "18–38 min — HANDS-ON: deploy async environmental_data plugin on Active board",
            "38–52 min — Query InfluxDB, validate environmental_data measurement rows",
            "52–60 min — TOO(L)SMART Turin vs VM-bundle models + 3-hour course wrap-up",
        ]),

        ("content", "Learning objectives and deliverables", [
            "Understand the three-layer architecture: orchestration, execution, and application/storage.",
            "Deploy the async environmental_data plugin writing CSV rows to InfluxDB every 30 seconds.",
            "Query time-series data with Influx CLI — deliverable: rows visible in environmental_data.",
            "Relate the lab demo to TOO(L)SMART smart-city deployment models in Turin and plug-and-play cities.",
            "Horizon login: {{HZ_CRED}} · InfluxDB ping: http://{{VM_IP}}:8086/ping · LR UI: {{LR_CRED}} at :1474.",
        ]),

        ("section", "Design principles", "Firmware vs plugins · modular edge architecture"),

        ("theory", "Firmware vs plugin paradigm — why plugins win (Ch.15 intro)", [
            "Traditional firmware embeds logic in flash — updates require physical access, truck rolls, or risky OTA reflashing.",
            "Firmware changes are slow, expensive, and tightly coupled to specific hardware board revisions and pin maps.",
            "Stack4Things plugins deploy at runtime — IoTronic orchestrates upload, inject, start, update, and removal remotely.",
            "Edge logic can iterate daily during a smart-city pilot without touching device flash or rebooting the OS.",
            "The plugin model aligns with I/Ocloud virtualization from Chapter 4 — sensors become callable software functions.",
            "Chapter 15 environmental publisher is the canonical async plugin proving continuous urban data acquisition.",
        ], "Ch.15 introduction · firmware vs plugin"),

        ("theory", "Firmware vs plugin — operational comparison", [
            "Firmware rollback requires backup partitions or JTAG recovery — plugins rollback by re-injecting prior repository version.",
            "Firmware testing cycles span hardware QA labs; plugin testing uses the same Horizon inject flow as production.",
            "Multiple plugins coexist on one board — environmental, Docker, HelloName — without reflashing monolithic firmware.",
            "Plugin interrupt and remove cleanly stop background loops and release Python resources on Lightning-Rod.",
            "Production Raspberry Pi stations run the same Worker class as today's LR container — only the data source changes.",
            "Physical sensors replace CSV rows; InfluxDB host, measurement name, and 30-second interval stay identical.",
        ], "Ch.15 · software-defined edge nodes"),

        ("theory", "Design principles — modular plugin architecture (Ch.15)", [
            "Modular plugin-based architecture enforces clear separation of concerns across cloud, edge, and storage tiers.",
            "Orchestration (IoTronic) owns lifecycle, multi-tenancy, REST APIs, and Horizon dashboard operations.",
            "Execution (Lightning-Rod) owns Worker loading, WAMP messaging, oslo_log emission, and local I/O access.",
            "Application logic lives inside the plugin — CSV parsing, timestamp assignment, InfluxDB write_points calls.",
            "External time-series storage (InfluxDB) keeps the edge lightweight — no heavy database on constrained boards.",
            "Security sandboxing limits plugin access to declared resources; extensibility adds new Workers without platform forks.",
        ], "Ch.15 § design principles"),

        ("theory", "Design principles — state, fault tolerance, observability", [
            "State management uses last_index.state on disk so the plugin resumes CSV replay after restart or crash.",
            "Fault tolerance: failed InfluxDB writes log errors via oslo_log but the loop continues to next row when possible.",
            "Structured logging spans execution layer → centralized IoTronic logs in production deployments.",
            "Lightweight edge plus external DB mirrors smart-city reality — Pi acquisition, cloud-scale storage and Grafana.",
            "Open standards throughout: JSON data points, WAMP control, Docker Compose lab stack, CKAN open-data portals.",
            "These principles directly enabled TOO(L)SMART replication from Turin reference to four plug-and-play cities.",
        ], "Ch.15 § design principles · fault tolerance"),

        ("theory", "Security and sandboxing (Ch.15)", [
            "Running arbitrary plugin code requires sandboxing, access control, and signature verification.",
            "Tenant isolation in IoTronic prevents one operator from injecting plugins on another's boards.",
            "LR executes Python Workers with OS-level boundaries — production adds resource limits and auditing.",
            "Digital signatures on uploaded plugins ensure integrity before fleet-wide rollout.",
            "Security-by-design aligns with GDPR and smart-city procurement requirements in TOO(L)SMART.",
            "Lab scope: trusted training environment — production deployments enforce stricter policies.",
        ], "Ch.15 § design principles · security sandboxing"),

        ("theory", "PluginExec — local plugin testing (Ch.15)", [
            "PluginExec is a command-line tool that simulates plugin execution on the board before cloud inject.",
            "Developers debug Worker.run() locally with mock params and q_result — faster iteration cycle.",
            "Reduces failed inject cycles during smart-city pilot deployments with hundreds of boards.",
            "Same Worker class used in PluginExec and IoTronic inject — behaviour matches production.",
            "Workflow: write → PluginExec test → upload repository → inject → Start on Active board.",
            "Book abstract positions PluginExec as accelerator for plugin-based urban services.",
        ], "Ch.15 abstract · PluginExec tool"),

        ("theory", "Book vs lab environmental JSON schema (Ch.15)", [
            "Book measurement environmental_data includes full air-quality set: CO, CO2, O3, NO2, VOC.",
            "Lab CSV subset focuses on Temperature, Humidity, PM2.5, PM10 — sufficient for InfluxDB demo.",
            "Tags: host, source · timestamp: ISO format assigned per row in plugin_demo run loop.",
            "Same InfluxDB line protocol and database name secco — only field cardinality differs.",
            "Production Raspberry Pi stations use identical schema with live sensor drivers instead of CSV.",
            "Tables tab:meteorological and tab:airquality in book define full pilot-city parameter lists.",
        ], "Ch.15 · tab:meteorological · tab:airquality · plugin_demo listing"),

        ("theory", "LoRaWAN edge-collector-cloud path (Ch.15)", [
            "TOO(L)SMART stations often use LoRaWAN: many end nodes → few gateway collectors → cloud.",
            "Gateway placement at urban zone edges mitigates path loss — uniform coverage in dense cities.",
            "S4T LR on collector node runs environmental async plugin — same architecture as today's lab.",
            "LoRaWAN handles low-power wide-area links; InfluxDB and Grafana remain in application tier.",
            "Lab CSV replay simulates collector-acquired rows — swap CSV for LoRa decoder output in production.",
            "Book cites empirical LoRaWAN deployment studies for Turin and other pilot municipalities.",
        ], "Ch.15 § Environmental monitoring · LoRaWAN architecture"),

        ("section", "Three-layer architecture", "Orchestration · execution · application"),

        ("theory", "Orchestration layer — IoTronic cloud control plane", [
            "IoTronic Conductor exposes REST API on port 8812 and Horizon IoT panels for operators and tenants.",
            "It maintains the plugin repository, board registry, injection mappings, and fleet group definitions.",
            "Start, Stop, Interrupt, and Plugin Call commands traverse RabbitMQ and Crossbar WAMP to reach Lightning-Rod.",
            "Multi-tenant isolation follows OpenStack Keystone — each city project sees only its boards and plugins.",
            "Centralized logging aggregation receives LR log streams for cross-fleet troubleshooting without SSH.",
            "Chapter 13 deployed this layer in Module A; Chapter 15 adds async plugin activation on top of it.",
        ], "Ch.15 · fig:chap15 architecture · orchestration layer"),

        ("theory", "Execution layer — Lightning-Rod edge agent", [
            "Lightning-Rod connects the board to IoTronic via WAMP over wss://crossbar:8181 inside the Docker s4t network.",
            "Plugin Manager loads the Worker class, sets self._is_running for async loops, and routes self.params.",
            "oslo_log LOG.info and LOG.error emit structured messages consumed locally and forwarded centrally in production.",
            "LR container in the lab simulates a physical board — same agent binary used on Raspberry Pi edge nodes.",
            "pip-installed dependencies (influxdb, pandas, requests) must exist inside LR before environmental plugin starts.",
            "Network hostname influxdb resolves on s4t bridge — localhost inside LR does not reach the InfluxDB container.",
        ], "Ch.15 · execution layer · Lightning-Rod"),

        ("theory", "Application layer — plugin, storage, visualization", [
            "The environmental Worker reads CSV rows, assigns UTC timestamps, and writes InfluxDB points every 30 seconds.",
            "InfluxDB 1.8 stores measurement environmental_data in database secco with admin credentials in the lab overlay.",
            "Grafana dashboards (grafana.json in ch15 repo) visualize air-quality and meteorological fields for operators.",
            "CKAN data portals publish open datasets to citizens — the TOO(L)SMART public-facing tier above raw time-series.",
            "Node-RED flows in full Turin deployment orchestrate alerts and integrations beyond simple storage.",
            "Lab validates the plugin → InfluxDB path; Grafana and CKAN are previewed as production application tier.",
        ], "Ch.15 · application layer · InfluxDB · Grafana · CKAN"),

        ("image", "Environmental dataflow (diagram)",
         "diagrams/environmental-dataflow.png",
         "CSV → async Worker → InfluxDB (host=influxdb) → optional Grafana · Ch.15 pipeline"),

        ("section", "Environmental data publisher", "Async plugin · Ch.15 listing"),

        ("theory", "Environmental publisher — purpose and data source", [
            "The environmental data publisher simulates a continuous real-time sensor stream by replaying CSV rows.",
            "Each row receives a fresh UTC timestamp at publish time — decoupling historical data from wall-clock acquisition.",
            "In production, Raspberry Pi boards with I2C, SPI, or GPIO sensors replace CSV iloc iteration with live reads.",
            "The plugin is asynchronous: Callable = OFF, activated with Start, runs until Stop or dataset exhaustion.",
            "Repository: github.com/AssemblingSmartCPS/ch15 · lab file: training/ch15-lab/plugin_demo_lab.py.",
            "Measurement name written to InfluxDB: environmental_data — the validation target for today's deliverable.",
        ], "Ch.15 · environmental data publisher listing"),

        ("theory", "Environmental publisher — initialization and CSV handling", [
            "On __init__, the Worker ensures /opt/data exists and downloads structured_time_series_v2.csv if missing.",
            "pandas reads the CSV, parses the time column, and fills NaN with zero for safe float conversion.",
            "InfluxDBClient connects with host, port 8086, username admin, password admin, database secco.",
            "create_database ensures secco exists before the run loop begins publishing points.",
            "load_last_index reads last_index.state to resume from the last successfully written row after restart.",
            "Dependencies: influxdb, pandas, requests — install inside LR container before plugin Start.",
        ], "Ch.15 · plugin __init__ · CSV download from Google Drive"),

        ("theory", "Environmental publisher — generate_data_point structure", [
            "Each InfluxDB point has measurement environmental_data, tags host and source, UTC time, and numeric fields.",
            "Tags identify the station name and source file — enabling multi-station queries in Grafana and CKAN.",
            "Fields include meteorological and air-quality metrics parsed via safe_float from CSV columns.",
            "safe_float strips quotes and returns 0.0 on parse failure — preventing one bad cell from crashing the loop.",
            "write_points sends a single-element list; success logs Row N sent via oslo_log for traceability.",
            "After each write, last_index increments and persists to last_index.state for fault-tolerant resume.",
        ], "Ch.15 · generate_data_point · listing"),

        ("section", "InfluxDB and networking", "Lab overlay · LR container connectivity"),

        ("theory", "InfluxDB in the lab stack — deployment and access", [
            "Training overlay docker-compose.lab.yml adds influxdb:1.8 on Docker network s4t alongside S4T services.",
            "Host port 8086 maps to InfluxDB HTTP API — curl http://{{VM_IP}}:8086/ping returns 204 when healthy.",
            "Default credentials: admin / admin — enabled via INFLUXDB_HTTP_AUTH_ENABLED in compose environment.",
            "Database secco stores environmental time-series; _internal is InfluxDB system metadata.",
            "Interactive shell: docker exec -it influxdb influx -username admin -password admin",
            "Book also documents standalone docker run influxdb:1.8 for non-compose deployments.",
        ], "Ch.15 · InfluxDB Docker deployment · lab overlay"),

        ("theory", "LR → InfluxDB networking — why localhost fails", [
            "Default ch15 plugin_demo uses host localhost:8086 — this FAILS inside the Lightning-Rod container.",
            "localhost inside LR refers to the LR container itself, where no InfluxDB process listens on 8086.",
            "Fix: self.host = 'influxdb' — Docker embedded DNS on network s4t resolves the InfluxDB service name.",
            "Lab file training/ch15-lab/plugin_demo_lab.py already applies this fix — use it, not raw repo plugin_demo.",
            "Do NOT use host gateway IP (172.17.0.1) — fragile across Docker restarts and compose network changes.",
            "Same hostname pattern as wss://crossbar:8181 from Module A — always use s4t service names inside containers.",
        ], "Ch.15 · container networking · critical lab fix"),

        ("theory", "InfluxDB data model — measurements, tags, fields, time", [
            "InfluxDB 1.x line protocol: measurement, tag set, field set, and timestamp define each point.",
            "Tags (host, source) are indexed strings — use for GROUP BY station in queries and Grafana templates.",
            "Fields (Temperature, PM25, Humidity, …) hold numeric values — the actual sensor readings.",
            "Timestamps are UTC ISO format assigned at publish time in the lab CSV replay scenario.",
            "Retention policies and continuous queries can downsample raw 30-second data for long-term storage.",
            "SHOW MEASUREMENTS and SELECT * FROM environmental_data LIMIT 5 validate successful plugin writes.",
        ], "Ch.15 · InfluxDB time-series concepts"),

        ("section", "JSON schema and execution loop", "Data model · async run() method"),

        ("theory", "JSON data model — meteorological fields (Ch.15)", [
            "Temperature records ambient air temperature in degrees Celsius from the CSV replay or live sensor.",
            "Humidity captures relative humidity percentage — critical for comfort and mold-risk urban indicators.",
            "Wind_speed and Wind_direction describe horizontal flow magnitude and compass bearing.",
            "Pressure reports barometric pressure — useful for weather trend analysis across station networks.",
            "Precipitation accumulates rainfall depth — key hydrological input for smart-city flood early warning.",
            "Gust, Light, and UVI extend the meteorological profile for comprehensive station dashboards.",
        ], "Ch.15 Table · meteorological JSON fields"),

        ("theory", "JSON data model — air quality and particulate fields", [
            "PM25, PM10, and PM100 measure particulate matter at 2.5, 10, and 100 micrometer thresholds.",
            "Part03 through Part100 provide size-binned particle count distributions for detailed air-quality studies.",
            "These fields map directly to EU air-quality index reporting used in TOO(L)SMART open-data portals.",
            "CO, CO2, O3, NO2, and VOC appear in the book schema for full stations — lab CSV includes PM and meteo subset.",
            "lat, lon, and alt tags geolocate each reading for map overlays in Grafana and CKAN.",
            "Consistent field naming across cities enabled TOO(L)SMART Model 2 plug-and-play VM replication.",
        ], "Ch.15 Table · air quality JSON · lines 633–664"),

        ("theory", "JSON data model — tags, timestamps, and open-data alignment", [
            "Tag host identifies the station name from CSV name column — e.g. distinct Turin district stations.",
            "Tag source_file traces provenance to the original CSV segment for audit and debugging.",
            "UTC timestamps on each point align Grafana time axes across time zones in multi-city deployments.",
            "JSON structure in the book listing is the contract CKAN harvesters and Grafana datasources expect.",
            "Lab plugin assigns datetime.utcnow().isoformat() per row — simulating live acquisition cadence.",
            "Production stations use sensor read time or NTP-synchronized board clock for the time field.",
        ], "Ch.15 · JSON structure listing · open-data contract"),

        ("theory", "Execution loop — run() method step by step (Ch.15)", [
            "run() logs plugin start, InfluxDB target host:port, database name, and resume index.",
            "while self._is_running and self.last_index < len(self.df): fetches the current CSV row by iloc.",
            "generate_data_point(row) builds the InfluxDB dict with measurement, tags, time, and fields.",
            "client.write_points([data_point]) sends the point; success logs Row N sent, failure logs exception.",
            "last_index increments; save_last_index persists progress to /opt/data/last_index.state.",
            "time.sleep(30) waits 30 seconds between publications — matching book cadence and lab timing.",
            "Loop exits when dataset complete or plugin stopped; logs Dataset complete or plugin stopped.",
        ], "Ch.15 · async run() listing"),

        ("theory", "Execution loop — timing, Start vs Plugin Call, lifecycle", [
            "Async plugins never use Plugin Call for each row — Start launches the entire loop until Stop or Interrupt.",
            "Start the plugin by minute 18 of the hands-on block to accumulate rows before Module C wrap-up at minute 52.",
            "Thirty-second interval means ~2 rows per minute — plan query validation accordingly after 5+ minutes running.",
            "Interrupt sets _is_running False — preferred graceful stop before plugin code update or board maintenance.",
            "Remove injection only after Stop — avoids orphaned write loops holding InfluxDB client connections.",
            "Same seven-step lifecycle from Ch.14 applies: create, inject, start, monitor, update, interrupt, remove.",
        ], "Ch.15 · plugin activation · Ch.14 lifecycle"),

        ("section", "Hands-on — InfluxDB and async plugin", "Lab overlay · plugin_demo_lab.py"),

        ("demo", "Environmental publisher — learning outcomes", [
            "Prove async plugins run autonomously without a Plugin Call per data point — validating Module B async theory.",
            "Prove edge LR container publishes time-series to InfluxDB reachable on Docker network s4t at hostname influxdb.",
            "Prove the data model matches TOO(L)SMART air-quality and meteorological schema with environmental_data measurement.",
            "Prove state file resume and oslo_log traceability for production-style fault-tolerant urban monitoring.",
            "Deliverable: at least one SELECT * FROM environmental_data row with Temperature and PM25 fields populated.",
        ]),

        ("image", "UML sequence — Async environmental publisher (Module C)",
         "diagrams/seq-environmental-async.png",
         "Start plugin → loop CSV → InfluxDB secco.environmental_data every 30s"),

        ("hands_on", "Step 1 — Verify InfluxDB (5 min)", [
            "Confirm container influxdb running: docker compose ps | grep influxdb (lab overlay).",
            "curl http://{{VM_IP}}:8086/ping — expect HTTP 204 No Content.",
            "docker exec influxdb influx -username admin -password admin \\",
            "  -execute 'CREATE DATABASE IF NOT EXISTS secco'",
            "SHOW DATABASES should list secco alongside _internal.",
        ]),

        ("image", "InfluxDB — debug / metrics page",
         "chapter15/influxdb-debug.png", "http://{{VM_IP}}:8086/debug/vars", "", True),

        ("warn", "LR → InfluxDB networking fix (critical)", [
            "Default ch15 plugin uses localhost:8086 — FAILS inside LR container with connection refused.",
            "Fix: self.host = 'influxdb' (Docker DNS on network s4t) — already applied in plugin_demo_lab.py.",
            "Use lab file: training/ch15-lab/plugin_demo_lab.py — not raw training/repos/ch15/plugin_demo.",
            "Do NOT use host IP gateway — fragile across restarts; use s4t service names consistently.",
        ]),

        ("hands_on", "Step 2 — Install dependencies in LR (5 min)", [
            "docker exec -it lightning-rod pip install influxdb pandas requests",
            "docker exec -it lightning-rod mkdir -p /opt/data",
            "CSV downloads automatically on first plugin start from Google Drive URL in plugin code.",
            "Verify LR on s4t network: docker inspect lightning-rod | grep -A5 Networks",
        ]),

        ("image", "Lightning-Rod — Configuration",
         "chapter13/lr-dashboard-conf.png",
         "http://{{VM_IP}}:1474 — async plugin executes inside LR on network s4t", "", True),

        ("hands_on", "Step 3 — Create and start async plugin (15 min)", [
            "Horizon → Plugins → Create — paste training/ch15-lab/plugin_demo_lab.py source.",
            "Callable = OFF (async) → Submit to repository.",
            "Inject on Active board from Module A → use Start (NOT Plugin Call).",
            "Watch logs: docker compose logs -f lightning-rod — expect Row N sent every 30 seconds.",
        ]),

        ("image", "Horizon IoT — Plugins (async Start)",
         "chapter14/horizon-plugins-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/plugins/ — Callable=OFF → Inject → Start", "", True),

        ("hands_on", "Step 4 — Query InfluxDB and validate (10 min)", [
            "docker exec influxdb influx -username admin -password admin -database secco \\",
            "  -execute 'SELECT * FROM environmental_data ORDER BY time DESC LIMIT 5'",
            "Expected: rows with temperature, humidity fields — verified 4+ points in lab.",
            "$ ./validate/validate-demo-ch15.sh",
        ]),

        ("image", "InfluxDB — environmental_data query result",
         "chapter15/influx-query-environmental.png",
         "Verified query output from Module C demo", "", True),

        ("content", "Hands-on troubleshooting — environmental plugin", [
            "No rows after 2 min → check plugin Started (not just injected) and LR logs for connection errors.",
            "Connection refused to InfluxDB → confirm self.host = 'influxdb' not localhost in plugin source.",
            "CSV download failed → verify VM has outbound HTTPS to Google Drive; check /opt/data inside LR.",
            "ImportError influxdb → re-run pip install inside lightning-rod container before Start.",
            "Empty measurement → wrong database; confirm USE secco and SHOW MEASUREMENTS output.",
        ]),

        ("section", "TOO(L)SMART smart-city case", "Ch.15 §15.5 · national replication"),

        ("theory", "TOO(L)SMART — national smart station network overview", [
            "TOO(L)SMART builds a replicable national network of environmental smart stations across Italian cities.",
            "Pilot cities: Turin, Padua, Lecce, Siracusa, and Messina — each with distinct deployment maturity.",
            "Goal: democratize air-quality and meteorological monitoring with open data and standardized edge software.",
            "Stack4Things and IoTronic orchestrate edge nodes; cloud stores time-series and serves CKAN open-data APIs.",
            "Grafana dashboards and Node-RED flows provide operator visualization and alert automation.",
            "Today's lab CSV plugin implements the same Worker pattern deployed on physical Pi stations in the field.",
        ], "Ch.15 §15.5 · TOO(L)SMART"),

        ("theory", "Deployment Model 1 — Turin full integration", [
            "Turin deployed seven monitoring stations as the reference architecture for the entire national program.",
            "Full stack: S4T, IoTronic, Lightning-Rod, InfluxDB, Grafana, CKAN, Node-RED, and WebSocket tunnels.",
            "Custom integration tied each station to municipal IT, university research networks, and public portals.",
            "Approximately eight months from design to deployment plus one year of operational validation.",
            "Lessons from Turin informed standardized VM bundles used in Model 2 cities.",
            "Turin remains the template for cities willing to invest in deep OpenStack and S4T integration.",
        ], "Ch.15 · Deployment Model 1 · Turin"),

        ("theory", "Deployment Model 1 — Turin operational outcomes", [
            "Continuous environmental_data streams feed municipal air-quality compliance reporting.",
            "Open CKAN datasets enable citizen science apps and academic research on urban pollution.",
            "Centralized IoTronic logging lets operators diagnose station faults without visiting rooftop enclosures.",
            "Plugin remote update deployed new CSV field mappings without hardware changes during pilot extensions.",
            "WebSocket tunnels exposed station maintenance APIs securely through municipal firewalls.",
            "Model 1 proves the three-layer architecture at production scale — not only lab Docker Compose.",
        ], "Ch.15 · Model 1 · Turin operational validation"),

        ("theory", "Deployment Model 2 — plug-and-play VM bundles", [
            "Padua, Lecce, Siracusa, and Messina received pre-configured VM images for rapid city onboarding.",
            "Each bundle ships Controller Node plus Data Portal — minimal custom integration per municipality.",
            "Modularity and virtualization accelerated city-to-city replication from months toward weeks.",
            "Open standards throughout: CKAN for data, WAMP for control, JSON for payloads, Docker for packaging.",
            "Cities with limited OpenStack expertise still join the network without Turin-scale custom engineering.",
            "Environmental Worker and InfluxDB measurement schema are identical across Model 1 and Model 2.",
        ], "Ch.15 · Deployment Model 2 · VM bundle"),

        ("theory", "Deployment Model 2 — when cities choose plug-and-play", [
            "Smaller municipalities lack dedicated cloud engineers — VM bundles reduce operational skill requirements.",
            "Pre-tested images include Grafana dashboards and CKAN harvesters matching TOO(L)SMART field naming.",
            "Controller Node VM runs IoTronic-facing services; edge Pi boards still run Lightning-Rod and plugins.",
            "Data Portal VM hosts InfluxDB, Grafana, and public APIs — separating acquisition from publication tier.",
            "Upgrade path: cities can migrate from Model 2 bundle toward Model 1 full integration as maturity grows.",
            "Lab Docker Compose is a minimal Model 2 slice — one VM, one LR board, one InfluxDB, one async plugin.",
        ], "Ch.15 · Model 2 · replication economics"),

        ("theory", "Lessons learned — TOO(L)SMART and Chapter 15", [
            "Plugin model enables remote logic updates without physical access — essential for rooftop station maintenance.",
            "Time-series storage plus Grafana dashboards give operators observability missing from raw CSV exports.",
            "Cloud-native OpenStack with IoTronic scales multi-city orchestration under Keystone multi-tenancy.",
            "Lab CSV demo maps one-to-one to Raspberry Pi sensor acquisition — swap data source, keep architecture.",
            "Open-data publication via CKAN closes the loop from edge sensing to citizen-facing urban intelligence.",
            "Software-defined infrastructure turns each station into a remotely programmable cyber-physical asset.",
        ], "Ch.15 conclusion · TOO(L)SMART lessons"),

        ("content", "3-hour core course wrap-up", [
            "Module A (Ch.13): deploy I/Ocloud S4T stack, onboard board to Active state.",
            "Module B (Ch.14): sync HelloName plugin, async theory, optional Docker at edge.",
            "Module C (Ch.15): environmental async publisher → InfluxDB time-series validation.",
            "Extended path (6–9h): Modules D–I — multiboard fleet, VN, web services, FL, Blueprint, FaaS.",
            "See 00_Course_Map_EN.pptx · validate: cd training && ./validate-lab.sh",
        ]),

        ("content", "Final deliverables checklist", [
            "□ Board Active screenshot (Module A).",
            "□ HelloName Plugin Call output in Horizon or LR log (Module B).",
            "□ InfluxDB SELECT * FROM environmental_data LIMIT 5 output (Module C).",
            "Material: training/GUIDA_SETUP_CORSISTI.md · training/HANDS_ON_COMMANDS.md",
        ]),
    ]
