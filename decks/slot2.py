"""Module B — Slot 2: Plugins & services (Ch.14). Hand-authored theory + demo slides."""

from generate_slides import DOCKER_JSON, HELLO_PLUGIN


def slides() -> list:
    return [
        ("title", "Stack4Things Plugins & Edge Services",
         "Module B — IoTronic Plugins & Services · Ch.14 · 60 min\nLab VM: {{VM_IP}}",
         "Assembling Smart CPS · Part II"),

        ("section", "Chapter 14 overview", "Plugins · Fleet · Web services"),

        ("theory", "What Chapter 14 covers (abstract)", [
            "Chapter 14 examines how Stack4Things injects customized business logic directly into remote IoT nodes at the network edge.",
            "Plugins are modular, extensible units orchestrated by the Lightning-Rod agent on each board.",
            "The chapter distinguishes synchronous on-demand execution from asynchronous continuous background operation.",
            "Fleet management treats heterogeneous devices as coordinated logical groups for bulk operations.",
            "Web services integration exposes board HTTP endpoints over the public Web without manual port forwarding.",
            "Together these capabilities turn passive edge nodes into programmable, remotely managed cyber-physical assets.",
        ], "Ch.14 abstract · Stack4Things Services"),

        ("content", "Module B — 60-minute timeline", [
            "0–10 min  — Plugin theory: sync vs async, lifecycle, oslo_log centralized logging",
            "10–20 min — Worker anatomy, Plugin Manager runtime, HelloName listing walkthrough",
            "20–40 min — HANDS-ON: create, inject, and Plugin Call sync HelloName plugin",
            "40–50 min — Optional: Docker lifecycle plugin — run alpine container at the edge",
            "50–60 min — Fleet preview, K3s lifecycle theory, web services preview → Module C",
        ]),

        ("content", "Prerequisites, objectives & deliverables", [
            "Requires Module A complete — board must show Active in Horizon before any plugin demo.",
            "Create a synchronous HelloName plugin using the standard Python Worker class template.",
            "Inject the plugin on the Active board and invoke it via Plugin Call from Horizon.",
            "Verify the greeting in the Horizon result panel and in Lightning-Rod oslo_log output.",
            "Optional deliverable: Docker run alpine JSON result with container id and short_logs.",
            "Horizon login: {{HZ_CRED}} · LR UI: http://{{VM_IP}}:1474 ({{LR_CRED}}).",
        ]),

        ("section", "Plugin theory — motivation", "Why edge logic matters in S4T"),

        ("theory", "Why plugins? — extending the edge (Ch.14 §14.1)", [
            "Traditional firmware updates require physical access or costly over-the-air reflashing of each device.",
            "Stack4Things plugins encapsulate sensing, actuation, local compute, or protocol forwarding as deployable Python modules.",
            "Operators upload plugin source to the IoTronic repository and inject it onto one board or an entire fleet remotely.",
            "Plugin logic executes inside Lightning-Rod on the board, close to sensors and actuators where latency is lowest.",
            "The model bridges low-level hardware control on the edge and high-level cloud orchestration through IoTronic APIs.",
            "Domain-specific behavior — environmental monitoring, container management, K3s join — becomes software-defined infrastructure.",
        ], "Ch.14 §14.1 · Plugins in Stack4Things"),

        ("theory", "Plugin-based architecture — separation of concerns", [
            "IoTronic holds the plugin repository, metadata, injection state, and REST/Horizon management APIs in the cloud.",
            "Lightning-Rod loads the Worker class, passes runtime parameters, and supervises execution on the edge node.",
            "Each plugin is an independent unit: deploy, update, interrupt, or remove without restarting the full LR agent.",
            "Callable flag in Horizon marks synchronous plugins; non-callable plugins run as long-lived background workers.",
            "Results flow back through q_result queues to IoTronic, where Horizon and REST consumers read them.",
            "This mirrors the I/Ocloud idea from Chapter 4 — physical capability exposed as a remotely invocable function.",
        ], "Ch.14 · plugin management model · Ch.4 I/Ocloud"),

        ("theory", "Lightning-Rod Plugin Manager runtime", [
            "The Plugin Manager on each board loads the Python Worker subclass into an isolated execution context.",
            "Constructor signature is fixed: __init__(self, uuid, name, q_result, params=None) calling super on Plugin.Plugin.",
            "self.params carries the JSON dict from a Plugin Call in synchronous mode or startup configuration in async mode.",
            "self.q_result is a queue where run() puts return values that IoTronic forwards to the cloud caller or dashboard.",
            "Execution modes include callable (sync on demand), onboot (start when LR starts), and periodic (scheduled intervals).",
            "The run() method is the single entry point — all plugin business logic lives inside it or methods it calls.",
            "LR 0.4.17 requires the Python class to be named Worker regardless of the display name shown in Horizon.",
        ], "Ch.14 · lst:plugin-skeleton · Plugin Manager"),

        ("section", "Asynchronous plugins", "Continuous edge workloads · Ch.14 §14.1.1"),

        ("theory", "Asynchronous plugins — purpose and pipeline (Ch.14 §14.1.1)", [
            "Asynchronous plugins run continuously or at fixed intervals without an explicit cloud trigger for each iteration.",
            "They remain active in the background until an operator sends Stop or Interrupt from IoTronic or Horizon.",
            "The canonical pipeline is: Lightning-Rod → Sensor Plugin → Database → Visualization dashboard.",
            "Environmental monitoring, weather stations, and air-quality streams are the primary motivating use cases.",
            "Module C (Chapter 15) deploys the environmental_data async publisher writing CSV rows to InfluxDB every 30 seconds.",
            "Async plugins use while self._is_running loops with time.sleep intervals between acquisition cycles.",
        ], "Ch.14 §14.1.1 · asynchronous plugins"),

        ("theory", "Asynchronous plugins — weather station example", [
            "The book's weather station plugin reads temperature, humidity, and barometric pressure from board sensors every 60 seconds.",
            "Each reading is timestamped, optionally enriched with device metadata, and written to a local or remote time-series store.",
            "Grafana or CKAN portals consume the stored series for operator dashboards and open-data publication.",
            "Because the plugin runs autonomously, network interruptions can be handled with local buffering and resume logic.",
            "Horizon shows async plugins with Callable = OFF; activation uses Start rather than Plugin Call.",
            "Interrupt stops the _is_running loop cleanly so the board can accept updated plugin code on the next inject.",
            "Listing reference: lst:plugin-async and ch14/plugins/asynchronous/weather_station_plugin.py.",
        ], "Ch.14 · weather station async listing"),

        ("theory", "Asynchronous plugins — when to choose async mode", [
            "Choose async when data must be collected on a schedule independent of human or API-driven triggers.",
            "Choose async when the workload is long-running and would exceed reasonable synchronous call timeouts.",
            "Choose async when multiple samples must be aggregated before cloud upload to reduce bandwidth and cost.",
            "Do not use async for one-shot diagnostics, GPIO toggles, or Docker operations that need immediate JSON responses.",
            "Async plugins may still push interim results to q_result for live monitoring, but primary output is often direct DB writes.",
            "State persistence — e.g. last_index.state in Ch.15 — enables fault-tolerant resume after restart or crash.",
        ], "Ch.14 §14.1.1 · async vs sync decision guide"),

        ("section", "Synchronous plugins", "On-demand edge microservices · Ch.14 §14.1.2"),

        ("theory", "Synchronous plugins — purpose and pipeline (Ch.14 §14.1.2)", [
            "Synchronous plugins remain dormant on the board until explicitly invoked by a Plugin Call from IoTronic.",
            "Each invocation runs run() exactly once, places the result on q_result, and returns control to the Plugin Manager.",
            "The pipeline is: Cloud Request → IoTronic Plugin Call → Lightning-Rod executes Worker → result returned to caller.",
            "They behave like callable microservices embedded on the IoT board, addressable via Horizon UI or REST API.",
            "Use cases include instant sensor reads, GPIO or LED control, Docker container lifecycle, and K3s cluster join/status.",
            "Horizon Create Plugin form sets Callable = ON to register the plugin in synchronous mode.",
        ], "Ch.14 §14.1.2 · synchronous plugins"),

        ("theory", "Synchronous plugins — HelloName as canonical example", [
            "HelloName reads a name parameter from self.params and returns a personalized greeting string.",
            "If name is omitted, the plugin defaults to User — demonstrating defensive parameter handling on the edge.",
            "LOG.info writes the same message through oslo_log for centralized traceability in production deployments.",
            "The entire request–response cycle typically completes in sub-second time over the WAMP control channel.",
            "Listing lst:plugin-sync is the reference implementation used in today's hands-on lab block.",
            "Once HelloName works, the same inject-and-call pattern applies to LED control and Docker lifecycle plugins.",
        ], "Ch.14 · lst:plugin-sync · hello_name_plugin"),

        ("theory", "Orchestrator agent lifecycle plugin (Ch.14 §14.1.3)", [
            "Separate from application Workers — manages board-side orchestrator agent state.",
            "Listing lst:plugin-orchestrator documents join/status/leave operations for edge agents.",
            "Used when LR must coordinate with external orchestration platforms beyond IoTronic alone.",
            "Distinct from K3s lifecycle plugin — different privilege and API surface.",
            "Not exercised in core lab — documented for completeness against book §14.1.3.",
            "Shows plugin model generality: any board-side Python logic can become a Worker.",
        ], "Ch.14 §14.1.3 · orchestrator agent lifecycle listing"),

        ("theory", "GPIO and LED control plugin (Ch.14)", [
            "Book web-services example reads /sys/class/gpio and toggles LED via POST /led.",
            "Hardware-facing WoT: REST endpoint maps to physical actuator on Raspberry Pi board.",
            "Contrasts with HelloName (pure software) and environmental (database publisher) plugins.",
            "Requires LR with GPIO access — Docker lab simulates HTTP; hardware pilots use real pins.",
            "Same inject + ServiceEnable path as weather_web_server.py for public WoT exposure.",
            "Connects Module B plugin model to Module F GPIO/LED endpoints in ch14 demos.",
        ], "Ch.14 §14.3 · GPIO weather server · demos/weather_web_server.py"),

        ("theory", "Synchronous plugins — parameter contracts and REST", [
            "Plugin Call accepts a JSON object whose keys map directly to self.params inside Worker.run().",
            "Horizon provides a Call dialog; equivalent automation uses IoTronic REST endpoints on the Conductor API.",
            "Input parameter JSON schemas can be declared at plugin creation time to document expected Call payloads.",
            "Errors inside run() should be logged with LOG.error and returned as structured JSON on q_result when possible.",
            "Synchronous plugins do not use self._is_running loops unless the operation itself is intentionally long.",
            "Callable plugins can be injected on multiple boards and invoked independently with different params per board.",
        ], "Ch.14 §14.1.2 · Plugin Call semantics"),

        ("image", "Plugin pipelines — sync vs async",
         "diagrams/plugin-sync-async.png",
         "Theory diagram — pairs HelloName (sync) with Ch.15 environmental publisher (async)"),

        ("section", "Plugin lifecycle", "Seven steps from development to removal"),

        ("theory", "Plugin lifecycle — steps 1–2: develop and register", [
            "Step 1 — Develop: write Python source following the S4T skeleton with Worker class, oslo_log, and run() method.",
            "Test logic locally where possible using a mock q_result queue before uploading to IoTronic.",
            "Step 2 — Create: upload the plugin to the IoTronic repository via Horizon Create Plugin or Conductor REST API.",
            "Provide display name, description, full source code, and Callable flag (ON = sync, OFF = async).",
            "Optional input-parameter JSON schema documents Plugin Call fields for synchronous plugins.",
            "The plugin receives a repository UUID; it is not yet running on any board until injection.",
            "Book listings: lst:plugin-skeleton (template), lst:plugin-sync, lst:plugin-docker, lst:plugin-k3s-lifecycle.",
        ], "Ch.14 · plugin lifecycle · steps 1–2"),

        ("theory", "Plugin lifecycle — steps 3–4: inject and execute", [
            "Step 3 — Inject: associate the repository plugin with a target board (or fleet) from Horizon Boards → Actions.",
            "Injection copies plugin metadata and source to the edge; Lightning-Rod acknowledges via WAMP messaging.",
            "Step 4 — Execute: for sync plugins, use Plugin Call with JSON params; for async, use Start from Horizon or API.",
            "Sync execution is single-shot; async execution enters the background loop until Stop or Interrupt.",
            "IoTronic tracks injection state per board so operators see which plugins are attached and running.",
            "Fleet-level inject deploys the same plugin to every member board in one coordinated operation (Ch.14 §14.2).",
        ], "Ch.14 · plugin lifecycle · steps 3–4"),

        ("theory", "Plugin lifecycle — steps 5–7: update, interrupt, remove", [
            "Step 5 — Update: push revised Python source to the repository and re-inject or hot-update on connected boards.",
            "Remote update avoids truck rolls — critical for large urban deployments like TOO(L)SMART in Chapter 15.",
            "Step 6 — Interrupt: for async plugins, signal _is_running = False to stop the loop without removing the injection.",
            "Interrupt is preferred over kill when the plugin maintains state files or open database connections.",
            "Step 7 — Remove: detach the plugin from the board; Lightning-Rod cleans up execution context and resources.",
            "Full lifecycle control — create, inject, execute, update, interrupt, delete — is available from Horizon and REST.",
        ], "Ch.14 · plugin lifecycle · steps 5–7"),

        ("section", "Structured logging", "oslo_log and centralized observability"),

        ("theory", "oslo_log in plugins — pattern and purpose (Ch.14–15)", [
            "Every production plugin imports from oslo_log: from oslo_log import log as logging; LOG = logging.getLogger(__name__).",
            "LOG.info, LOG.debug, LOG.warning, and LOG.error provide structured, level-filtered messages from edge execution.",
            "Using the OpenStack logging stack ensures consistent formatting across IoTronic cloud services and Lightning-Rod.",
            "Plugin authors should log entry parameters, major state transitions, and errors — never silent failure on the edge.",
            "HelloName demonstrates the minimum viable pattern: LOG.info(message) alongside self.q_result.put(message).",
            "Docker and environmental plugins extend this with operation names, container ids, and InfluxDB write confirmations.",
        ], "Ch.14–15 · oslo_log pattern · lst:plugin-sync"),

        ("theory", "Centralized logging — production vs lab (Ch.14–15)", [
            "In production Stack4Things deployments, Lightning-Rod log streams forward to IoTronic centralized logging service.",
            "Operators query logs across all boards from the cloud without SSH access to individual edge nodes.",
            "Multi-tenant deployments isolate log streams per tenant/project following OpenStack Keystone boundaries.",
            "In the training lab, logs are visible via: docker compose logs lightning-rod | grep Hello (or environmental).",
            "Centralized logging is infrastructure observability — distinct from HTTP services exposed via WSTUN or Designate DNS.",
            "Chapter 15 environmental plugin uses the same oslo_log pattern for each CSV row sent to InfluxDB.",
        ], "Ch.15 § logging infrastructure · Ch.14 Docker plugin traceability"),

        ("theory", "Logging vs web-exposed services — do not conflate", [
            "Plugin logs answer: did the edge logic run, with what parameters, and did it succeed or throw?",
            "Web services answer: can an external HTTP client reach a board-local port through DNS or WSTUN tunnels?",
            "The weather_web_server.py demo (Ch.14 §14.3) exposes GET /sensors — that is a web service, not a log stream.",
            "Docker plugin returns JSON on q_result; LOG.info captures the same facts for audit trails.",
            "When debugging Plugin Call failures, check both Horizon result panel and LR container logs in parallel.",
            "Module F extends web services with WSTUN port forwarding; today's focus is plugin execution and logging.",
        ], "Ch.14 §14.3 vs logging · Module F handoff"),

        ("section", "Hands-on — HelloName sync plugin", "Listing lst:plugin-sync · Callable = ON"),

        ("demo", "HelloName — learning outcomes", [
            "Prove that the cloud can invoke customized edge logic on demand with sub-second turnaround over WAMP.",
            "Prove that Plugin Call JSON parameters reach Worker.run() as self.params and drive business logic.",
            "Prove that results return through q_result and appear in the Horizon Plugin Call result panel.",
            "Prove that oslo_log emits the same message inside the Lightning-Rod container for operator verification.",
            "Establish the inject-and-call workflow reused by Docker lifecycle, LED control, and fleet bulk deploy in later modules.",
        ]),

        ("image", "UML sequence — Sync Plugin Call (Module B)",
         "diagrams/seq-plugin-sync.png",
         "Inject → Plugin Call → Conductor → Crossbar → Worker.run() → result"),

        ("content", "Plugin skeleton — FIXED section (do not change)", [
            "from iotronic_lightningrod.modules.plugins import Plugin",
            "from oslo_log import log as logging",
            "LOG = logging.getLogger(__name__)",
            "class Worker(Plugin.Plugin):  # name MUST be Worker in LR 0.4.17",
            "    def __init__(self, uuid, name, q_result, params=None):",
            "        super(Worker, self).__init__(uuid, name, q_result, params)",
        ]),

        ("content", "Plugin skeleton — USER section (your logic in run)", [
            "def run(self):",
            "    person_name = self.params.get('name', 'User')",
            "    message = f'Hello {person_name}'",
            "    LOG.info(message)",
            "    self.q_result.put(message)",
            "Only the run() body and helper methods belong in the USER section — keep FIXED imports and class name.",
        ]),

        ("warn", "Worker class name + ch14 repository fix", [
            "Lightning-Rod 0.4.17: the Python class MUST be named Worker — not HelloNamePlugin or any display alias.",
            "The dashboard plugin display name (HelloName) is independent of the Python class identifier.",
            "BUG: upstream ch14 hello_name_plugin.py uses HelloNamePlugin — injection will fail silently or error.",
            "Use the corrected file: training/ch14-fixed/plugins/synchronous/hello_name_plugin.py",
            "If Plugin Call returns empty, verify class name, injection status, and board Active state in that order.",
        ]),

        ("code", "HelloNamePlugin — listing lst:plugin-sync", HELLO_PLUGIN,
         "Paste in Create Plugin form. Set Callable = ON."),

        ("content", "Create Plugin form — field by field", [
            "Horizon → IoT → Plugins → + Create Plugin.",
            "Plugin Name: HelloName — display label in repository and Call dialog.",
            "Description: optional — e.g. synchronous greeting demo for Module B.",
            "Source: paste full Python Worker code from the listing slide.",
            "Callable: ✓ ON — marks plugin as synchronous and enables Plugin Call button.",
            "Input parameters: optional JSON schema documenting the name field for callers.",
        ]),

        ("image", "Horizon IoT — Plugins panel (live)",
         "chapter14/horizon-plugins-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/plugins/", "", True),

        ("hands_on", "Step 1 — Create HelloName plugin (10 min)", [
            "Open http://{{VM_IP}}/horizon — login {{HZ_CRED}}.",
            "Navigate IoT → Plugins → + Create Plugin.",
            "Paste from: training/ch14-fixed/plugins/synchronous/hello_name_plugin.py (NOT upstream ch14).",
            "Repo: github.com/AssemblingSmartCPS/ch14 · set Callable = ON · class must be Worker.",
            "Verify: ./validate/validate-demo-ch14.sh",
        ]),

        ("image", "Horizon IoT — Boards panel (inject target)",
         "chapter13/horizon-boards-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/ — select Active board → Actions → Inject Plugin", "", True),

        ("hands_on", "Step 2 — Inject plugin on board (5 min)", [
            "Horizon → IoT → Boards → select your Active board from Module A.",
            "Actions → Inject Plugin → choose HelloName from repository.",
            "Confirm injection — plugin is now attached to the board edge agent.",
            "Board must remain Active; re-check LR Status at http://{{VM_IP}}:1474 if inject fails.",
        ]),

        ("code", "Step 3 — Plugin Call JSON", '{"name": "YourName"}',
         'Default if name omitted: "User" · Book example uses {"name": "Messina"}'),

        ("hands_on", "Step 3 — Plugin Call and verify (10 min)", [
            "Horizon → Plugins → HelloName → Call (or board Actions → Call Plugin).",
            'Paste JSON: {"name": "Messina"} — replace with your own name to personalize.',
            "Check Horizon result panel — expect: Hello Messina (or Hello YourName).",
            "Verify LR logs: docker compose logs lightning-rod 2>&1 | grep Hello",
        ]),

        ("image", "Lightning-Rod — Status (plugin runtime)",
         "chapter13/lr-dashboard-status.png",
         "http://{{VM_IP}}:1474 — Connected board + plugin activity in LR logs", "", True),

        ("theory", "Sync pipeline — operational flow step by step", [
            "Step A: operator triggers Plugin Call in Horizon with JSON payload.",
            "Step B: IoTronic Conductor validates the request and sends a WAMP command to Lightning-Rod.",
            "Step C: LR Plugin Manager loads the injected Worker class and binds self.params from the Call JSON.",
            "Step D: Worker.run() executes once, writes LOG.info, and puts the greeting string on q_result.",
            "Step E: IoTronic receives the result and displays it in Horizon; REST API exposes the same payload.",
            "Any failure in steps B–D surfaces as empty result, LR error log, or WAMP disconnect on Status page.",
        ], "Ch.14 §14.1.2 · sync operational flow"),

        ("content", "Expected HelloName output and troubleshooting", [
            "Horizon Plugin Call result panel: Hello Messina (or your chosen name).",
            "LR container log line: INFO Hello Messina — confirms oslo_log path works.",
            "Empty result → check Worker class name is exactly Worker, not HelloNamePlugin.",
            "No log line → plugin not injected or board not Active; re-run Module A onboarding.",
            "WAMP error → confirm LR Configuration uses wss://crossbar:8181 inside Docker network.",
        ]),

        ("section", "Optional — Docker plugin at edge", "Ch.14 §14.1.4 · container lifecycle"),

        ("theory", "Docker management plugin — design (Ch.14 §14.1.4)", [
            "The Docker lifecycle plugin uses docker.from_env() — the official Python SDK talking to the host Docker daemon.",
            "Plugin Call JSON drives operations: run, stop, remove, and inspect on named containers.",
            "run pulls the image if missing, optionally removes an existing same-name container, starts detached, and returns status.",
            "This enables deploying containerized microservices on edge boards without SSH to each device.",
            "Fleet-wide inject can launch the same monitoring sidecar on every board in a coordinated batch.",
            "Listing reference: lst:plugin-docker · ch14/plugins/synchronous/docker_lifecycle_plugin.py.",
        ], "Ch.14 §14.1.4 · Docker plugin listing"),

        ("theory", "Docker plugin — lab prerequisites and security", [
            "Lightning-Rod must reach /var/run/docker.sock on the host — enabled by training lab overlay mount.",
            "Verify: docker exec lightning-rod ls /var/run/docker.sock — file must exist inside LR container.",
            "Install SDK if missing: docker exec lightning-rod pip install docker",
            "Granting Docker socket access is powerful — production deployments must sandbox and audit plugin code.",
            "Returned JSON includes status, container id, name, and short_logs tail for immediate verification.",
            "stop and remove operations use container_name from params — same field as run for consistency.",
        ], "Ch.14 · Docker plugin · lab overlay docker-compose.lab.yml"),

        ("demo", "Docker plugin — learning outcomes", [
            "Prove that synchronous plugins can orchestrate host Docker daemon operations from a Plugin Call JSON payload.",
            "Prove that alpine container starts on the board host and returns id, status, and log tail without SSH.",
            "Prove that edge containerization complements plugin model — microservices beside Python Worker logic.",
            "Optional only — skip if time is short; HelloName deliverable is sufficient for Module B completion.",
        ]),

        ("code", "Docker PluginCall — run alpine container", DOCKER_JSON,
         "Fields: operation, image, container_name, command, auto_remove"),

        ("hands_on", "Docker plugin demo — optional steps (15 min)", [
            "1. docker exec lightning-rod ls /var/run/docker.sock — confirm socket mount.",
            "2. docker exec lightning-rod pip install docker  (if ImportError on first call).",
            "3. Create and inject Docker lifecycle plugin from ch14 listing; Callable = ON.",
            "4. Plugin Call with JSON above → verify status running, container id, short_logs echo line.",
        ]),

        ("section", "Fleet, K3s & web services preview", "Theory for Modules D, F, and H"),

        ("theory", "Fleet abstraction — coordinated edge groups (Ch.14 §14.2)", [
            "A fleet is a tenant-aware logical collection of boards — not merely a UI label or tag.",
            "Devices grouped by operational intent act in unison: same plugin, same config, same data collection schedule.",
            "Horizon Fleets panel lists fleets; each fleet has a Plugins tab for bulk inject and lifecycle operations.",
            "Coordinated ops reduce administrative overhead when managing dozens or hundreds of urban sensor stations.",
            "Fleet health metrics include device availability percentage, error rates, and data quality across members.",
            "Full hands-on with three boards and fleet Hello inject: Module D (ModuleD_MultiBoard deck).",
        ], "Ch.14 §14.2 · fig:fleetpanel · FLEET_MANAGEMENT.md"),

        ("theory", "Fleet operations — bulk deploy pattern", [
            "Create fleet in Horizon with name and description tied to your OpenStack tenant/project.",
            "Associate Active boards as fleet members — heterogeneous device types can share one fleet.",
            "Inject Plugin on fleet deploys the repository plugin to every member in one action.",
            "Sync plugins still require per-board or API-driven Plugin Call unless a orchestration layer batches calls.",
            "Async plugins are started fleet-wide — environmental monitoring on all stations simultaneously.",
            "Book example: weather-monitoring-fleet with shared alert thresholds for temperature and humidity.",
        ], "Ch.14 §14.2 · fleet-level plugin deployment"),

        ("image", "Horizon IoT — Fleets panel",
         "chapter14/horizon-fleets-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/fleets/"),

        ("theory", "K3s lifecycle plugin — theory only (Ch.14 §14.1.5)", [
            "The K3s plugin is synchronous: operations join, status, and leave against a Kubernetes edge cluster.",
            "join installs a K3s agent on the board pointing at server endpoint URL and cluster join token.",
            "status reports whether the node is registered and ready in the cluster control plane.",
            "leave removes the agent cleanly — enabling dynamic scale-out and scale-in of IoT nodes as K8s workers.",
            "Requires root privileges, working K3s server, and network reachability — not part of the 3-hour core lab.",
            "Hands-on deferred to Module H (Blueprint + K3s) · listing lst:plugin-k3s-lifecycle.",
        ], "Ch.14 §14.1.5 · lst:plugin-k3s-lifecycle"),

        ("theory", "K3s at the edge — why it matters for smart CPS", [
            "Kubernetes at the edge standardizes packaging, scheduling, and health checks for containerized edge apps.",
            "S4T plugins bridge IoTronic fleet orchestration with K3s node lifecycle without manual SSH provisioning.",
            "Blueprint (Chapter 11) and Crossplane provider patterns extend this to declarative GitOps in advanced modules.",
            "Join token and server URL arrive as Plugin Call JSON params — same contract as HelloName and Docker plugins.",
            "Production smart-city stacks combine LR plugins for sensors with K3s for heavier analytics containers.",
            "Do not attempt K3s join in today's lab VM — theory only to connect Ch.14 listings to Module H roadmap.",
        ], "Ch.14 §14.1.5 · Module H preview"),

        ("theory", "Web services preview — exposing board HTTP (Ch.14 §14.3)", [
            "Stack4Things Web Services expose IoT HTTP endpoints on the public Web without manual router port forwarding.",
            "Designate DNS-as-a-Service assigns a subdomain per board — e.g. weather.board-1.example.com.",
            "NGINX reverse proxy and WebSocket tunnels route HTTPS requests to the board local service port.",
            "Book demo: weather_web_server.py serves GET /sensors, GET /led/status, POST /led/toggle on port 8080.",
            "Connects to Web of Things theory in Chapter 6 — physical sensors as REST resources on the global Web.",
            "Full WSTUN lab demo without Designate DNS: Module F (ModuleF_WebServices_WoT deck).",
        ], "Ch.14 §14.3 · WEB_SERVICES_INTEGRATION.md"),

        ("theory", "Web services — weather station WoT endpoints", [
            "GET /sensors returns JSON with timestamp, temperature, humidity, and pressure readings.",
            "GET /led/status reports actuator state; POST /led/toggle flips GPIO-driven LED for remote actuation.",
            "Horizon Web Services Manager registers service name and local port per board for tunnel establishment.",
            "WSTUN lab alternative maps cloud public_port (50001–50100) to board local port without DNS registration.",
            "Web-exposed services are long-lived HTTP servers — distinct from one-shot synchronous plugin calls.",
            "Service catalog + ServiceEnable workflow documented in Module F with nginx demo on LR port 50000.",
        ], "Ch.14 · demos/weather_web_server.py · Ch.6 WoT"),

        ("image", "Horizon IoT — Boards with services (preview)",
         "chapter14/horizon-boards-with-services.png",
         "http://{{VM_IP}}/horizon/iot/ — web services attach to Active boards · Module F hands-on"),

        ("content", "Module B checklist and handoff to Module C", [
            "□ HelloName Plugin Call returns Hello <name> in Horizon and LR logs.",
            "□ (Optional) Docker run alpine succeeded with container id in JSON result.",
            "Deliverable: Plugin Call screenshot or docker compose logs lightning-rod | grep Hello snippet.",
            "Next: Module C — async environmental publisher + InfluxDB time-series (Ch.15).",
            "Run validation: cd training && ./validate-lab.sh before starting Module C.",
        ]),
    ]
