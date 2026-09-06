"""Module A — Slot 1: Deploy I/Ocloud (Ch.4 + Ch.13). Hand-authored theory + demo slides."""


def slides() -> list:
    return [
        ("title", "Live Deploy — Stack4Things I/Ocloud",
         "Module A — Deploy Stack4Things I/Ocloud · Ch.4 + Ch.13 · 60 min\n"
         "Lab host: {{VM_IP}} — replace with your machine IP",
         "Assembling Smart CPS · Part II"),

        ("section", "Context", "Where this lab sits in the book"),

        ("theory", "Part I vs Part II — reading map (1/2)", [
            "Part I (Chapters 1–12) establishes the theoretical foundations of the cloud continuum, "
            "the I/Ocloud paradigm, the Web of Things, and the Blueprint methodology for smart CPS.",
            "Part II (Chapters 13–21) moves from architecture to practice: deploy Stack4Things, "
            "inject plugins, build urban services, and study real case studies.",
            "Module A is the mandatory entry point for all Part II hands-on work — without a running "
            "I/Ocloud and an Active board, Modules B through I cannot proceed.",
            "Today's session combines Chapter 4 (why Stack4Things exists) with Chapter 13 "
            "(how to deploy it reproducibly using Docker Compose).",
            "The book authors (the book authors — MDSLab, University of Messina) "
            "designed S4T as an OpenStack extension for IoT fleet management.",
            "By the end of this hour you will have reproduced the S4T testbed that every subsequent "
            "chapter assumes as its starting environment.",
        ], "Book Introduction · Part I / Part II"),

        ("theory", "Part I vs Part II — reading map (2/2)", [
            "Chapter 4 introduces the I/Ocloud as an architectural abstraction that elevates sensors, "
            "actuators, and edge devices into first-class programmable cloud resources.",
            "Chapter 13 operationalises that vision: clone the IoTronic repository, launch containers, "
            "register a virtual board, and verify cloud-to-edge connectivity.",
            "Module B (Ch.14) will inject synchronous and asynchronous plugins onto the board you "
            "register today.",
            "Module C (Ch.15) will stream environmental sensor data from an async plugin into InfluxDB.",
            "The training lab uses Docker-only deployment instead of the book's VirtualBox VM path — "
            "same services, faster provisioning, identical learning outcomes.",
            "Keep the distinction clear: theory from Ch.4 explains *why*; Ch.13 explains *how* to deploy.",
        ], "Ch.4 abstract · Ch.13 abstract"),

        ("content", "Module A — learning objectives", [
            "Clone the ch13 repository and start the full S4T stack with Docker Compose plus the lab overlay.",
            "Verify the IoTronic Conductor REST API responds and the Horizon dashboard is reachable.",
            "Register a virtual board in Horizon and configure Lightning-Rod to reach Active state.",
            "Deliverable: screenshot of board Active in Horizon + successful API curl against :8812.",
            "Run training/validate-lab.sh to confirm the environment is ready for Module B.",
        ]),

        ("content", "60-minute timeline", [
            "0–5 min   — Environment check (docker, RAM, git clone)",
            "5–15 min  — Theory: I/Ocloud architecture, services, Docker rationale",
            "15 min    — START docker compose (first boot takes 15–25 min)",
            "15–40 min — Continue theory while stack boots; monitor container health",
            "40–55 min — Horizon login, board create, Lightning-Rod configuration",
            "55–60 min — Confirm Active board + handoff checklist to Module B",
        ]),

        ("section", "Chapter 4 — I/Ocloud foundations", "Why Stack4Things exists"),

        ("theory", "Integrating IoT and the cloud (Ch.4 §4.1)", [
            "The proliferation of embedded smart devices across cities and industries makes vertical "
            "ad-hoc solutions ineffective at scale.",
            "IoT and cloud integration is presented in the book as a winning strategy to manage both "
            "the volume of data and the number of connected devices.",
            "Rather than inventing new infrastructure tooling, the authors propose extending OpenStack — "
            "the de-facto open-source IaaS platform — toward Cyber-Physical Systems.",
            "OpenStack already manages virtualised compute and storage; Stack4Things extends it to manage "
            "sensor- and actuator-hosting nodes at the network edge.",
            "On the board side the reference platforms are open-source devices such as 4rancino and "
            "Arduino YUN, running Linux distributions like Arancino OS on the MPU.",
            "The I/Ocloud vision treats physical I/O pins and connected transducers as cloud-manageable "
            "resources, not isolated firmware silos.",
        ], "Ch.4 § Integrating IoT and the cloud"),

        ("theory", "I/Ocloud design considerations (Ch.4 §4.1.1)", [
            "The I/Ocloud extends OpenStack's virtual infrastructure manager to encompass IoT devices "
            "as programmable entities within a unified cloud-native ecosystem.",
            "Unlike rigid predefined schemes for mixing resources, the IaaS approach to IoT nodes "
            "offers higher degrees of freedom when engineering any vertical application.",
            "Leveraging an industrial-strength open-source IaaS brings built-in role-based authentication, "
            "delegation, and service-oriented governance that ad-hoc IoT platforms lack.",
            "A novel subsystem called IoTronic is introduced specifically for provisioning configuration "
            "and tasks for board-hosted sensing and actuation resources.",
            "In the conceptual architecture, a diamond-shaped board replaces the traditional VM box, "
            "with interactions described along the control and data paths.",
            "Integrating IoT management into OpenStack had not been independently explored by the community "
            "before Stack4Things — making this a genuinely novel research contribution.",
        ], "Ch.4 § I/Ocloud design considerations · fig:chap04:Stack4Things-pillars"),

        ("theory", "OpenStack extension — IoTronic subsystem (Ch.4 §4.2)", [
            "IoTronic is modelled after standard OpenStack services (Nova, Neutron, Keystone) and exposes "
            "a REST interface for managing remote IoT nodes.",
            "The IoTronic Conductor is the core component: it manages the database, dispatches RPCs among "
            "internal microservices, and orchestrates board lifecycle events.",
            "The IoTronic API server exposes REST endpoints for boards, plugins, services, and telemetry — "
            "accessible via CLI client or Web browser.",
            "OpenStack Horizon has been enhanced with an S4T dashboard panel for visual board management, "
            "plugin injection, and service orchestration.",
            "The IoTronic WAMP agent acts as a bridge between AMQP-internal messaging and WAMP messages "
            "sent to edge boards via Crossbar.",
            "The IoTronic WS tunnel agent (WSTUN) wraps the WebSocket server that boards connect to for "
            "reverse-tunnel access to board-hosted services.",
        ], "Ch.4 § Cloud side: IoTronic · fig:chap04:S4T-cloud-arch"),

        ("image", "Stack4Things pillars (Ch.4)",
         "diagrams/s4t-stack.png",
         "OpenStack core + IoTronic + Lightning-Rod — reference architecture from Ch.4"),

        ("theory", "WAMP — routed RPC for NAT traversal (Ch.4 §4.2.1)", [
            "Traditional RPC client-server models fail when IoT devices sit behind NATs, firewalls, or "
            "cellular networks with frequently changing IP addresses.",
            "Routed RPCs (rRPCs) solve this by introducing a broker that routes calls dynamically, "
            "keeping communication possible even when direct IP reachability is impossible.",
            "The Web Application Messaging Protocol (WAMP) is a real-time, routed messaging protocol "
            "designed specifically for these networking challenges.",
            "With WAMP, devices do not need to know each other's IP addresses — messages are routed "
            "through a Dealer (router) that bypasses NAT and firewall restrictions.",
            "Connections remain persistent over WebSockets, reducing the overhead of frequent "
            "reconnections that plague polling-based approaches.",
            "WAMP supports both Remote Procedure Calls and Publish/Subscribe patterns — RPC is not "
            "available in plain AMQP, which is why S4T chose WAMP for board interactions.",
        ], "Ch.4 § Remote configuration · WAMP routed RPC"),

        ("theory", "WAMP call procedure — Caller, Dealer, Callee (Ch.4)", [
            "A Callee registers a procedure at the Dealer under an abstract URI identifying the procedure "
            "(step 1 in the book's WAMP sequence diagram).",
            "The Dealer maintains a registry mapping procedure URIs to the Callees that implement them.",
            "To invoke a remote procedure, the Caller sends the procedure URI to the Dealer (step 2).",
            "The Dealer looks up the URI in its registry and forwards the call to the correct Callee.",
            "When execution completes, the Dealer retrieves the result and returns it to the Caller "
            "(step 3).",
            "Neither Caller nor Callee needs direct network knowledge of the other — all routing is "
            "handled at the WAMP level by Crossbar in the S4T deployment.",
            "In our lab, Lightning-Rod is the Callee and IoTronic components act as Callers via the "
            "WAMP agent bridge.",
        ], "Ch.4 · fig:chap04:WAMP-steps"),

        ("theory", "WebSocket reverse tunneling — WSTUN (Ch.4 §4.2.2)", [
            "Boards in restrictive IPv4 deployments can almost always initiate outgoing HTTP/HTTPS traffic, "
            "even when inbound connections are blocked by NAT or firewall rules.",
            "Stack4Things implements a novel reverse tunneling technique: the board initiates a WebSocket "
            "connection to the cloud, and the cloud exposes a TCP port for external clients.",
            "When an external client connects to the cloud-side TCP port, the tunnel server signals the "
            "board through the control WebSocket to open a data tunnel.",
            "TCP segments are piped through the WebSocket tunnel, allowing cloud-triggered reachability "
            "to any board-hosted service (SSH, HTTP, custom daemons).",
            "This design enables server-initiated connectivity without port forwarding or VPNs — "
            "critical for large-scale IoT fleet management.",
            "WSTUN (iotronic-wstun container) implements this mechanism on port 8080 in the lab stack.",
            "Module F (Ch.14 web services) will demonstrate exposing an edge HTTP service through this tunnel.",
        ], "Ch.4 § Service forwarding mechanism · fig:chap04:service-forwarding"),

        ("theory", "Lightning-Rod — the edge agent (Ch.4 §4.3)", [
            "Lightning-Rod (LR) runs on the board's MPU and is the single point of contact between the "
            "physical device and the cloud infrastructure.",
            "The LR engine connects to Crossbar via a WebSocket full-duplex WAMP channel, sending and "
            "receiving commands from IoTronic in the cloud.",
            "LR can interact with digital/analog I/O pins through MCUIO sysfs libraries, with OS tools "
            "(filesystem, package manager, services), and with user-injected plugins.",
            "The plugin loader allows custom Python Workers to be injected from the cloud and executed "
            "on the board — the foundation for Modules B and C.",
            "LR also acts as a WebSocket reverse tunnel client, enabling external users to reach "
            "board-internal services through the cloud-side WSTUN agent.",
            "In the emulated lab environment, Lightning-Rod runs inside a Docker container that simulates "
            "a virtual board — no physical hardware is required.",
        ], "Ch.4 § Device side: Lightning-Rod · fig:chap04:LR"),

        ("section", "Stack4Things architecture", "Cloud ↔ edge messaging planes"),

        ("theory", "What is Stack4Things? — platform overview", [
            "Stack4Things (S4T) is open-source middleware for IoT fleet management built on top of "
            "OpenStack, extending cloud orchestration to the network edge.",
            "IoTronic is the cloud-side controller providing REST API, Horizon UI, and MariaDB-backed "
            "persistence for boards, plugins, and services.",
            "Lightning-Rod is the device-side agent providing plugin runtime, WAMP client, and local "
            "I/O abstraction on each board.",
            "S4T is designed with modular architecture: individual components can be developed, deployed, "
            "and updated independently.",
            "All services are containerised and orchestrated via Docker Compose for reproducible "
            "single-host testbed deployments.",
            "The book positions S4T as the instantiation of the I/Ocloud vision within the OpenStack "
            "ecosystem.",
        ], "Ch.4 § Stack4Things architecture · Ch.13 abstract"),

        ("theory", "Logical architecture — three communication planes", [
            "The control plane comprises IoTronic Conductor, Keystone identity service, and the "
            "plugin/service registry exposed through Horizon and REST.",
            "The messaging plane uses RabbitMQ (AMQP) for internal microservice coordination and "
            "Crossbar (WAMP) for bidirectional cloud-to-board RPC and pub/sub.",
            "The data/tunnel plane is implemented by WSTUN (iotronic-wstun), providing reverse "
            "WebSocket tunnels for NAT traversal to board-hosted services.",
            "The edge plane is Lightning-Rod on each board, connecting local I/O, plugins, and OS "
            "resources to the three cloud planes above.",
            "IoTronic WAMP agent translates AMQP messages from internal services into WAMP messages "
            "routed through Crossbar to the correct board.",
            "This separation of planes allows each layer to scale independently — multiple WAMP agents "
            "and WSTUN instances can be instantiated for redundancy.",
        ], "Ch.13 · Ch.4 § Architecture overview · Ch.16 MACM components"),

        ("section", "IoTronic REST API", "Ch.4 — nodes, pins, services, plugins"),

        ("theory", "Stack4Things REST API — resource groups (Ch.4)", [
            "Table table:api documents IoTronic v0.1 endpoints grouped by resource type.",
            "Nodes: GET /v1/nodes lists registered boards; GET /v1/nodes/{uuid} returns board metadata.",
            "Pins: read/set GPIO modes and values — REST hides WAMP complexity for I/O abstraction.",
            "Services: activate or delete forwarded services (SSH, HTTP) on a board via JSON body.",
            "Plugins: GET/POST/DELETE /v1/nodes/{uuid}/plugins — same inject/remove semantics as Horizon.",
            "Lab health check curl http://{{VM_IP}}:8812/ maps to modern Conductor root; book uses v0.1 paths.",
        ], "Ch.4 § Stack4Things REST API · table:api"),

        ("theory", "Use case — list registered nodes (Ch.4)", [
            "Prerequisite: one or more boards already registered in IoTronic MariaDB.",
            "Horizon or CLI issues GET /v1/nodes → message on RabbitMQ AMQP queue.",
            "Conductor queries MariaDB and returns NodeCollection JSON with UUID and description links.",
            "No board interaction required — listing is purely cloud-side metadata.",
            "Optional: Conductor queries WAMP presence on demand for live connectivity status.",
            "Alternative: WAMP agents periodically write connectivity into DB — trades freshness for API speed.",
        ], "Ch.4 § List of nodes · fig:chap04:list-node"),

        ("theory", "Use case — SSH service forwarding via WSTUN (Ch.4)", [
            "User requests SSH to board port 22 through Horizon — REST call #10 in table:api.",
            "Boards behind NAT cannot accept inbound SSH; a board-initiated reverse tunnel is required.",
            "Conductor picks a free TCP port on WSTUN agent and signals LR via WAMP.",
            "Lightning-Rod opens WebSocket tunnel to WSTUN and pipes traffic to local sshd.",
            "User receives cloud IP + port — same reverse-channel pattern reused for HTTP in Module F.",
            "Module F WSTUN demos are the HTTP analogue of this classic SSH forwarding workflow.",
        ], "Ch.4 § Service forwarding · fig:chap04:enable-ssh · WSTUN"),

        ("theory", "I/Ocloud virtual filesystem — FUSE drivers (Ch.4)", [
            "Beyond REST, S4T exposes remote board I/O as a virtual POSIX filesystem via FUSE.",
            "Plugin Node.js drivers map sensors/actuators to filesystem paths — cloud VMs mount remote pins.",
            "MCUIO hypervisor virtualizes Arduino YUN GPIO across containers with access control.",
            "Design trade-off: interactive apps keep VNs near sensors; compute-heavy tasks migrate to cloud.",
            "Training lab focuses on Docker Compose + REST; FUSE path is production/research extension.",
            "Connects I/Ocloud theory (Ch.4) to environmental plugins (Ch.15) as callable functions.",
        ], "Ch.4 § I/Ocloud implementation · fig:chap04:S4T-IOcloud · YUN virtualization"),

        ("section", "Docker & Docker Compose", "Why containers for S4T deployment"),

        ("theory", "Docker — portability and isolation (Ch.13 §13.2)", [
            "Docker is an open-source platform for building, shipping, and running applications inside "
            "lightweight, portable containers.",
            "Unlike virtual machines that emulate an entire operating system, containers encapsulate only "
            "the application and its dependencies, sharing the host kernel.",
            "Portability enables the write-once-run-anywhere paradigm: a Stack4Things component deployed "
            "on Ubuntu 22.04 behaves identically on any host with Docker installed.",
            "Isolation prevents dependency conflicts by encapsulating each service in its own container "
            "with independent filesystem, network namespace, and process tree.",
            "Docker builds on Linux cgroups and namespaces, offering a higher-level abstraction accessible "
            "through CLI and REST APIs.",
            "This reproducibility makes containers especially suitable for research prototyping, training "
            "labs, and production deployments alike.",
        ], "Ch.13 § Docker"),

        ("theory", "Docker — efficiency and scalability (Ch.13 §13.2)", [
            "Containers consume significantly fewer system resources than virtual machines because they "
            "share the host operating system kernel rather than duplicating it.",
            "A full S4T stack with ten or more services runs comfortably on a VM with 4 GB RAM — "
            "impossible with equivalent VM-per-service virtualization.",
            "Docker integrates seamlessly with orchestration tools such as Docker Compose and Kubernetes "
            "to facilitate automated deployment and dynamic scaling.",
            "For the training lab, a single docker compose up -d command replaces hours of manual "
            "per-service installation and configuration.",
            "The book's alternative path uses Oracle VirtualBox with Ubuntu 22.04 — functionally equivalent "
            "but slower to provision for a 60-minute session.",
            "Scaling beyond single-host Compose deployments toward Kubernetes is covered in Chapter 11 "
            "for production-grade multi-node environments.",
        ], "Ch.13 § Docker · scalability bullet"),

        ("theory", "Docker Compose — multi-container orchestration (Ch.13 §13.2)", [
            "Docker Compose extends Docker by enabling definition and management of multi-container "
            "applications through a declarative YAML configuration file.",
            "Real-world systems consist of interconnected services (databases, message brokers, API servers) "
            "that must be orchestrated together with explicit dependency ordering.",
            "Compose describes services, their dependencies (depends_on), networks, and storage volumes "
            "in a single docker-compose.yml file.",
            "A single command — docker compose up -d — brings up the entire S4T application stack, "
            "eliminating manual container creation and wiring.",
            "Compose manages service dependencies and coordinates the lifecycle of multiple containers "
            "as a cohesive application.",
            "Internally Compose relies on the Docker Engine but provides declarative reproducibility "
            "ideal for prototyping, experimentation, and CI/CD pipelines.",
            "For Stack4Things, Compose defines and launches IoTronic, Crossbar, MariaDB, RabbitMQ, "
            "Keystone, WSTUN, and Lightning-Rod in one unified environment.",
        ], "Ch.13 § Docker Compose"),

        ("section", "S4T services & ports", "Ch.13 Table — comprehensive service map"),

        ("theory", "S4T services — API, messaging, persistence (Ch.13 Table)", [
            "IoTronic Conductor API: central RESTful interface for boards, plugins, services, and "
            "telemetry — exposed on port 8812 in the repository (book lists 8888).",
            "Crossbar.io WAMP router: bidirectional RPC and pub/sub via WAMP protocol on port 8181 — "
            "Lightning-Rod connects to wss://crossbar:8181 inside the Docker network.",
            "MariaDB database: persistent store for board metadata, user data, plugins, and services "
            "on port 3306 — controlled via MYSQL_ROOT_PASSWORD environment variable.",
            "RabbitMQ message bus: AMQP-based internal coordination between Conductor, WAMP agent, and "
            "other IoTronic microservices on port 5672.",
            "MQTT Broker (Mosquitto): lightweight pub/sub for IoTronic-to-Lightning-Rod communication "
            "on port 1883 in some S4T configurations.",
            "CA Service: Certificate Authority generating TLS material for secure board authentication "
            "and encrypted internal communications.",
            "All inter-service traffic on the internal s4t Docker network uses container hostnames for DNS resolution.",
        ], "Ch.13 · tab:S4T-services"),

        ("theory", "S4T services — identity, UI, edge agent (Ch.13 Table)", [
            "Keystone identity service: OpenStack authentication and authorization on port 5000 — "
            "required for Horizon login and API token issuance.",
            "IoTronic Web UI (Horizon): OpenStack dashboard enhanced with S4T IoT panel on port 80 — "
            "credentials {{HZ_CRED}}.",
            "Lightning-Rod agent: edge software executing remote tasks, running plugins, and maintaining "
            "WAMP session — local UI on port 1474.",
            "IoT WSTUN (iotronic-wstun): reverse WebSocket tunnel server on port 8080 for exposing "
            "board-hosted services to external clients.",
            "WebSocket (WS) agent: alternative reverse tunneling on port 8083 in some configurations.",
            "InfluxDB (lab overlay only): time-series database on port 8086 for Module C environmental "
            "data — not in the upstream ch13 compose file.",
            "RabbitMQ management UI is optionally available on port 15672 for queue inspection during troubleshooting.",
        ], "Ch.13 · tab:S4T-services · training lab overlay"),

        ("theory", "Internal messaging — AMQP bridge to WAMP (Ch.4 + Ch.13)", [
            "All communication among IoTronic internal components travels over the network via AMQP "
            "queues on RabbitMQ, following standard OpenStack microservice philosophy.",
            "This AMQP bus allows components to be deployed on different machines without affecting "
            "service functionality — enabling horizontal scalability.",
            "The IoTronic WAMP agent (iotronic-wagent container) translates AMQP messages into WAMP "
            "messages and vice versa for board-facing communication.",
            "Multiple WAMP agents and WSTUN instances can be instantiated, each handling a subset "
            "of IoT devices for redundancy and high availability.",
            "WAMP was chosen over extending AMQP to boards because it is a WebSocket subprotocol supporting "
            "both RPC and Publish/Subscribe — RPC is not natively available in AMQP.",
            "Crossbar serves as the WAMP Dealer: Lightning-Rod registers procedures, IoTronic invokes them.",
            "The WAMP realm used in the lab is s4t — all LR agents authenticate against this realm.",
        ], "Ch.4 § IoTronic WAMP agent · Ch.13 service table"),

        ("section", "Compose configuration", "Services, networks, lab overlay"),

        ("theory", "docker-compose.yml — service roles and dependencies", [
            "ca_service generates the Root CA and Crossbar TLS certificates into the shared iotronic_ssl volume.",
            "crossbar starts the WAMP router on port 8181, depending on CA certificates being present.",
            "iotronic-db (MariaDB) and rabbitmq must pass healthchecks before downstream services start.",
            "keystone provides OpenStack identity — Horizon and Conductor authenticate against it on port 5000.",
            "iotronic-conductor is the core REST API and orchestration logic, healthy on port 8812.",
            "iotronic-wagent bridges AMQP internal bus to WAMP messages for board communication.",
            "iotronic-wstun provides reverse WebSocket tunnels on port 8080 for board service exposure.",
            "iotronic-ui (Horizon) and lightning-rod provide operator dashboards on ports 80 and 1474.",
        ], "Ch.13 deploy walkthrough · docker-compose.yml"),

        ("theory", "Docker network s4t — internal DNS resolution", [
            "All S4T containers are placed on a user-defined bridge network named s4t.",
            "Docker's embedded DNS resolves container service names as hostnames within the network.",
            "Lightning-Rod reaches Crossbar at wss://crossbar:8181 — not localhost, not the host IP.",
            "IoTronic Conductor connects to iotronic-db, rabbitmq, and keystone using their service names.",
            "This eliminates manual IP configuration and makes the compose file portable across hosts.",
            "Port mappings (e.g. 80:80, 8812:8812) expose selected services to the host for browser and curl access.",
            "Limitation: this single-host s4t network is designed for local development and training — "
            "multi-host production requires additional networking (Ch.11 Kubernetes).",
        ], "Ch.13 networking section · Ch.13 § Configuration summary"),

        ("theory", "Lab overlay — training patches (not in book repo)", [
            "training/patches/docker-compose.lab.yml extends the upstream ch13 docker-compose.yml.",
            "Fixes ca_service: replaces EOL debian:buster with alpine:3.19 + openssl for certificate generation.",
            "Fixes Lightning-Rod image: mdslab/lrod:compose replaces a broken @sha256 placeholder in upstream.",
            "Mounts /var/run/docker.sock into LR — enables the Ch.14 Docker lifecycle plugin demo in Module B.",
            "Adds influxdb:1.8 on network s4t with hostname influxdb — required for Module C CSV ingestion.",
            "Adds lightning-rod-2 and lightning-rod-3 on ports 1475 and 1476 for multi-board modules later.",
            "Always launch with both compose files: -f docker-compose.yml -f ../../patches/docker-compose.lab.yml.",
        ], "Training material — patches/docker-compose.lab.yml"),

        ("warn", "Book ↔ repository corrections", [
            "API port: book documents :8888 → repository exposes Conductor on :8812 — "
            "use curl http://{{VM_IP}}:8812/.",
            "Horizon dashboard: http://{{VM_IP}}/horizon — credentials {{HZ_CRED}}.",
            "Lightning-Rod UI: http://{{VM_IP}}:1474 — credentials {{LR_CRED}}.",
            "Boards panel URL: /horizon/iot/ (NOT /horizon/iot/boards/ — that path returns 404).",
            "WAMP inside Docker: wss://crossbar:8181 — never use localhost or {{VM_IP}} from inside LR container.",
        ]),

        ("section", "Lab: deploy stack", "Docker Compose + lab overlay"),

        ("demo", "Module A — expected outcomes", [
            "You will prove that the full S4T cloud-side stack runs reproducibly on a single training VM.",
            "You will confirm the IoTronic Conductor REST API responds with HTTP 200 on port 8812.",
            "You will log into Horizon and navigate to the IoT Boards panel without authentication errors.",
            "You will register a virtual board and configure Lightning-Rod to establish a WAMP session.",
            "You will observe the board transition to Active state — the mandatory gate for Modules B–I.",
            "This deployment connects Ch.4 theory (I/Ocloud, WAMP, WSTUN) to Ch.13 practice (Compose, onboarding).",
            "Every subsequent module assumes today's stack is running and at least one board is Active.",
        ]),

        ("content", "Environment check", [
            "$ docker --version && docker compose version",
            "$ groups | grep docker    # user must be in docker group",
            "$ free -h                 # ≥ 4 GB free RAM recommended",
            "$ git clone https://github.com/AssemblingSmartCPS/ch13.git training/repos/ch13",
        ]),

        ("hands_on", "Start the stack", [
            "$ cd training/repos/ch13",
            "$ docker compose -f docker-compose.yml \\",
            "    -f ../../patches/docker-compose.lab.yml up -d",
            "First boot: 15–25 min (image pull + MariaDB init + CA certificate generation).",
            "Monitor with: docker compose ps and docker compose logs -f crossbar",
        ]),

        ("demo", "First-boot timing — why Compose starts early", [
            "First boot is I/O-bound: Docker pulls ~2 GB of images and MariaDB runs schema migrations.",
            "CA certificate generation must complete before Crossbar can start its WAMP router.",
            "Keystone database initialisation and RabbitMQ healthcheck add several minutes of startup time.",
            "Use the waiting period to study boot order, CA/TLS, and service roles in the theory slides.",
            "Monitor with docker compose ps — look for (healthy) status on db, rabbitmq, and conductor.",
            "If any container restart-loops, the troubleshooting section at the end provides diagnostic steps.",
        ]),

        ("image", "Horizon IoT — Boards panel",
         "chapter13/horizon-boards-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/ — target UI for board registration"),

        ("theory", "Boot order — infrastructure layer (Ch.13)", [
            "Step 1: ca_service writes Root CA and Crossbar TLS certificates to the iotronic_ssl shared volume.",
            "Step 2: iotronic-db (MariaDB) starts and must pass its healthcheck before any service needing persistence.",
            "Step 3: rabbitmq starts and must pass its healthcheck — the AMQP bus must be ready for microservices.",
            "Step 4: keystone starts, initialising the OpenStack identity database for Horizon authentication.",
            "If MariaDB or RabbitMQ fail healthchecks, all downstream services will remain in a waiting state.",
            "Inspect with: docker compose logs iotronic-db and docker compose logs rabbitmq.",
            "Typical first-boot delay: 5–10 minutes for database schema creation alone.",
        ], "Ch.13 · operational sequencing"),

        ("theory", "Boot order — application layer (Ch.13)", [
            "Step 5: crossbar starts the WAMP router on port 8181, mounting certificates from iotronic_ssl.",
            "Step 6: iotronic-wagent starts, connecting to both RabbitMQ (AMQP) and Crossbar (WAMP).",
            "Step 7: iotronic-wstun starts the reverse tunnel server on port 8080 with TLS from iotronic_ssl.",
            "Step 8: iotronic-conductor starts the REST API, becoming healthy on port 8812.",
            "Step 9: iotronic-ui (Horizon) becomes reachable on port 80 after Keystone is ready.",
            "Step 10: lightning-rod container starts with its local configuration UI on port 1474.",
            "Healthy stack indicator: docker compose ps shows (healthy) for db, rabbitmq, and conductor.",
        ], "Ch.13 · operational sequencing · fig:chap13:Docker-compose-ok"),

        ("content", "While waiting — monitor in terminal 2", [
            "$ docker compose -f docker-compose.yml \\",
            "    -f ../../patches/docker-compose.lab.yml ps",
            "$ docker compose logs -f crossbar",
            "$ docker compose logs -f iotronic-conductor",
            "Healthy = (healthy) in ps output for iotronic-db, rabbitmq, iotronic-conductor.",
        ]),

        ("theory", "CA service & TLS certificate chain (Ch.13 + Ch.16)", [
            "The Certificate Authority container (ca_service) generates a Root CA key and certificate "
            "plus a Crossbar-specific key and signed certificate.",
            "All TLS material is written to the iotronic_ssl Docker volume, shared by crossbar, "
            "iotronic-wstun, and other components requiring encrypted communications.",
            "Crossbar mounts iotronic_ssl at /node/.crossbar/ssl and starts WAMP over wss:// on port 8181.",
            "If Crossbar enters a restart loop, inspect ca_service logs: docker compose logs ca_service.",
            "The lab overlay uses alpine:3.19 instead of debian:buster because Buster apt repositories are EOL.",
            "WAMP endpoint inside Docker: wss://crossbar:8181 in realm s4t — TLS is terminated at Crossbar.",
            "Never delete iotronic_ssl volume while the stack is running — Crossbar will lose its certificates.",
        ], "Ch.16 — CA secures internal tunnel communications · Ch.13 volumes"),

        ("theory", "Crossbar — WAMP router configuration (Ch.13)", [
            "Crossbar.io is the WAMP Dealer that routes RPC calls and pub/sub messages between IoTronic and boards.",
            "Lightning-Rod connects as a Callee, registering board procedures under URIs in the s4t realm.",
            "IoTronic WAMP agent connects as a Caller, invoking board procedures on behalf of REST API requests.",
            "Crossbar requires valid TLS certificates from ca_service before it can accept wss:// connections.",
            "Port 8181 is mapped to the host for debugging but LR must use the internal hostname crossbar.",
            "If WAMP session fails, check: (1) Crossbar healthy, (2) certificates present, (3) LR uses wss:// not ws://.",
            "Crossbar logs show registration events when LR successfully connects and registers procedures.",
        ], "Ch.13 · Crossbar service · Ch.4 WAMP Dealer role"),

        ("theory", "MariaDB — IoTronic persistence layer (Ch.13)", [
            "MariaDB (iotronic-db container) stores all persistent IoTronic state on port 3306.",
            "Board registrations, UUIDs, user associations, and tenant mappings are stored in the IoTronic schema.",
            "Plugin definitions, injection records, and service catalog entries persist across container restarts.",
            "Data is stored in the unime_iotronic_db_data Docker volume — survives docker compose down without -v.",
            "Connection string is configured via DB_CONNECTION in .env: mysql+pymysql://user:pass@iotronic-db/iotronic.",
            "If Conductor fails with database connection errors, verify iotronic-db shows (healthy) in compose ps.",
            "Wiping unime_iotronic_db_data forces full re-initialisation — all board registrations are lost.",
        ], "Ch.13 service table · Ch.13 § Volumes"),

        ("theory", "RabbitMQ — internal AMQP message bus (Ch.13)", [
            "RabbitMQ provides the AMQP message bus for asynchronous coordination among IoTronic microservices.",
            "The Conductor publishes commands and events that WAMP agent, WSTUN, and other workers consume.",
            "Default AMQP port is 5672; management UI is available on 15672 for queue depth inspection.",
            "RabbitMQ must pass its healthcheck before iotronic-conductor and iotronic-wagent can start.",
            "Message orientation, queueing, routing (point-to-point and pub/sub), and reliability are "
            "provided by the AMQP open standard.",
            "If services hang at startup, check RabbitMQ logs: docker compose logs rabbitmq.",
            "RabbitMQ data persists in its own Docker volume — queue state survives container restarts.",
        ], "Ch.13 service table · Ch.4 § AMQP internal bus"),

        ("theory", "Keystone — OpenStack identity service (Ch.13)", [
            "Keystone provides authentication and authorization for Horizon and IoTronic API access.",
            "Horizon login uses Keystone credentials: {{HZ_CRED}} in the lab environment.",
            "API requests to Conductor include Keystone-issued tokens when auth_strategy=keystone in iotronic.conf.",
            "Keystone runs on port 5000 inside the s4t network; iotronic-conductor references http://keystone:5000.",
            "The OpenStack role-based access model from Ch.4 applies: users, projects, and domains are "
            "managed through Keystone's identity backend.",
            "If Horizon shows authentication errors, verify keystone container is running and its database "
            "initialised: docker compose logs keystone.",
            "Keystone is a standard OpenStack service — the same identity layer used by Nova, Neutron, and Glance.",
        ], "Ch.13 service table · Ch.4 § OpenStack identity"),

        ("content", "Verify API and dashboards", [
            "$ curl -s -o /dev/null -w '%{http_code}\\n' http://{{VM_IP}}:8812/",
            "Browser: http://{{VM_IP}}/horizon  ({{HZ_CRED}})",
            "Browser: http://{{VM_IP}}:1474  ({{LR_CRED}})",
            "Expected: HTTP 200 or 302 — not 000 (connection refused) or 502 (upstream not ready).",
        ]),

        ("image", "Horizon — login screen", "chapter13/horizon-login.png",
         "http://{{VM_IP}}/horizon", "", True),

        ("image", "Horizon — after login", "chapter13/horizon-after-login.png",
         "OpenStack admin dashboard — navigate to IoT section in left sidebar"),

        ("section", "Board onboarding", "Cloud registration + edge agent configuration"),

        ("theory", "Virtual board concept — emulated IoT device (Ch.13)", [
            "In the emulated lab environment, the IoT device is a Lightning-Rod Docker container, not physical hardware.",
            "Horizon Create Board allocates a unique UUID and registration code stored in the IoTronic MariaDB.",
            "The registration code acts as a one-time credential allowing the LR agent to bind to the cloud record.",
            "Board states progress: registered → first_boot → online/Active when WAMP session is established.",
            "An Active board can receive plugin injections, service deployments, and WSTUN tunnel requests.",
            "Multiple virtual boards can coexist: lightning-rod (1474), lightning-rod-2 (1475), lightning-rod-3 (1476).",
            "The book describes adding a second board on a separate VM — the lab uses additional LR containers instead.",
        ], "Ch.13 § Setting up Stack4Things · § Adding a new virtual IoT device"),

        ("theory", "Board lifecycle and Horizon management (Ch.13)", [
            "Navigate to Horizon → IoT → Boards to see all registered boards with ID, name, fleet, and status.",
            "Create Board form requires: board name, description, and device type — tags are optional.",
            "After submission, Horizon displays the board UUID and registration code — copy both immediately.",
            "The registration code must be pasted into Lightning-Rod Configuration before the agent can connect.",
            "Board status in Horizon updates in real time as LR establishes or loses its WAMP session.",
            "Fleet assignment groups boards for coordinated plugin injection in Module B (Ch.14 fleet management).",
            "Deleting a board in Horizon does not automatically stop the LR container — reconfigure or restart LR separately.",
        ], "Ch.13 · fig:chap13:New-IoT · fig:chap13:blist"),

        ("demo", "What board onboarding proves — theory connection", [
            "Onboarding demonstrates that IoTronic's cloud registry and the edge LR agent can establish a "
            "secure, persistent WAMP session through Crossbar.",
            "It validates the Ch.4 routed RPC model: LR registers procedures, IoTronic invokes them without "
            "direct IP reachability.",
            "It confirms Keystone authentication works end-to-end: Horizon login, board creation, API access.",
            "It proves the CA/TLS chain is functional: LR connects via wss:// with valid Crossbar certificates.",
            "An Active board is the prerequisite for plugin injection (Module B), environmental data (Module C), "
            "and web service exposure (Module F).",
            "Without Active state, WSTUN tunnels cannot be established and no edge service is reachable.",
            "Take a screenshot of the Active board — it is the mandatory Module A deliverable.",
        ]),

        ("image", "UML sequence — Board onboarding (Module A)",
         "diagrams/seq-board-onboarding.png",
         "Horizon → Conductor → Crossbar → Lightning-Rod → Active state"),

        ("content", "Create Board on Horizon", [
            "Horizon → IoT → Boards → + Create Board",
            "Fill: name (e.g. board-alpha), description, device type",
            "Copy registration code and board UUID shown after create",
            "Book reference: Ch.13 fig. sshot-create-board",
        ]),

        ("image", "Book figure — Create Board (Ch.13)",
         "chapter13/sshot-create-board.png",
         "Reference UI fields from book — name, description, device type"),

        ("theory", "Lightning-Rod configuration fields (Ch.13)", [
            "Open the LR web UI at http://{{VM_IP}}:1474 and log in with {{LR_CRED}}.",
            "The WAMP endpoint field must be set to wss://crossbar:8181 — the internal Docker hostname.",
            "Using localhost or {{VM_IP}} in the WAMP field will fail because LR runs inside the s4t network.",
            "Paste the board registration code from Horizon into the designated configuration field.",
            "Click CONFIGURE to persist settings — LR will attempt to connect to Crossbar immediately.",
            "Navigate to the Status page: IoTronic connection must show Connected with Name and UUID populated.",
            "LR credentials ({{LR_CRED}}) are separate from Horizon credentials ({{HZ_CRED}}).",
        ], "Ch.13 step-by-step onboarding · fig:chap13:lrconf"),

        ("theory", "WAMP session establishment — what happens at CONFIGURE", [
            "Lightning-Rod initiates a WebSocket connection to wss://crossbar:8181 with TLS verification.",
            "LR authenticates to the s4t WAMP realm using the board registration code as credential.",
            "Crossbar accepts the session and LR registers its board procedures under WAMP URIs.",
            "IoTronic WAMP agent is notified via AMQP that a new board session is active.",
            "The Conductor updates the board record in MariaDB from registered to online/Active status.",
            "Horizon Boards panel reflects the status change within seconds of successful WAMP registration.",
            "If connection fails, LR Status shows error details — cross-check WAMP URL and registration code.",
        ], "Ch.4 § WAMP registration · Ch.13 § Lightning-Rod configuration"),

        ("image", "Lightning-Rod — login", "chapter13/lr-ui-login.png",
         "http://{{VM_IP}}:1474 — {{LR_CRED}}", "", True),

        ("image", "Lightning-Rod — Configuration (live)", "chapter13/lr-dashboard-conf.png",
         "Registration code + WAMP endpoint wss://crossbar:8181 — configure before Status check", "", True),

        ("content", "Configure Lightning-Rod", [
            "Open http://{{VM_IP}}:1474 — login {{LR_CRED}}",
            "WAMP field: wss://crossbar:8181",
            "Paste board registration code from Horizon → click CONFIGURE",
            "Verify Status page: Connected + board Name and UUID populated",
        ]),

        ("image", "Book figure — LR configuration (Ch.13)",
         "chapter13/sshot-lr-conf.png",
         "Book reference for WAMP endpoint and board registration code fields"),

        ("image", "Lightning-Rod — Status dashboard", "chapter13/lr-dashboard-status.png",
         "Connected board — mandatory gate before Module B", "", True),

        ("content", "Confirm Active board", [
            "Horizon → IoT → Boards → your board row shows Active/online status",
            "LR Status: IoTronic connection Connected, Name and UUID populated",
            "Take screenshot — mandatory deliverable before Module B",
            "Run: cd training && ./validate-lab.sh",
        ]),

        ("image", "Book figure — board info Active (Ch.13)",
         "chapter13/sshot-board-info.png",
         "Target end state for Module A — board details with Active status"),

        ("theory", "Persistent volumes — data survival across restarts (Ch.13)", [
            "unime_iotronic_db_data stores MariaDB content: board registrations, users, plugins, services.",
            "iotronic_ssl holds CA-generated TLS certificates used by Crossbar, WSTUN, and other secure services.",
            "iotronic_logs and iotronic-ui_logs capture audit trails from Conductor and Horizon for troubleshooting.",
            "lr_data, lr_var, lr_confs volumes persist Lightning-Rod configuration and plugin state across restarts.",
            "docker compose down stops containers but preserves volumes — board data survives a simple restart.",
            "docker compose down -v wipes ALL volumes — full re-onboarding required, including new board registration.",
            "Volumes are defined in docker-compose.yml and automatically managed by Docker.",
        ], "Ch.13 § Volumes"),

        ("theory", "Networking, ports, and environment variables (Ch.13)", [
            "All containers share the s4t user-defined bridge network with embedded DNS hostname resolution.",
            "Host port mappings expose services to the training VM: 80 (Horizon), 8812 (API), 1474 (LR), 8181 (Crossbar).",
            "Environment variables control service behaviour: DB passwords, Keystone URLs, auth strategy.",
            "Variables can be set inline in docker-compose.yml, in .env file, or as Docker secrets for production.",
            "This single-host configuration is designed for development, testing, and demonstration only.",
            "Distributed multi-host deployment requires additional networking and security configuration (Ch.11).",
            "The book's configuration summary table lists all default ports and roles for reference.",
        ], "Ch.13 § Networking · § Configuration summary"),

        ("section", "Troubleshooting", "Common first-boot and onboarding issues"),

        ("content", "Troubleshooting — infrastructure services", [
            "Crossbar restart loop → inspect ca_service: docker compose logs ca_service; wait for iotronic_ssl certs.",
            "MariaDB not ready → wait for iotronic-db (healthy); Conductor will not start without it.",
            "RabbitMQ connection refused → check rabbitmq healthcheck; restart with docker compose restart rabbitmq.",
            "Keystone auth failure → verify keystone container running; check iotronic.conf auth_strategy=keystone.",
            "Conductor unhealthy → docker compose logs iotronic-conductor; often a downstream dependency not ready.",
        ]),

        ("content", "Troubleshooting — edge agent and ports", [
            "Port 80 or 8812 busy → ss -tlnp | grep ':80\\|:8812' — stop conflicting host services.",
            "LR image pull error → confirm lab overlay uses mdslab/lrod:compose, not broken upstream SHA.",
            "LR WAMP connection failed → verify wss://crossbar:8181 (not localhost); check Crossbar is healthy.",
            "Board stays registered but not Active → re-paste registration code; restart LR: docker compose restart lightning-rod.",
            "Horizon 404 on /horizon/iot/boards/ → use correct path /horizon/iot/ instead.",
        ]),

        ("demo", "Module A deliverable — what you submit", [
            "Screenshot of Horizon Boards panel showing your board in Active/online state.",
            "Terminal output of curl returning HTTP 200 from http://{{VM_IP}}:8812/.",
            "Confirmation that LR Status page shows Connected with correct board UUID.",
            "Successful run of training/validate-lab.sh with no FAIL lines.",
            "This deliverable unlocks Module B: synchronous HelloName plugin injection (Ch.14).",
            "Keep the stack running between modules — docker compose down stops all services.",
            "If you must restart, volumes preserve board data; LR reconnects automatically if already configured.",
        ]),

        ("content", "Module A checklist & handoff to Module B", [
            "□ curl http://{{VM_IP}}:8812/ returns 200",
            "□ Horizon login OK at http://{{VM_IP}}/horizon ({{HZ_CRED}})",
            "□ LR login OK at http://{{VM_IP}}:1474 ({{LR_CRED}})",
            "□ Board Active in Horizon — screenshot saved",
            "Next: Module B — Plugins & Services (Ch.14) · ./training/validate-lab.sh",
        ]),
    ]
