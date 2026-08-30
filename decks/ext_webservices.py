"""Module F — Web Services, WSTUN & WoT (Ch.6 + Ch.14)."""

LOCAL_PORT = 50000


def slides() -> list:
    return [
        ("title", "Module F — Web Services, WSTUN & WoT",
         "Ch.6 + Ch.14 · Extension · VM {{VM_IP}}",
         "Extension · Ch.6 + Ch.14 — Web Services, WSTUN & WoT · book :8080 vs lab :50000"),

        ("section", "Web of Things theory", "Ch.6 — layered model before the WSTUN demo"),

        ("theory", "Fragmented IoT and the need for abstraction (Ch.6)", [
            "IoT devices use incompatible protocols — Zigbee, MQTT, CoAP, proprietary HTTP APIs.",
            "Each vendor ships its own stack — integration requires custom middleware and data mapping.",
            "Parallel to the pre-WWW Internet: incompatible islands before HTTP unified access.",
            "WoT reuses HTTP, URIs, JSON, REST — decades of proven Web infrastructure and tooling.",
            "Common abstraction decouples application logic from board-specific SDKs and pin maps.",
            "S4T I/Ocloud + WoT gateway pattern is the book's answer to fragmentation at scale.",
        ], "Ch.6 §6.1 · fragmented IoT · need for common abstraction"),

        ("theory", "Web of Things paradigm (Ch.6)", [
            "Extend Web standards (HTTP, URIs, JSON, HTML) to physical objects and sensors",
            "Web Things expose RESTful APIs: readable properties, invokable actions, events",
            "Three integration patterns: direct API on device, smart gateway, I/Ocloud virtual nodes",
            "Goal: interoperable IoT at Web scale — not proprietary silo protocols (MQTT-only, etc.)",
            "WoT aligns with I/Ocloud vision (Ch.4): programmable CPS as Web-accessible infrastructure",
            "Module I (Ch.7 Deviceless) builds on WoT exposure patterns introduced here",
        ], "Ch.6 · Weaving the Web of Things · chapter abstract"),

        ("theory", "WoT layered model — Access layer (Ch.6)", [
            "Device becomes HTTP resource: GET /temperature, POST /led, GET /humidity",
            "Content negotiation: JSON for machines, HTML for human-readable sensor dashboards",
            "Gateway pattern: heterogeneous sensors → LR adapts protocols → uniform REST on HTTP/S",
            "Book live demo: wot.rasp-univ.iot.* — Flask endpoints on Raspberry Pi gateway",
            "Security: HTTPS termination at cloud reverse proxy; board may use HTTP internally",
            "Book figure: fig:chap06:WoT-layers — Access is the foundation layer",
        ], "Ch.6 · fig:chap06:WoT-layers · Access"),

        ("theory", "WoT layered model — Find, Share, Compose (Ch.6)", [
            "Find: machine-readable Thing Descriptions + discovery mechanisms (CoRE Link Format, etc.)",
            "Share: cross-domain access with social/trust models — who may read/actuate which Thing",
            "Compose: mashups combining distributed Web Things (sensor page + live video + map)",
            "S4T stack: Designate DNS + IoTronic service catalog enable Find at Web scale",
            "Horizon Web Services Manager exposes human-friendly URLs for board services",
            "DeXMS mediators (Ch.6 §6.4) deploy protocol bridges (MQTT, CoAP) on remote gateways",
        ], "Ch.6 · Find · Share · Compose layers"),

        ("theory", "Gateway-based WoT in S4T (Ch.6 §6.4)", [
            "Heterogeneous boards connect via Lightning-Rod — protocol adaptation at the edge",
            "Cloud stack: Designate (DNS) + IoTronic + NGINX reverse proxy + WebSocket tunnels",
            "Book architecture: cloud NGINX routes https://wot.board.example.com → board HTTP service",
            "LR runs local HTTP server (Flask, nginx) — cloud exposes it on public URL or port",
            "WoT Thing Description documents available endpoints for automated discovery",
            "Training lab uses WSTUN port mapping instead of full Designate DNS registration",
        ], "Ch.6 §6.4 · Stack4Things gateway WoT system · fig:chap06:s4t-wot"),

        ("theory", "Designate DNS and ACME certificates (Ch.6)", [
            "Designate is OpenStack's DNS-as-a-service — manages zones and records for board subdomains.",
            "Production WoT URL: web-server.node-A.example.com decomposed into service.node.fqdn parts.",
            "ACME (Certbot/Let's Encrypt) issues DV TLS certificates once DNS records propagate.",
            "Cloud NGINX terminates HTTPS and forwards to WSTUN backend for the matching board tunnel.",
            "Nine-step book workflow: catalog service → Enable → DNS → cert → NGINX → public HTTPS URL.",
            "Lab WSTUN skips DNS/ACME — same ServiceEnable API, different public endpoint format.",
        ], "Ch.6 § DNS in OpenStack · Designate · ACME · sec:expose-service"),

        ("theory", "DeXMS — gateway mediators for heterogeneous protocols (Ch.6)", [
            "DeXMS deploys protocol-bridge mediators on remote gateways via IoTronic RPC.",
            "DeXIDL GUI generates mediator JARs — packaged into LR Docker images for K8s/K3s rollout.",
            "CoAP observe streams and MQTT pub/sub topics become HTTP endpoints for WoT consumers.",
            "ESB-style integration without forcing every sensor to speak HTTP natively.",
            "Book sequence diagrams: CoAP→HTTP and MQTT→HTTP mediation paths (fig:chap06:coap/mqtt).",
            "Connects Module F HTTP demos to constrained-device protocols in smart-city deployments.",
        ], "Ch.6 §6.4 DeXMS · CoAP/MQTT mediation · fig:chap06:mediation"),

        ("theory", "Direct vs gateway vs virtual-node WoT patterns (Ch.6)", [
            "Direct: sensor board runs HTTP server — reachable if public IP (rare in IoT)",
            "Gateway: LR aggregates multiple sensors → single REST API surface (most common S4T)",
            "Virtual node: cloud-side software representation with same REST contract as physical board",
            "S4T supports all three; Ch.14 web services focus on gateway pattern with DNS/WSTUN",
            "Book weather station: gateway pattern — Flask on board, exposed via cloud proxy",
            "Lab nginx demo: gateway pattern — nginx in LR container, exposed via WSTUN tunnel",
        ], "Ch.6 · three WoT integration patterns"),

        ("section", "S4T Web Services (Ch.14 §14.3)", "Designate + WSTUN + service catalog"),

        ("theory", "Stack4Things Web Services overview (Ch.14 §14.3)", [
            "Expose IoT resources over the Web without manual port forwarding on edge routers",
            "Designate DNS-as-a-Service assigns subdomain per board (wot.board-1.example.com)",
            "NGINX reverse proxy + WebSocket tunnel routes HTTPS to edge HTTP service",
            "IoTronic Service Catalog: define reusable service templates (name + port + protocol)",
            "ServiceEnable action on board activates tunnel — cloud assigns public endpoint",
            "Book repo: ch14/demos/weather_web_server.py — canonical WoT weather station on :8080",
        ], "Ch.14 §14.3 · Web services integration · abstract"),

        ("theory", "Web Services Manager workflow (Ch.14)", [
            "Horizon Web Services panel → enable WSM per board → configure subdomain",
            "Service catalog entry: name (e.g. wot) + local port (8080 in book weather demo)",
            "Public URL: https://wot.board-1.example.com (Designate A record + NGINX location block)",
            "Exposes sensor GET endpoints + actuator POST (temperature, humidity, LED toggle)",
            "Book figures: fig:chap14:wot-manager, fig:chap14:wot-example",
            "Full path requires Designate + NGINX + valid DNS zone — optional in Docker lab",
        ], "Ch.14 · Web Services Manager · fig:chap14:wot-manager"),

        ("theory", "Book weather server — weather_web_server.py (Ch.14)", [
            "Flask app on board port 8080 — GET /temperature, /humidity, POST /led",
            "Simulated or real sensor reads — returns JSON for programmatic access",
            "Represents canonical WoT gateway service in book hands-on walkthrough",
            "Service catalog entry: name=wot, port=8080, protocol=TCP",
            "After ServiceEnable: public URL or WSTUN port maps to board :8080",
            "Students should understand this as the production-intent service (vs lab nginx shortcut)",
        ], "Ch.14 demos/weather_web_server.py · listing weather endpoints"),

        ("theory", "WSTUN — lab alternative to full Designate (Ch.13–14)", [
            "WSTUN Server (iotronic-wstun) manages reverse WebSocket tunnels to NAT-bound boards",
            "Service catalog: define service name + local TCP port on board (lab: 50000)",
            "ServiceEnable on board → cloud assigns public_port from range 50001–50100",
            "Lab access: http://{{VM_IP}}:<public_port>/ — no DNS registration required",
            "Same IoTronic API workflow as production — only the public endpoint format differs",
            "Book Ch.16 MACM documents WSTUNServer component architecture",
        ], "Ch.13 WSTUN · Ch.16 MACM WSTUNServer · docker-compose"),

        ("theory", "Book :8080 vs lab ports — verified divergence", [
            "Book (Ch.14): weather_web_server.py on port 8080 — GET /sensors, POST /led/toggle",
            "LR compose image reserves :8080 internally — lab runs weather on port 8088 instead",
            "Lab infra smoke test: lr-nginx-demo on port 50000 → WSTUN public_port (e.g. 50002)",
            "Book WoT demo verified: weather-wot service on lab port 8088 → WSTUN :50062 → HTTP 200 /sensors",
            "Both demos use identical IoTronic workflow: catalog → ServiceEnable → curl public endpoint",
            "Repo: github.com/AssemblingSmartCPS/ch14 · demos/weather_web_server.py",
        ], "Ch.14 demos/weather_web_server.py · run-weather-demo.sh"),

        ("image", "WSTUN port forwarding architecture",
         "diagrams/wstun-port-forwarding.png",
         "Edge service → WSTUN tunnel → cloud public_port (50001–50100 range)"),

        ("image", "UML sequence — ServiceEnable / WSTUN (Module F)",
         "diagrams/seq-wstun-enable.png",
         "Catalog → ServiceEnable → WSTUN tunnel → curl public_port/sensors"),

        ("content", "Module F — learning objectives", [
            "Explain Ch.6 WoT layered model and Ch.14 web services architecture",
            "Run book weather demo via run-weather-demo.sh (port 8088 lab / 8080 book)",
            "Run nginx infra smoke test via setup-wstun-demo.py (port 50000)",
            "Execute ServiceEnable on Active board — obtain public_port mapping",
            "curl /sensors JSON from weather tunnel and HTTP 200 from nginx tunnel",
        ]),

        ("content", "Module F — 40-minute timeline", [
            "0–15 min  — WoT theory (Ch.6) + Web Services theory (Ch.14)",
            "15–20 min — Two verified demos: weather-wot (book) + lr-nginx-demo (infra)",
            "20–35 min — HANDS-ON: run scripts → curl public ports → compare JSON vs HTML",
            "35–40 min — validate-lab-wstun.sh + optional Designate panel tour",
        ]),

        ("demo", "Demo A — Book weather server (ch14) — verified", [
            "Script: experiments/webservices/run-weather-demo.sh",
            "Starts weather_web_server.py inside LR on lab port 8088 (book uses 8080 on hardware)",
            "Creates catalog entry weather-wot · ServiceEnable → public_port (verified :50062)",
            "Success: curl http://{{VM_IP}}:<public_port>/sensors → JSON temperature/humidity",
            "Screenshot: assets/chapter14/weather-server-dashboard.png",
            "State file: experiments/webservices/weather-state.json",
        ]),

        ("demo", "Demo B — nginx infra smoke test — verified", [
            "Script: experiments/webservices/setup-wstun-demo.py",
            "Catalog lr-nginx-demo port 50000 → public_port (verified :50002) → HTTP 200",
            "Validates WSTUN tunnel plumbing without deploying Flask weather server",
            "Use when time is short — weather demo proves full WoT API path",
            "Both services can coexist on same board with different local ports",
        ]),

        ("content", "Lab stack — WSTUN component ports", [
            "WSTUN control plane: iotronic-wstun container in docker compose stack",
            "Tunnel public range: host ports 50001–50100 mapped in lab overlay patch",
            "Requires board Active (Module A) + service catalog entry with valid port ≠ 0",
            "Conductor API: http://{{VM_IP}}:8812 · Horizon: http://{{VM_IP}}/horizon/iot/",
            "Horizon login: {{HZ_CRED}}",
        ]),

        ("warn", "Horizon Create Service — Porta default is 0!", [
            "Form /horizon/iot/services/create/ defaults Porta = 0 — INVALID for any service",
            "You MUST set Porta = 50000 for lab nginx demo (LOCAL_PORT constant in this deck)",
            "Book weather demo uses port 8080 — same form, different port value",
            "Port 0 causes ServiceEnable failure or silent misconfiguration — always verify in list",
            "Prefer API if UI unclear: POST /v1/services with explicit port field in JSON body",
            "setup-wstun-demo.py script automates catalog creation with correct port",
        ]),

        ("section", "Hands-on — Demo A: book weather server", "run-weather-demo.sh"),

        ("hands_on", "Step 1 — Run verified weather demo script", [
            "$ cd training",
            "$ ./experiments/webservices/run-weather-demo.sh",
            "# Starts ch14/demos/weather_web_server.py inside LR on port 8088",
            "# Creates catalog weather-wot · ServiceEnable · writes weather-state.json",
            "Expected: OK http://{{VM_IP}}:<public_port>/sensors → HTTP 200",
        ]),

        ("image", "Weather server dashboard via WSTUN tunnel",
         "chapter14/weather-server-dashboard.png",
         "http://{{VM_IP}}:<public_port>/ — JSON /sensors from ch14 demo", "", True),

        ("hands_on", "Step 2 — Verify WoT sensor API", [
            "$ CLOUD=$(python3 -c \"import json; print(json.load(open('experiments/webservices/weather-state.json'))['cloud_port'])\")",
            "$ curl -s http://{{VM_IP}}:$CLOUD/sensors | python3 -m json.tool",
            "Expected fields: temperature, humidity, pressure, device=weather-station",
            "$ curl -X POST http://{{VM_IP}}:$CLOUD/led/toggle",
        ]),

        ("section", "Hands-on — Demo B: nginx infra smoke test", "setup-wstun-demo.py"),

        ("hands_on", "Step 3 — Run nginx WSTUN smoke test", [
            "$ .venv/bin/python experiments/webservices/setup-wstun-demo.py",
            "Creates lr-nginx-demo port 50000 · captures Horizon screenshots",
            "$ curl -v http://{{VM_IP}}:50002/",
            "Expected: HTTP 200 nginx welcome page",
        ]),

        ("image", "Horizon — Servizi list (port verified)",
         "chapter14/horizon-services-list.png",
         "http://{{VM_IP}}/horizon/iot/services/ — lr-nginx-demo port 50000", "", True),

        ("theory", "Service catalog REST schema (Ch.14)", [
            "POST /v1/services — body: name (string), port (integer), protocol (TCP|UDP)",
            "GET /v1/services/ — list all catalog entries with UUID and port fields",
            "Catalog is tenant-global — same service definition reused across multiple boards",
            "ServiceEnable on board creates board-specific tunnel instance with public_port",
            "DELETE /v1/services/{uuid} — remove catalog entry (boards must disable first)",
            "Port must match actual listening port inside LR container (50000 nginx / 8080 Flask)",
        ], "Ch.14 · IoTronic services API · listing create_service"),

        ("code", "Step 2 — ServiceEnable on board (API)",
         'curl -X POST http://{{VM_IP}}:8812/v1/boards/<BOARD_UUID>/services/lr-nginx-demo/action \\\n'
         '  -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \\\n'
         '  -d \'{"action":"ServiceEnable"}\'',
         "Response JSON includes public_port on iotronic-wstun (e.g. 50002)"),

        ("image", "Horizon — Boards with exposed service",
         "chapter14/horizon-boards-with-services.png",
         "Servizi column: lr-nginx-demo [TCP] 50000 → 50002", "", True),

        ("theory", "ServiceEnable response and port mapping (Ch.14)", [
            "Response public_port: host-accessible port on lab VM (50001–50100 range)",
            "Board column in Horizon shows: service_name [protocol] local_port → public_port",
            "Traffic flow: client → {{VM_IP}}:public_port → WSTUN → LR:local_port",
            "LR nginx (lab) or Flask (book) must be listening BEFORE ServiceEnable",
            "ServiceDisable action tears down tunnel — public_port returned to pool",
            "Multiple services on same board: separate catalog entries with different local ports",
        ], "Ch.14 · ServiceEnable · WSTUN port allocation"),

        ("hands_on", "Step 4 — Verify cloud endpoint with curl", [
            "$ curl -v http://{{VM_IP}}:50002/",
            "# nginx demo public_port — check wstun-state.json if different",
            "Expected: HTTP 200 + nginx welcome page from board LR container",
            "$ ./validate/validate-demo-ch14.sh && ./validate-lab-wstun.sh",
        ]),

        ("hands_on", "Step 5 — WSTUN troubleshooting logs", [
            "$ docker logs iotronic-wstun 2>&1 | tail -20",
            "$ docker logs lightning-rod 2>&1 | grep -i 'Cloud service'",
            "Look for: TCP server listening on assigned public port",
            "Common fix: recreate catalog entry if port was 0",
        ]),

        ("theory", "Book weather server — verified lab procedure (Ch.14)", [
            "Script run-weather-demo.sh copies ch14/demos/weather_web_server.py into LR container",
            "Lab port 8088 used because LR compose image reserves :8080 for WSTUN client stack",
            "Catalog entry weather-wot port 8088 · ServiceEnable → curl /sensors JSON via public_port",
            "Verified: HTTP 200 on /sensors with temperature, humidity, pressure fields",
            "Book hardware boards use port 8080 as documented in ch14/demos/README.md",
            "Repo: github.com/AssemblingSmartCPS/ch14",
        ], "Ch.14 demos/weather_web_server.py · weather-state.json"),

        ("image", "Horizon — Web Services panel (Designate path)",
         "chapter14/horizon-webservices-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/webservices/ — full WoT URL setup (optional tour)", "", True),

        ("theory", "Production WoT path — Designate + /etc/hosts (Ch.14)", [
            "Install/configure OpenStack Designate with public domain zone (example.com)",
            "Testing without real DNS: map example.com → {{VM_IP}} in /etc/hosts on client machine",
            "Enable WSM → service wot :8080 → https://wot.board-1.example.com/temperature",
            "NGINX terminates TLS — forwards to WSTUN tunnel — same machinery as port mapping",
            "Human-readable URLs enable WoT Find/Share layers (Ch.6) at scale",
            "Designate optional in Docker lab — WSTUN port path sufficient for training objectives",
        ], "Ch.14 · local domain simulation · Designate integration"),

        ("theory", "WoT security considerations (Ch.6 + Ch.14)", [
            "HTTPS at cloud edge — never expose raw board HTTP to public Internet in production",
            "Keystone authentication for IoTronic API — ServiceEnable requires valid token",
            "Board services should validate input on POST actuators (LED, GPIO) — prevent abuse",
            "Rate limiting at NGINX for public WSTUN endpoints under DDoS exposure",
            "Lab: HTTP acceptable on {{VM_IP}}:public_port for classroom — not production pattern",
            "Cross-reference Module E VN for network-layer security groups on overlay",
        ], "Ch.6 · Ch.14 security notes"),

        ("theory", "REST design for WoT resources (Ch.6 + Ch.14)", [
            "GET /temperature — read sensor property; idempotent, cacheable, safe method",
            "POST /led — actuate actuator with JSON body {\"state\": \"on\"} — non-idempotent action",
            "Content-Type: application/json for machine clients; text/html optional for dashboards",
            "HTTP status codes: 200 OK read, 201 Created action, 503 if sensor temporarily unavailable",
            "Book weather server returns JSON: {\"temperature\": 22.5, \"unit\": \"C\"} — WoT property pattern",
            "Lab nginx returns HTML welcome page — infra validation only; weather server is true WoT API",
        ], "Ch.6 RESTful Things · Ch.14 weather_web_server.py endpoints"),

        ("theory", "NGINX reverse proxy role in S4T WoT (Ch.6 §6.4 + Ch.14)", [
            "Cloud NGINX terminates TLS and routes Host header to correct board tunnel backend",
            "Location block per subdomain: wot.board-1.example.com → upstream WSTUN backend port",
            "Board-side nginx (lab :50000) or Flask (:8080) is origin server — NGINX is edge proxy",
            "WebSocket upgrade headers preserved for WSTUN tunnel establishment and maintenance",
            "Same NGINX instance serves Horizon UI and IoT service proxy — different server_name blocks",
            "Production: NGINX + Designate + WSTUN three-component path to Deviceless URL (Module I)",
        ], "Ch.6 §6.4 gateway architecture · Ch.14 NGINX integration"),

        ("theory", "Thing Descriptions and discovery (Ch.6 Find layer)", [
            "WoT Thing Description (TD): JSON-LD document listing properties, actions, events, schemas",
            "Well-known URI: /.well-known/wot-thing-description — automated discovery by mashup apps",
            "CoRE Link Format alternative for constrained devices — Link header in HTTP responses",
            "S4T Designate DNS enables stable TD URL: https://wot.board.example.com/td",
            "Find layer completes Access: clients discover API contract before invoking endpoints",
            "Lab WSTUN path skips Find (no DNS) — students should know production adds TD + DNS",
        ], "Ch.6 · Find layer · Thing Description W3C WoT spec cross-reference"),

        ("theory", "Service lifecycle — Enable, Disable, Update (Ch.14)", [
            "ServiceEnable: creates WSTUN tunnel, assigns public_port, starts forwarding traffic",
            "ServiceDisable: tears down tunnel, releases public_port back to pool 50001–50100",
            "Board must be Active before ServiceEnable — same prerequisite as plugin inject (Module A)",
            "Changing catalog port requires Disable → update catalog → re-Enable on affected boards",
            "Multiple services per board: separate catalog entries (lr-nginx-demo :50000, wot :8080)",
            "Horizon boards column shows all active service mappings per board for operational audit",
        ], "Ch.14 · service lifecycle · ServiceDisable listing"),

        ("theory", "WSTUN vs Designate — decision guide (Ch.14)", [
            "Use WSTUN port mapping: lab, demos, quick tests — http://{{VM_IP}}:public_port/path",
            "Use Designate DNS: production, human URLs, WoT Find/Share layers, Module I Deviceless",
            "Same ServiceEnable API — difference is only how clients construct the public URL",
            "Designate requires DNS zone + NGINX server_name config — more setup, better UX",
            "Book weather demo intended for Designate path — WSTUN port path is lab training shortcut",
            "Both paths traverse same WebSocket tunnel — WSTUNServer is shared infrastructure",
        ], "Ch.14 §14.3 · WSTUN vs Designate comparison table"),

        ("hands_on", "Step 5 — ServiceDisable cleanup (optional)", [
            "API: POST .../services/lr-nginx-demo/action with {\"action\":\"ServiceDisable\"}",
            "Verify Horizon boards column clears service mapping",
            "Re-Enable to confirm public_port may change — not guaranteed same port after recycle",
        ]),

        ("hands_on", "Step 6 — Validate WSTUN module", [
            "$ cd training && ./validate-lab-wstun.sh",
            "Script verifies catalog port, ServiceEnable state, and curl HTTP 200",
        ]),

        ("content", "Module F checklist", [
            "□ weather-wot service verified: curl /sensors → JSON HTTP 200 (run-weather-demo.sh)",
            "□ lr-nginx-demo port 50000 → public_port curl HTTP 200 (setup-wstun-demo.py)",
            "□ Board Servizi column shows both tunnel mappings",
            "□ Student can explain book port 8080 vs lab port 8088 (LR image constraint)",
            "□ Student can describe Designate path vs WSTUN port path",
            "□ ./validate/validate-all.sh Module F checks pass",
        ]),
    ]
