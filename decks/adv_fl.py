"""Module G — Federated Learning (Ch.19)."""


def slides() -> list:
    return [
        ("title", "Module G — Federated Learning on the Edge",
         "Ch.19 · Advanced · VM {{VM_IP}}",
         "Advanced · Ch.19 — Federated Learning · requires Module D (3 Active boards)"),

        ("section", "Federated Learning theory", "Ch.19 — motivation, architecture, taxonomy"),

        ("theory", "Why Federated Learning? (Ch.19)", [
            "Centralized ML: collect all raw data to cloud — privacy, GDPR, bandwidth, latency risks",
            "FL: train collaboratively — raw data never leaves edge devices or local storage",
            "Only model weight updates (gradients/parameters) sent to aggregation server each round",
            "Critical for healthcare, finance, smart cities, IoT fleets with sensitive local data",
            "Regulatory frameworks (GDPR, DPDP, HIPAA) restrict data centralization — FL enables compliance",
            "Book motivation section cites real-world cases: hospitals, banks, cross-device IoT",
        ], "Ch.19 · FL motivation · regulatory compliance section"),

        ("theory", "Centralized vs federated — operational contrast (Ch.19)", [
            "Centralized: ETL pipeline uploads datasets → single GPU cluster trains monolithic model",
            "Federated: N clients train locally → server aggregates → global model improves iteratively",
            "Centralized bottleneck: network upload of full dataset from each edge site",
            "Federated bottleneck: straggler clients, non-IID data distribution, communication rounds",
            "S4T value proposition: IoTronic deploys FL client plugin to fleet — operational layer for FL",
            "Lab demo: 3 production lines, 3 CSV files, 1 Flower server — horizontal FL for failure prediction",
        ], "Ch.19 · centralized vs federated comparison"),

        ("theory", "FL architecture components (Ch.19)", [
            "Server (Flower in lab): orchestrates rounds, aggregates updates (FedAvg algorithm)",
            "Clients: local training on board-resident telemetry — machine_1/2/3.csv (predictive maintenance)",
            "Stack4Things: async plugin injected on each board via IoTronic — Worker connects to server",
            "Direct TCP to Flower server on VM host — lightweight for lab; MQTT optional in field",
            "Book figure: fig:chap19:federated_learning_architecture — 3 clients + 1 server",
            "Each client runs local epochs before sending weight update — not every mini-batch",
        ], "Ch.19 · fig:chap19:federated_learning_architecture · listing server.py"),

        ("theory", "FedAvg aggregation algorithm (Ch.19)", [
            "Federated Averaging: server computes weighted average of client model parameters",
            "Weight proportional to local dataset size — larger datasets influence global model more",
            "Round k: server broadcasts global model → clients train locally → clients send updates",
            "Server aggregates → broadcasts updated global model → repeat for FL_ROUNDS iterations",
            "Convergence depends on data IID-ness — lab CSVs designed with compatible schema",
            "Flower framework abstracts transport — same FedAvg logic in lab and production",
        ], "Ch.19 · FedAvg · Flower framework references"),

        ("theory", "FL taxonomy — four categories (Ch.19)", [
            "Horizontal FL: same features, different samples — hospitals, IoT boards (lab demo type)",
            "Vertical FL: different features, same samples — bank + credit card company collaboration",
            "Cross-silo: organizations with stable connectivity and rich local datasets",
            "Cross-device: many mobile/IoT clients, intermittent connectivity, small local data",
            "Lab demo: horizontal cross-silo — 3 boards, same CSV schema, different row samples",
            "Book taxonomy table helps students classify real-world FL deployment scenarios",
        ], "Ch.19 · FL types · horizontal vs vertical"),

        ("theory", "Non-IID data challenges (Ch.19)", [
            "Real edge data often non-IID: each production line has different failure signatures",
            "Lab: CNC spindle vs conveyor vs pump — distinct vibration/temperature/current patterns",
            "target=1 = failure imminent; federated model learns global predictor without centralizing CSVs",
            "Non-IID slows convergence — may require more FL_ROUNDS or specialized aggregation",
            "Production mitigations: FedProx, SCAFFOLD — beyond lab scope",
            "Module D fleet (3 boards) mirrors cross-silo industrial FL scenario",
        ], "Ch.19 · non-IID · predictive maintenance lab extension"),

        ("theory", "S4T + FL integration — plugin model (Ch.19)", [
            "Each board monitors a different machine: vibration, temperature, motor current (local CSV)",
            "Target: binary failure_imminent — raw telemetry never leaves the edge board",
            "Plugin lifecycle: install datasets → shared fl-client in FL panel → inject → Start",
            "board-alpha = CNC spindle, board-beta = conveyor motor, board-gamma = pump line",
            "Non-IID by design: each line has different failure signatures (Ch.19 horizontal FL)",
            "Repo: ch19/server.py + fl_client_plugin.py + machine_*.csv (generate_pm_datasets.py)",
        ], "Ch.19 · server on cloud VM · 3 board clients · Horizon Federated Learning panel"),

        ("theory", "Privacy and regulatory framing (Ch.19)", [
            "GDPR Article 25: data protection by design — FL keeps raw data at edge by default",
            "DPDP (India), HIPAA (US healthcare): restrict cross-border raw data transfer",
            "FL enables smarter systems while data stays on edge nodes under local jurisdiction",
            "S4T provides deployment vehicle (IoTronic inject) — FL provides training methodology",
            "Production extensions: differential privacy noise on updates, secure aggregation (crypto)",
            "Lab scope: demonstrate FL workflow — not production-grade privacy guarantees",
        ], "Ch.19 · regulatory compliance · privacy-preserving FL footnote"),

        ("theory", "FL challenges and open issues (Ch.19)", [
            "System heterogeneity: boards differ in CPU, RAM, bandwidth — stragglers delay aggregation rounds.",
            "Client availability: intermittent connectivity reduces effective participants per round.",
            "Model heterogeneity: incompatible architectures complicate weight merging and convergence.",
            "Statistical heterogeneity (Non-IID): skewed local data degrades global model accuracy.",
            "Model update security: poisoning and backdoor attacks via malicious local training data.",
            "Mitigations include FedProx, secure aggregation, differential privacy — research beyond lab scope.",
        ], "Ch.19 § Challenges and open issues · FedProx · secure aggregation footnote"),

        ("theory", "FL platform landscape (Ch.19)", [
            "Open source: TensorFlow Federated, Flower (lab choice), PySyft, LEAF benchmarks, FedML.",
            "Enterprise: NVIDIA FLARE, IBM FL — production orchestration and compliance tooling.",
            "Flower chosen in ch19 repo for lightweight Python server + edge client plugin integration.",
            "Platform choice depends on scale, privacy requirements, and edge hardware constraints.",
            "S4T contribution: same IoTronic inject lifecycle deploys FL client Workers on real boards.",
            "Google/Apple on-device FL cited in book as industry validation of federated approach.",
        ], "Ch.19 § Core requirements · tools and frameworks"),

        ("image", "FL architecture — 3 edge clients",
         "diagrams/fl-architecture.png",
         "Flower server on VM host + 3 LR clients on :1474/:1475/:1476 (Module D)"),

        ("image", "UML sequence — Federated Learning round (Module G)",
         "diagrams/seq-fl-round.png",
         "Broadcast weights → local train → upload gradients → FedAvg"),

        ("content", "Module G — learning objectives", [
            "Explain FL motivation, FedAvg, and horizontal cross-silo taxonomy (Ch.19)",
            "Deploy Flower server; federated failure-prediction model across 3 edge production lines",
            "Inject FL async client on 3 Active boards with distinct machine_*.csv datasets",
            "Observe ≥2 aggregation rounds complete (FL_ROUNDS=2 classroom pacing)",
            "Pass validate-lab-fl.sh — bridge Ch.19 AI methodology with Ch.13–14 S4T stack",
        ]),

        ("content", "Module G — 60-minute timeline", [
            "0–20 min  — FL theory: motivation, FedAvg, taxonomy, S4T integration",
            "20–25 min — DEMO GOAL review + prerequisites check (Module D)",
            "25–40 min — HANDS-ON: start Flower server + deploy client plugins",
            "40–55 min — HANDS-ON: Start plugins, watch aggregation rounds in server log",
            "55–60 min — Validate + privacy/regulatory discussion wrap-up",
        ]),

        ("demo", "What the FL demo proves — demo goals", [
            "Edge boards participate in distributed ML without sharing raw CSV data across boards",
            "IoTronic deploys identical FL client plugin code to heterogeneous Active boards",
            "Aggregation improves global model accuracy over successive rounds (FL_ROUNDS=2 in class)",
            "Bridges Ch.19 AI methodology with Ch.13–14 S4T operational stack (inject + Start)",
            "Students can classify lab setup as horizontal cross-silo FL from Ch.19 taxonomy",
            "Flower server log shows round completion — tangible evidence of federated aggregation",
        ]),

        ("content", "Prerequisites & resource constraints", [
            "Module D complete — 3 Active boards on {{VM_IP}}:1474/:1475/:1476",
            "Repo: ch19/server.py + fl_client_plugin.py + machine_*.csv (predictive maintenance lab)",
            "Run install-fl-on-boards.sh once — deps + machine_*.csv into LR containers",
            "Classroom pacing: FL_ROUNDS=2 — keeps session within 60 minutes",
            "Do NOT run simultaneously with Module H K3s — RAM gate: free -h ≥ 2 GB during FL",
            "Horizon {{HZ_CRED}} · LR dashboards {{LR_CRED}} on all three instances",
        ]),

        ("section", "Hands-on — Flower server setup", "Install dependencies + start aggregation"),

        ("hands_on", "Step 1 — Install FL deps on VM and boards", [
            "$ cd training && pip install flwr torch pandas scikit-learn  # or use .venv",
            "$ ./experiments/federated-learning/install-fl-on-boards.sh",
            "Copies machine_1/2/3.csv + fl_client_plugin.py into each LR container (/opt/fl/)",
        ]),

        ("theory", "Flower server configuration (Ch.19)", [
            "server.py on VM host: FedAvg strategy — same role as book listing (Cap. 19)",
            "FL_ROUNDS env var controls aggregation iterations — set to 2 for classroom demo",
            "Server binds 0.0.0.0:8087 (default) — avoids WSTUN conflict on :8080",
            "LR containers reach VM host via Docker bridge gateway (e.g. 172.18.0.1:8087)",
            "Minimum clients: 3 (matches 3 boards from Module D) — server waits for all before round",
            "Server log prints per-round aggregated metrics — instructor projects for class visibility",
        ], "Ch.19 · server.py on cloud VM · FL_PORT=8087 · Horizon panel + fl-control :8091"),

        ("hands_on", "Step 2 — Enable FL panel and start Flower server", [
            "$ cd training && ./experiments/federated-learning/setup-fl-horizon.sh  # once",
            "Horizon → IoT → Federated Learning → Lab parameters → Save",
            "Click Start Flower server (or Restart after param changes) — live topology iframe",
            "Optional demo-ready: ./experiments/federated-learning/setup-fl-demo-plugins.sh",
        ]),

        ("section", "Hands-on — deploy FL client plugins", "Single shared fl-client plugin"),

        ("hands_on", "Step 3 — Create and inject FL client plugin", [
            "Horizon → Federated Learning → Create / update FL client plugin (name: fl-client)",
            "One shared async plugin — per-board JSON: csv_file + board_name only",
            "Inject fl-client: board-alpha (machine_1/CNC), board-beta (machine_2/conveyor), board-gamma (machine_3/pump)",
            "Lab parameters supply server_address and dashboard_url — Apply to all boards",
        ]),

        ("image", "Horizon — Federated Learning panel (Module G)",
         "chapter19/horizon-fl-panel.png",
         "Predictive maintenance lab · machine_1/2/3.csv per board · {{HZ_CRED}}", "", True),

        ("image", "Lab parameters — rounds, server and dashboard URLs",
         "chapter19/horizon-fl-lab-params.png",
         "FL rounds + Docker gateway for Flower :8087 and dashboard :8090", "", True),

        ("image", "Edge FL clients — failure prediction per production line",
         "chapter19/horizon-fl-edge-clients.png",
         "board-alpha CNC · board-beta conveyor · board-gamma pump · machine_*.csv JSON", "", True),

        ("image", "Multi-board topology for FL clients",
         "diagrams/multiboard-fleet.png",
         "3 LR clients :1474/:1475/:1476 → Flower server on VM host :8087 (not on a board)"),

        ("image", "Live topology — federated failure-prediction dashboard",
         "chapter19/horizon-fl-live-topology.png",
         "Vibration/temperature/current models aggregate without sharing raw CSVs", "", True),

        ("hands_on", "Step 4 — Start FL clients on all three boards", [
            "With Flower server running: Federated Learning panel → Start all clients",
            "Or Start fl-client individually per board from the panel",
            "Watch live topology: clients connect → rounds advance → loss/accuracy update",
            "LR logs: docker logs lightning-rod-2 — local training progress messages",
        ]),

        ("theory", "Client plugin execution flow (Ch.19)", [
            "Start action launches async Worker — connects to Flower server via gRPC/TCP",
            "Worker loads local CSV — initializes model with global weights from server",
            "Local training: N local epochs on board CPU — sends weight delta to server",
            "Server aggregates all 3 client updates — broadcasts new global weights",
            "Round 2: clients receive updated global model — repeat local training",
            "Stop: Interrupt plugin on each board after rounds complete — clean shutdown",
        ], "Ch.19 · fl_client_plugin.py Worker + HeartClient · async plugin pattern"),

        ("theory", "Troubleshooting FL connectivity (Ch.19 lab)", [
            "Clients cannot connect: verify server on VM :8087 and gateway IP from install-fl-on-boards.sh",
            "Horizon 'Unable to retrieve boards list': run scripts/fix-iotronic-wampagents.sh",
            "Server stuck waiting: ensure all 3 Start actions fired — minimum client count not met",
            "OOM on board: reduce local epochs in plugin params — edge boards have limited RAM",
            "Plugin error on Start: re-run install-fl-on-boards.sh (flwr/torch in LR container)",
            "validate-lab-fl.sh — artifacts, Horizon mounts, panel URL, live proxy + optional E2E",
        ], "fix-iotronic-wampagents.sh · validate-lab-fl.sh · install-fl-on-boards.sh"),

        ("theory", "FL in the Cloud Continuum research context (Ch.19 + Ch.11)", [
            "Ch.11 Type 4 experiments: AI/ML workflows including federated learning at edge",
            "SLICES RI multi-site FL: clients on different European sites, server on cloud slice",
            "S4T IoTronic inject scales FL client deployment — same pattern as Module D fleet ops",
            "Crossplane Workflow CRD could declare FL experiment: server + N client plugins + datasets",
            "Edge-board FL preserves data sovereignty requirements of SLICES partner institutions",
            "Lab on {{VM_IP}} is minimal horizontal FL — production scales to cross-silo federation",
        ], "Ch.19 + Ch.11 Type 4 · SLICES RI FL experiment pattern"),

        ("section", "Validate & wrap-up", "Confirm aggregation + Module H exclusion"),

        ("hands_on", "Step 5 — Validate FL lab", [
            "$ cd training && ./validate-lab-fl.sh",
            "Live topology shows rounds completing; loss numeric (not em-dash)",
            "Interrupt FL plugins on all boards after successful validation",
        ]),

        ("content", "Module G checklist & resource note", [
            "□ Horizon FL panel: Start server + Start all clients — rounds complete in live topology",
            "□ Three production lines connected via fl-client with correct machine_*.csv per board",
            "□ validate-lab-fl.sh passes (Horizon mounts + :8091 control API)",
            "□ free -h ≥ 2 GB during FL — do NOT run K3s Blueprint (Module H) concurrently",
            "□ Students articulate horizontal cross-silo FL classification from Ch.19 taxonomy",
        ]),
    ]
