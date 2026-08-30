"""Module D — Multi-board & Fleet (Ch.13–14)."""


def slides() -> list:
    return [
        ("title", "Module D — Multi-board & Fleet Operations",
         "Extension · +45–60 min · Ch.13–14 · VM {{VM_IP}}",
         "Extension · Ch.14 — Multi-board & Fleet · prerequisite for Module G"),

        ("section", "Why multiple boards?", "Fleet theory before scaling the lab"),

        ("theory", "Scaling from one board to a fleet (Ch.13–14)", [
            "Real S4T deployments manage hundreds of heterogeneous boards across sites",
            "Each board = one Lightning-Rod instance with unique IoTronic registration code",
            "Lab simulates 3 boards via lightning-rod, lightning-rod-2, lightning-rod-3 containers",
            "Same cloud IoTronic Conductor manages all boards under one Keystone tenant",
            "Multi-board topology mirrors TOO(L)SMART multi-station urban deployments (Ch.15)",
            "Book repo ch13 documents docker-compose scaling pattern used in this module",
        ], "Ch.13 multi-board note · Ch.14 fleet abstract"),

        ("theory", "Lightning-Rod instance isolation (Ch.13)", [
            "Each LR container binds a distinct host port (:1474, :1475, :1476) for its Web UI",
            "WAMP connection shares crossbar:8181 — IoTronic distinguishes boards by registration",
            "Board metadata (name, UUID, status) stored in IoTronic MariaDB — not in LR container",
            "Plugin inject targets a specific board UUID or an entire fleet collection",
            "Credentials per LR dashboard: {{LR_CRED}} — same pattern on all three instances",
            "Active state requires successful WAMP handshake + heartbeat to Conductor",
        ], "Ch.13 § Lightning-Rod configuration · fig:chap13:lr-conf"),

        ("theory", "Board registration workflow recap (Ch.13)", [
            "Horizon IoT → Create Board → copy one-time registration code",
            "LR Configuration page: paste code, set WAMP URL wss://crossbar:8181, save",
            "Board transitions: Created → Registering → Active (or Error if misconfigured)",
            "Three boards in this module: board-alpha, board-beta, board-gamma",
            "Each board gets independent plugin namespace — inject does not cross boards unless fleet",
            "REST API mirror: GET /v1/boards/ lists all registered boards with status field",
        ], "Ch.13 § board onboarding · listing create_board"),

        ("theory", "Fleet abstraction in depth (Ch.14 §14.2)", [
            "Fleet ≠ trivial label — semantically meaningful collection of IoT devices",
            "Tenant-aware grouping under OpenStack Keystone multi-tenancy model",
            "Members act in unison: one fleet-level inject reaches ALL boards in the fleet",
            "Absence or failure of one member can affect fleet-level application behaviour",
            "Fleet metadata editable: name, description, member add/remove without re-registering boards",
            "Book figures: fig:fleetpanel, fig:fleetpanelCreation, fig:fleetinjPop",
        ], "Ch.14 §14.2 · Stack4Things fleet management"),

        ("theory", "Fleet vs individual board operations (Ch.14)", [
            "Individual inject: fine-grained control, debugging one misbehaving board",
            "Fleet inject: operational efficiency at scale — one UI action, N boards updated",
            "Same Worker Python code runs on each LR independently after fleet inject",
            "Plugin Call (sync) still per-board unless custom fleet orchestration API used",
            "Fleet delete removes grouping only — boards remain registered and Active",
            "Production pattern: dev/test on single board → promote inject to fleet for rollout",
        ], "Ch.14 bulk plugin deployment · fig:fleetinjPop"),

        ("theory", "Horizon fleet UI workflow (Ch.14)", [
            "Fleets panel: http://{{VM_IP}}/horizon/iot/fleets/ — create, filter, edit, delete",
            "Create Fleet: name + description → add member boards from Active board list",
            "Fleet detail → Plugins tab: inject / update / remove on ALL fleet members at once",
            "Boards panel remains for device-level troubleshooting and individual actions",
            "Horizon login: {{HZ_CRED}} — same tenant sees all boards and fleets",
            "Screenshots in deck captured from live lab — regenerate via capture_dashboards.py",
        ], "Ch.14 § Stack4Things fleets · Horizon IoT dashboard"),

        ("theory", "Plugin inject on fleet — execution model (Ch.14)", [
            "IoTronic sends inject command to each fleet member's Lightning-Rod concurrently",
            "Each LR Plugin Manager loads Worker class independently — no shared process",
            "Sync plugin (HelloName): after fleet inject, Plugin Call is still one board at a time",
            "Async plugin: Start on fleet would launch background loop on every member simultaneously",
            "Fleet inject failure on one member: check that board's LR logs before retrying fleet action",
            "Module G (FL) uses per-board async inject — fleet inject not used for Flower clients",
        ], "Ch.14 §14.1 plugin lifecycle · fleet inject listing"),

        ("theory", "Fleet operations beyond inject (Ch.14 §14.2)", [
            "Fleet-level async Start launches background plugins on all members simultaneously.",
            "Fleet update pushes revised plugin source to every attached board in one operation.",
            "Fleet remove detaches plugin from all members — boards remain Active in Horizon.",
            "Fleet health: absence or failure of one member can break fleet-level application logic.",
            "REST API mirrors Horizon: fleet CRUD and bulk plugin operations via Conductor.",
            "Lab focuses on sync HelloName fleet inject — async fleet Start is production pattern for Ch.15.",
        ], "Ch.14 §14.2 · supported fleet operations · fig:fleetinjPop"),

        ("image", "Multi-board fleet topology",
         "diagrams/multiboard-fleet.png",
         "Three LR instances → one IoTronic Conductor → fleet-level plugin inject"),

        ("content", "Module D — learning objectives", [
            "Start lightning-rod-2 and lightning-rod-3 on host ports 1475 and 1476",
            "Register board-alpha, board-beta, board-gamma — all Active in Horizon",
            "Create a fleet containing all three boards",
            "Fleet inject HelloName sync plugin; verify Plugin Call on each board",
            "Pass validate-lab-multiboard.sh — prerequisite for Module G Federated Learning",
        ]),

        ("content", "Module D — 45-minute timeline", [
            "0–10 min  — Fleet theory + multi-board architecture (slides above)",
            "10–15 min — DEMO GOAL review + start extra LR containers",
            "15–30 min — HANDS-ON: create 3 boards, configure 3 LR instances",
            "30–40 min — HANDS-ON: create fleet + fleet inject HelloName",
            "40–45 min — Validate + Module G handoff preview",
        ]),

        ("demo", "What this module proves — demo goals", [
            "Same IoTronic Conductor orchestrates multiple edge agents concurrently",
            "Fleet inject deploys identical plugin logic to all members in one Horizon action",
            "Each board maintains independent LR runtime — fleet is logical grouping only",
            "Prerequisite satisfied for Module G: 3 Active clients on separate boards for FL",
            "Mirrors production rollout: test plugin on one board → fleet inject for deployment",
            "Students can articulate difference between board inject and fleet inject",
        ]),

        ("section", "Hands-on — start extra Lightning-Rod instances", "Docker Compose lab overlay"),

        ("hands_on", "Step 1 — Start LR-2 and LR-3 containers", [
            "$ cd training/repos/ch13",
            "$ docker compose -f docker-compose.yml \\",
            "    -f ../../patches/docker-compose.lab.yml up -d lightning-rod-2 lightning-rod-3",
            "$ training/experiments/multiboard/check-endpoints.sh",
            "Expected: HTTP 200 on {{VM_IP}}:1475 and {{VM_IP}}:1476",
        ]),

        ("theory", "Lab compose port mapping (Ch.13 patch)", [
            "docker-compose.lab.yml adds lightning-rod-2 → host :1475, lightning-rod-3 → :1476",
            "Default lightning-rod (instance 1) remains on :1474 from Module A",
            "All three share iotronic-network — WAMP crossbar reachable as wss://crossbar:8181",
            "check-endpoints.sh verifies UI reachability before board registration begins",
            "Container names: lightning-rod, lightning-rod-2, lightning-rod-3 — distinct hostnames",
            "If port conflict: ensure no other service bound to 1475/1476 on lab VM",
        ], "training/patches/docker-compose.lab.yml · ch13 repo"),

        ("section", "Hands-on — register three boards in Horizon", "Create Board × 3"),

        ("image", "Horizon IoT — Boards dashboard (create 3 boards)",
         "chapter13/horizon-boards-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/ → Create Board × 3 · login {{HZ_CRED}}", "", True),

        ("hands_on", "Step 2 — Create three boards in Horizon", [
            "Open http://{{VM_IP}}/horizon/iot/ — login {{HZ_CRED}}",
            "Create Board: board-alpha → copy registration code to notepad",
            "Create Board: board-beta → copy registration code",
            "Create Board: board-gamma → copy registration code",
            "Do NOT reuse codes — each board gets a unique one-time registration token",
        ]),

        ("image", "Book figure — Create Board form (Ch.13)",
         "chapter13/sshot-create-board.png",
         "Reference UI fields: name, description, registration code display"),

        ("section", "Hands-on — configure each Lightning-Rod", "Registration code + WAMP URL"),

        ("image", "LR instance 1 — Configuration (board-alpha)",
         "chapter13/lr-dashboard-conf.png",
         "http://{{VM_IP}}:1474/config — board-alpha · {{LR_CRED}}", "", True),

        ("image", "LR instance 2 — home dashboard",
         "chapter19/lr-dashboard-home-lr2.png",
         "http://{{VM_IP}}:1475 — board-beta will register here"),

        ("hands_on", "Step 3 — Configure Lightning-Rod instance 1 (alpha)", [
            "Open http://{{VM_IP}}:1474/config — login {{LR_CRED}}",
            "Paste board-alpha registration code",
            "WAMP URL: wss://crossbar:8181 · Save",
            "Verify board-alpha shows Active in Horizon before proceeding",
        ]),

        ("image", "LR instance 2 — Configuration (board-beta)",
         "chapter19/lr-dashboard-conf-lr2.png",
         "http://{{VM_IP}}:1475/config — board-beta registration", "", True),

        ("hands_on", "Step 4 — Configure Lightning-Rod instance 2 (beta)", [
            "Open http://{{VM_IP}}:1475/config — login {{LR_CRED}}",
            "Paste board-beta registration code · WAMP: wss://crossbar:8181 · Save",
            "Wait for Active status in Horizon",
        ]),

        ("image", "LR instance 3 — home dashboard",
         "chapter19/lr-dashboard-home-lr3.png",
         "http://{{VM_IP}}:1476 — board-gamma will register here"),

        ("image", "LR instance 3 — Configuration (board-gamma)",
         "chapter19/lr-dashboard-conf-lr3.png",
         "http://{{VM_IP}}:1476/config — board-gamma registration", "", True),

        ("hands_on", "Step 5 — Configure Lightning-Rod instance 3 (gamma)", [
            "Open http://{{VM_IP}}:1476/config — login {{LR_CRED}}",
            "Paste board-gamma registration code · WAMP: wss://crossbar:8181 · Save",
            "All three boards MUST show Active in Horizon before fleet inject",
        ]),

        ("theory", "Troubleshooting multi-board registration", [
            "Board stuck in Registering: check LR logs — docker logs lightning-rod-2",
            "Wrong code on wrong LR: board shows Error — remove and re-create board in Horizon",
            "WAMP connection refused: verify crossbar container healthy in docker compose ps",
            "Duplicate registration: each code valid for one LR instance only",
            "API check: curl -s http://{{VM_IP}}:8812/v1/boards/ | python3 -m json.tool",
            "All three status fields must read Active before continuing to fleet creation",
        ], "Ch.13 troubleshooting · IoTronic REST API"),

        ("section", "Hands-on — create fleet and inject HelloName", "Fleet-level plugin deploy"),

        ("image", "UML sequence — Fleet plugin inject (Module D)",
         "diagrams/seq-fleet-inject.png",
         "Create fleet → inject HelloName on board-alpha, beta, gamma"),

        ("image", "Horizon IoT — Fleets panel",
         "chapter14/horizon-fleets-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/fleets/ — Create Fleet", "", True),

        ("hands_on", "Step 6 — Create fleet and add all Active boards", [
            "http://{{VM_IP}}/horizon/iot/fleets/ → Create Fleet",
            "Name: lab-fleet-3 · add board-alpha, board-beta, board-gamma",
            "Save — verify all three members listed in fleet detail view",
        ]),

        ("hands_on", "Step 7 — Fleet inject HelloName plugin", [
            "Fleet → Plugins tab → Inject → select HelloName (from Module B)",
            "Confirm inject succeeds on all three members",
            "Per board: Plugins → HelloName → Plugin Call → {\"name\": \"fleet-demo\"}",
            "Verify JSON result returned on each of :1474, :1475, :1476 boards",
        ]),

        ("theory", "Fleet inject vs individual inject — when to use each", [
            "Development/debug: individual board inject — isolate failures quickly",
            "Production rollout: fleet inject — consistent version across all edge nodes",
            "Heterogeneous fleets: filter members by tag/metadata before inject (production feature)",
            "HelloName sync demo: fleet inject saves time; Plugin Call proves per-board execution",
            "Module G FL: per-board async inject with different CSV — not fleet inject pattern",
            "Book Ch.14 fleet panel screenshots match Horizon workflow shown in hands-on steps",
        ], "Ch.14 §14.2 · bulk plugin deployment"),

        ("section", "Validate & wrap-up", "Confirm lab state for Module G"),

        ("hands_on", "Step 8 — Validate multi-board lab state", [
            "$ cd training && ./validate-lab-multiboard.sh",
            "$ curl -s http://{{VM_IP}}:8812/v1/boards/ | python3 -m json.tool",
            "Expected: 3 boards, all status Active, fleet lab-fleet-3 exists",
        ]),

        ("content", "Module D checklist", [
            "□ Three boards Active in Horizon (board-alpha, board-beta, board-gamma)",
            "□ Three LR UIs reachable: {{VM_IP}}:1474, :1475, :1476",
            "□ Fleet created with HelloName injected on all members",
            "□ validate-lab-multiboard.sh passes",
            "Prerequisite satisfied → proceed to Module G (Federated Learning) or Module F (WSTUN)",
        ]),
    ]
