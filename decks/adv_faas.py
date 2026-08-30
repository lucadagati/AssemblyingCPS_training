"""Module I — FaaS & Deviceless (Ch.7)."""


def slides() -> list:
    return [
        ("title", "Module I — FaaS & the Deviceless Paradigm",
         "Ch.7 · Advanced · VM {{VM_IP}}",
         "Advanced · Ch.7 — FaaS & Deviceless · contrasts Modules B, C, F"),

        ("section", "Deviceless & serverless theory", "Ch.7 — before side-by-side plugin demos"),

        ("theory", "Deviceless paradigm (Ch.7)", [
            "Physical devices abstracted as composable virtual Web resources with stable DNS names",
            "Developers interact with Things via HTTP URIs — not device-specific SDKs or serial protocols",
            "Geographic distribution transparent: wot.sensor-barcelona.example.com just works",
            "Deviceless = operational realization of WoT vision (Ch.6) at Cloud Continuum scale",
            "S4T Module F WSTUN/Designate exposure is the lab step toward Deviceless naming",
            "Book abstract positions Deviceless as key enabler for programmable CPS infrastructure",
        ], "Ch.7 · The Deviceless paradigm · chapter abstract"),

        ("theory", "From devices to Web resources (Ch.7)", [
            "Traditional IoT: developer learns board SDK, GPIO libraries, firmware toolchain",
            "Deviceless: developer consumes OpenAPI/REST contract — implementation opaque",
            "DNS stability: service moves from board A to board B — URL unchanged for consumers",
            "Compose (Ch.6 layer): mashup apps combine Deviceless resources without owning hardware",
            "Stack4Things IoTronic + Designate + NGINX implement Deviceless naming infrastructure",
            "Module I connects abstract Ch.7 taxonomy to concrete Ch.14 plugin modes in lab",
        ], "Ch.7 · device abstraction · WoT cross-reference Ch.6"),

        ("theory", "PaaS vs FaaS vs Deviceless (Ch.7)", [
            "PaaS: long-running platform service — always-on process or container on cloud/edge",
            "FaaS: event-driven function — invoke, execute, return result, scale to zero between calls",
            "Deviceless: device capability exposed as callable Web resource with DNS name — not a function runtime per se",
            "OpenStack Qinling: serverless functions on OpenStack cloud infrastructure (Zun containers)",
            "OpenWhisk-Light referenced in book as lightweight FaaS research platform",
            "All three coexist in Cloud Continuum — choice depends on workload lifetime and trigger pattern",
        ], "Ch.7 · serverless on OpenStack · Qinling · OpenWhisk-Light"),

        ("theory", "FaaS characteristics in detail (Ch.7)", [
            "Event-triggered: HTTP request, message queue event, scheduled cron — not continuous loop",
            "Stateless execution: function instance holds no persistent state between invocations",
            "Scale to zero: no cost/resources when idle — cold start latency trade-off",
            "Managed runtime: platform handles packaging, scaling, logging — developer supplies handler code",
            "Billing model: per-invocation + execution duration — vs PaaS always-on provisioning",
            "Edge FaaS (Ch.7 + Ch.11): functions deployed near data sources in K3s/Knative substrate",
        ], "Ch.7 · FaaS properties · edge serverless discussion"),

        ("theory", "PaaS characteristics in detail (Ch.7)", [
            "Long-running service: process starts once, serves many requests over hours/days/months",
            "Stateful acceptable: in-memory caches, connection pools, persistent background threads",
            "Always-on cost: container/VM provisioned continuously — even during idle periods",
            "Edge PaaS example: environmental_data async plugin (Module C) — 30 s publish loop",
            "Docker plugin (Module B optional): deploys containerized service on edge on demand",
            "PaaS appropriate when continuous monitoring/actuation required — not one-shot queries",
        ], "Ch.7 · PaaS at the edge · Module C cross-reference"),

        ("theory", "Mapping book concepts to S4T lab demos (Ch.7 applied)", [
            "HelloName Plugin Call (Module B) ≈ FaaS-like: one shot invocation, immediate JSON result",
            "environmental_data async plugin (Module C) ≈ PaaS-like: continuous microservice loop",
            "Docker plugin run (Module B optional) ≈ deploying containerized PaaS on edge on demand",
            "WoT HTTP exposure via WSTUN (Module F) ≈ Deviceless: board service as Web resource",
            "Sync vs async plugin modes (Ch.14) directly encode FaaS-like vs PaaS-like behaviour",
            "Module I makes taxonomy explicit — students re-label demos they already executed",
        ], "Ch.7 applied to Part II labs · Ch.14 plugin modes"),

        ("theory", "Serverless at the continuum edge (Ch.7 + Ch.11)", [
            "Function-as-a-Service models extend toward edge nodes in Cloud Continuum architecture",
            "K8s + Knative or Qinling can host ephemeral functions near IoT data sources",
            "S4T callable sync plugins are stepping stone — no Qinling in current Docker lab compose",
            "Blueprint Module H K3s substrate enables future FaaS integration via Crossplane CRDs",
            "Ch.11 Type 1 experiments include serverless architectural paradigm category",
            "Research direction: IoTronic inject deploys function handler instead of long-running Worker",
        ], "Ch.7 + Ch.11 Type 1 serverless experiments"),

        ("theory", "Qinling and OpenStack serverless (Ch.7)", [
            "Qinling: OpenStack project for function lifecycle management on Zun containers",
            "Functions packaged as containers — triggered by HTTP or message bus events",
            "Integrates with Keystone auth, Designate DNS — full OpenStack ecosystem fit",
            "Not deployed in current training Docker compose — documented as research/production direction",
            "Would enable true scale-to-zero functions managed like other OpenStack services",
            "Deviceless DNS + Qinling functions = full Ch.7 vision operational on S4T stack",
        ], "Ch.7 · Qinling references · OpenStack serverless roadmap"),

        ("theory", "Zun — OpenStack container service (Ch.7)", [
            "Zun-api: REST/WSGI entry point from Horizon or CLI for container lifecycle.",
            "Zun-compute: agent on compute nodes — hides Docker runtime operations from users.",
            "Zun-wsproxy: interactive shell and log streaming into running containers.",
            "Zun-scheduler: filters (RAM, CPU, labels) select host for new container placement.",
            "Zun networking driver: assigns reachability — Neutron in cloud, IoTronic WSTUN at edge.",
            "Capsule ≈ Kubernetes Pod: runtime + sidecar + pause containers sharing network namespace.",
        ], "Ch.7 § Zun · fig:chap07:zun-system"),

        ("theory", "Deviceless edge reachability — Zun + WSTUN (Ch.7)", [
            "IoT nodes act as Zun compute hosts — containers run on boards, not only in datacenter.",
            "Standard Neutron overlay cannot reach NAT-bound edge capsules — custom driver required.",
            "New Zun networking driver maps each public cloud port to a remote container via WSTUN.",
            "HostnameFilter scheduler policy targets a specific board by name/id for function placement.",
            "Qinling runtime creation on edge: Qinling → Zun capsule → IoTronic tunnel → reachable URL.",
            "Same WSTUN infrastructure as Module F — Deviceless adds serverless function semantics on top.",
        ], "Ch.7 § Implementation aspects · fig:chap07:devless-cloud-arch"),

        ("theory", "Node-RED and flow-based Deviceless (Ch.7)", [
            "Node-RED provides visual flow programming — wires connect HTTP, MQTT, and function nodes.",
            "Deviceless extends flows across cloud and edge without installing Node-RED on every board.",
            "Qinling function nodes invoke edge runtimes — distributed logic with Web-native triggers.",
            "Contrasts with OpenWhisk-Light: limited to local-only triggers on a single node.",
            "Book use cases show remote wires linking cloud dashboards to edge sensor preprocessing.",
            "Module I conceptual bridge — lab uses sync/async plugins instead of Qinling functions today.",
        ], "Ch.7 § Flow-based development · Node-RED · sec:use-cases"),

        ("image", "Serverless-like vs long-running contrast",
         "diagrams/faas-contrast.png",
         "HelloName sync Plugin Call (FaaS-like) vs environmental async (PaaS-like)"),

        ("content", "Module I — learning objectives", [
            "Define Deviceless, FaaS, and PaaS from Ch.7 with S4T lab examples",
            "Execute side-by-side Demo 1 (HelloName Plugin Call) and Demo 2 (environmental Start)",
            "Articulate which book category each existing module demo represents",
            "Connect Module F WoT exposure to Deviceless Web resource naming",
            "Identify Qinling/K3s as future FaaS integration path (Ch.7 + Ch.11)",
        ]),

        ("content", "Module I — 35-minute timeline", [
            "0–15 min  — Ch.7 theory: Deviceless, FaaS, PaaS, Qinling, edge serverless",
            "15–18 min — DEMO GOAL review — no new infrastructure required",
            "18–28 min — HANDS-ON Demo 1: HelloName Plugin Call (FaaS-like)",
            "28–35 min — HANDS-ON Demo 2: environmental async (PaaS-like) + wrap-up",
        ]),

        ("demo", "Side-by-side demo goals (Ch.7 applied to lab)", [
            "Demo 1: HelloName Plugin Call — atomic invocation, zero persistent background state",
            "Demo 2: environmental_data Start — long-running loop, continuous InfluxDB time-series output",
            "Students label each demo: FaaS-like, PaaS-like, or Deviceless (Module F exposure layer)",
            "No new containers or plugins — reuses Modules B and C artefacts on {{VM_IP}} lab",
            "Discussion prompts: Which billing model fits each pattern? Which has cold start? Which is stateful?",
            "Connects abstract Ch.7 taxonomy to concrete Ch.14 plugin sync/async modes already learned",
        ]),

        ("section", "Hands-on Demo 1 — FaaS-like Plugin Call", "HelloName synchronous invocation"),

        ("hands_on", "Demo 1 — atomic Plugin Call (serverless-like)", [
            "Open http://{{VM_IP}}/horizon/iot/ — login {{HZ_CRED}}",
            "Plugins → HelloName (from Module B) → Plugin Call",
            '{"name": "FaaS-demo"}',
            "Single invocation → immediate JSON result — no background process persists",
            "Contrast: no Start/Stop lifecycle — function-equivalent behaviour",
        ]),

        ("image", "Horizon IoT — Plugins (sync Plugin Call)",
         "chapter14/horizon-plugins-dashboard.png",
         "Callable=ON → one-shot invocation · HelloName sync plugin", "", True),

        ("theory", "Why HelloName is FaaS-like (Ch.7 + Ch.14)", [
            "Dormant until Plugin Call trigger — no CPU consumed while idle on board",
            "Single input JSON → single output JSON — request/response function signature",
            "No persistent state between calls — each Plugin Call is independent invocation",
            "Execution duration: milliseconds — matches FaaS short-lived handler pattern",
            "Missing FaaS features in lab: auto-scale, cold start metrics, per-invocation billing",
            "Closest lab analog to Ch.7 FaaS without deploying Qinling infrastructure",
        ], "Ch.14 §14.1.2 sync pipeline · Ch.7 FaaS mapping"),

        ("section", "Hands-on Demo 2 — PaaS-like async service", "environmental_data continuous publisher"),

        ("hands_on", "Demo 2 — long-running async plugin (PaaS-like)", [
            "Start environmental_data plugin from Module C (or restart if stopped)",
            "Observe continuous InfluxDB writes every 30 s at http://{{VM_IP}}:8086",
            "Contrast: no Plugin Call per iteration — persistent _is_running background loop",
            "Stop/Interrupt required to halt — unlike one-shot HelloName Plugin Call",
        ]),

        ("image", "InfluxDB — continuous async output",
         "chapter15/influxdb-debug.png",
         "Time-series grows while plugin runs — PaaS-style always-on edge service"),

        ("theory", "Why environmental_data is PaaS-like (Ch.7 + Ch.15)", [
            "Long-running background thread — active for minutes/hours during class session",
            "Stateful loop: maintains sensor read schedule and InfluxDB connection context",
            "Always-on resource consumption on board while plugin Started — no scale to zero",
            "Continuous output stream — not event-triggered single response pattern",
            "Matches edge microservice/PaaS deployment model from Ch.15 environmental publisher",
            "Production: would run 24/7 on edge gateway — FaaS inappropriate for this pattern",
        ], "Ch.15 async environmental plugin · Ch.7 PaaS mapping"),

        ("theory", "Deviceless layer — Module F connection (Ch.7 + Ch.6)", [
            "Module F WSTUN exposes board HTTP service at {{VM_IP}}:public_port — Web resource URI",
            "Production Designate path: stable DNS name independent of board physical location",
            "Deviceless consumer: curl https://wot.board.example.com/temperature — no LR SDK needed",
            "FaaS handler behind Deviceless URL: function invoked via HTTP POST to named endpoint",
            "Three-layer stack: Deviceless (naming) + FaaS/PaaS (execution model) + WoT (API contract)",
            "Module I completes taxonomy: HelloName=FaaS-like, environmental=PaaS-like, WSTUN=Deviceless enabler",
        ], "Ch.7 Deviceless · Ch.6 WoT · Module F cross-reference"),

        ("section", "Wrap-up & future directions", "Qinling + K3s + Course Map link"),

        ("theory", "Future work — full Ch.7 vision on S4T (Ch.7 + Ch.11)", [
            "Qinling on OpenStack S4T: true scale-to-zero functions with Keystone auth",
            "Knative on Module H K3s: Kubernetes-native FaaS with auto-scaling pods",
            "Crossplane CRD: declare function + Deviceless DNS + board target in single YAML",
            "IoTronic inject: deploy function handler container instead of persistent Worker class",
            "Research papers cited in Ch.7 on edge serverless latency and cold-start optimization",
            "Current training lab: conceptual bridge complete — infrastructure evolution is next step",
        ], "Ch.7 · future directions · Ch.11 K3s substrate"),

        ("content", "Module I wrap-up checklist", [
            "□ Demo 1 executed: HelloName Plugin Call labelled FaaS-like by students",
            "□ Demo 2 executed: environmental_data Start labelled PaaS-like by students",
            "□ Student explains Deviceless connection to Module F WoT/WSTUN exposure",
            "□ Student identifies Qinling/K3s as production FaaS path (Ch.7 + Ch.11)",
            "Return to Course Map — full 9h path complete: A→I modules covered",
        ]),
    ]
