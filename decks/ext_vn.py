"""Module E — Virtual Networking (Ch.5)."""


def slides() -> list:
    return [
        ("title", "Module E — Virtual Networking",
         "Ch.5 · Extension · VM {{VM_IP}} · OPTIONAL tier",
         "Extension · Ch.5 — Virtual Networking · optional if Neutron incomplete"),

        ("section", "Network virtualization theory", "Ch.5 — Neutron + IoTronic ports before the lab"),

        ("theory", "Problem: connecting cloud and edge (Ch.5)", [
            "IoT boards sit behind NAT, firewalls, and heterogeneous LAN topologies",
            "Cloud applications in VMs need logical connectivity to edge devices and sensors",
            "Network virtualization: overlay networks independent of physical wiring",
            "Stack4Things extends OpenStack Neutron toward edge IoT nodes via IoTronic",
            "Goal: treat remote boards as first-class network citizens in the cloud overlay",
            "Complements WSTUN (Module F) which solves HTTP service exposure, not L2/L3 overlay",
        ], "Ch.5 · Network virtualization in IoT · chapter abstract"),

        ("theory", "OpenStack Neutron recap for IoT context (Ch.5)", [
            "Neutron manages virtual networks, subnets, routers, security groups in OpenStack",
            "Standard cloud VMs attach to Neutron networks via virtual interfaces (VIFs)",
            "IoTronic ports API extends this model: boards receive VIFs on overlay networks",
            "WAgent (Worker Agent) on cloud side coordinates tunnel/port setup with edge LR agent",
            "Production: full Neutron L2/L3 with ML2 plugin; Docker lab: API workflow demo only",
            "Book tables list IoTronic networking REST endpoints with request/response schemas",
        ], "Ch.5 § OpenStack networking · Neutron architecture"),

        ("theory", "Virtual ports & VIF abstraction (Ch.5)", [
            "POST /v1/boards/{uuid}/ports/ attaches virtual network interface to registered board",
            "Response JSON includes VIF_name, ip address, MAC_add — logical identity on overlay",
            "Board-side: virtual interface appears in Linux network stack (tun/tap device)",
            "Applications on board bind to assigned overlay IP without physical NIC changes",
            "Cloud-side: other VMs on same Neutron network reach board via overlay routing",
            "Enables peer-to-peer cloud↔edge communication for latency-sensitive workloads",
        ], "Ch.5 · IoTronic networking API · attach port listing"),

        ("theory", "WAgent orchestration role (Ch.5 + Ch.13)", [
            "WAgent container (iotronic-wagent) runs alongside Conductor in cloud stack",
            "Receives port attach requests from IoTronic → configures tunnel/VIF on cloud side",
            "Coordinates with Lightning-Rod agent on board for edge-side interface creation",
            "Logs in docker logs iotronic-wagent show attach attempt and backend response",
            "If Neutron backend unavailable: API accepts request but L3 may not fully provision",
            "Lab value: understand book workflow before production OpenStack deployment",
        ], "Ch.5 · WAgent · Ch.13 docker-compose service list"),

        ("theory", "I/Ocloud networking context (Ch.4–5 bridge)", [
            "Virtual Nodes in cloud can participate in same overlay as physical boards",
            "Designate provides DNS naming; Neutron provides topology; IoTronic binds boards",
            "Full production: multi-site SLICES experiments span Neutron networks (Ch.10–11)",
            "VN enables cloud microservices to push/pull data directly to edge sensors",
            "Different from Module F WSTUN: VN is network-layer; WSTUN is application-layer tunnel",
            "Both coexist in complete S4T deployments for different connectivity patterns",
        ], "Ch.4 I/Ocloud + Ch.5 VN · fig:chap05:vn-workflow"),

        ("theory", "Attach-port REST workflow step-by-step (Ch.5)", [
            "Step 1: obtain Keystone token (or use Horizon session for API exploration)",
            "Step 2: GET /v1/boards/ — select Active board UUID",
            "Step 3: GET /v1/networks/ or Horizon — obtain target Neutron network UUID",
            "Step 4: POST /v1/boards/{BOARD_UUID}/ports/ with {\"network\": \"NETWORK_UUID\"}",
            "Step 5: parse response — note VIF_name, ip, MAC for verification on board",
            "Step 6: test connectivity from cloud VM to board overlay IP (production)",
        ], "Ch.5 · API tables · training/experiments/virtual-networking/"),

        ("theory", "MENO and Virtual Sensor Networks (Ch.5)", [
            "Managed Ecosystem of Networked Objects (MENO): limited cooperating devices without public IPs.",
            "VITRO Virtual Sensor Networking (VSN): dynamic collaboration across admin domains.",
            "Applications see only the logical overlay — physical LAN boundaries become transparent.",
            "Motivates S4T NV beyond lab attach-port: smart factories, buildings, and city districts.",
            "Contrasts with exposing every sensor on a public server — most IoT apps need local cooperation.",
            "Book figure: fig:chap05:MENO — end-to-end logical network over heterogeneous physical links.",
        ], "Ch.5 § Network virtualization in IoT · MENO · VITRO"),

        ("theory", "S4T NV use cases from the book (Ch.5)", [
            "Partitioning: split devices on one LAN into separate VNs — e.g. departments in a smart building.",
            "Cross-network: connect geo-distributed boards without VPN configuration on edge routers.",
            "Cloud extension: add OpenStack VMs to the same VN as edge sensors for storage and analytics.",
            "Personal devices: smartphones/tablets join VN — static overlay IP survives WiFi↔4G handoff.",
            "Hybrid VNs combine all patterns — countless topologies for application-specific requirements.",
            "AllJoyn requires same broadcast domain; S4T NV crosses NAT and subnet boundaries.",
        ], "Ch.5 § use cases · fig:chap05:use-cases · fig:chap05:use-case-personal"),

        ("image", "Attach port workflow",
         "diagrams/vn-attach-workflow.png",
         "Horizon/API → IoTronic → WAgent → board virtual interface"),

        ("content", "Module E — learning objectives", [
            "Understand Ch.5 virtual networking theory and IoTronic ports API",
            "Execute attach-port.sh helper script against live lab Conductor",
            "Inspect WAgent logs for orchestration evidence",
            "Articulate VN vs WSTUN difference (network overlay vs HTTP tunnel)",
            "Pass validate-lab-vn.sh where Neutron backend permits",
        ]),

        ("content", "Module E — 45-minute timeline (OPTIONAL)", [
            "0–15 min  — VN theory: Neutron, VIF, WAgent (slides above)",
            "15–20 min — DEMO GOAL review + list boards and existing ports",
            "20–35 min — HANDS-ON: attach port API call + log inspection",
            "35–45 min — Validate + contrast with Module F WSTUN",
            "[EXT] SKIP-IF-SHORT: omit entire module in 3h core-only path",
        ]),

        ("demo", "What this module demonstrates — demo goals", [
            "Operator can request virtual port attachment via REST API on live Conductor",
            "WAgent logs show orchestration attempt even if Neutron L3 backend is limited in Docker",
            "Students understand production attach-port workflow before field deployment",
            "Board appears as network participant — not just HTTP endpoint behind NAT",
            "Foundation for SLICES multi-site experiments (Ch.10–11) using Neutron overlays",
            "Optional module — skip gracefully if short on time without blocking other modules",
        ]),

        ("section", "Hands-on — explore boards and ports", "attach-port.sh helper scripts"),

        ("hands_on", "Step 1 — List boards and existing ports", [
            "$ cd training",
            "$ ./experiments/virtual-networking/attach-port.sh boards",
            "$ ./experiments/virtual-networking/attach-port.sh list",
            "Note Active board UUID(s) and any existing port attachments",
        ]),

        ("image", "Horizon IoT — Boards (attach port context)",
         "chapter13/horizon-boards-dashboard.png",
         "http://{{VM_IP}}/horizon/iot/ · login {{HZ_CRED}} · select Active board", "", True),

        ("theory", "attach-port.sh script internals", [
            "Script wraps IoTronic REST API with lab-friendly output formatting",
            "boards subcommand: GET /v1/boards/ — filters Active boards",
            "list subcommand: GET /v1/boards/{uuid}/ports/ — shows existing VIF attachments",
            "Uses Conductor at http://{{VM_IP}}:8812 — same endpoint as Module A API checks",
            "Token acquisition: script reads from env or prompts — see script header for details",
            "Safe to re-run list after attach to confirm new port appears in response JSON",
        ], "training/experiments/virtual-networking/attach-port.sh"),

        ("section", "Hands-on — attach port via API", "POST when network UUID known"),

        ("code", "Step 2 — Attach port API call",
         'curl -X POST http://{{VM_IP}}:8812/v1/boards/{BOARD_UUID}/ports/ \\\n'
         '  -H "X-Auth-Token: $TOKEN" -H "Content-Type: application/json" \\\n'
         '  -d \'{"network": "{NETWORK_UUID}"}\'',
         "Replace BOARD_UUID from boards listing · NETWORK_UUID from Neutron/Horizon if available"),

        ("theory", "Expected API response fields (Ch.5)", [
            "VIF_name: logical interface identifier assigned by IoTronic/Neutron",
            "ip address: overlay IP reachable within the Neutron network context",
            "MAC_add: hardware address for L2 operations on the overlay segment",
            "Empty or error response: Neutron backend may not be fully wired in Docker lab",
            "Partial success still demonstrates API contract students will use in production",
            "Compare response schema with Ch.5 API tables in the book listing",
        ], "Ch.5 · ports API response schema"),

        ("theory", "TUN/TAP and edge-side networking (Ch.5)", [
            "Virtual interfaces on board appear as tun/tap devices in Linux network stack",
            "ip link show on board container reveals new interface after successful attach",
            "Applications bind to assigned overlay IP — no change to physical NIC configuration",
            "Edge routing tables may need update for multi-homed board scenarios (advanced)",
            "WSTUN (Module F) solves different problem: HTTP service exposure via NAT traversal",
            "VN + WSTUN complement each other in full S4T production deployments",
        ], "Ch.5 · edge virtual interface · TUN/TAP"),

        ("hands_on", "Step 3 — Verify WAgent logs", [
            "$ docker logs iotronic-wagent 2>&1 | tail -30",
            "Look for port attach / VIF configuration messages",
            "If no Neutron network UUID available: document API attempt for instructor review",
        ]),

        ("theory", "VN vs WSTUN — comparison table (Ch.5 vs Ch.14)", [
            "VN (this module): L2/L3 overlay — board gets IP on Neutron network",
            "WSTUN (Module F): L7 reverse tunnel — board HTTP service exposed on public port",
            "VN use case: cloud VM pings board overlay IP; microservice-to-sensor direct TCP",
            "WSTUN use case: curl http://{{VM_IP}}:50002/ reaches nginx on board port 50000",
            "Production: both enabled simultaneously for different application patterns",
            "Lab Docker stack: WSTUN fully functional; VN demonstrates API + WAgent workflow",
        ], "Ch.5 · Ch.14 §14.3 · Module F cross-reference"),

        ("section", "Validate & further reading", "Production Neutron requirements"),

        ("hands_on", "Step 4 — Validate VN module", [
            "$ cd training && ./validate-lab-vn.sh",
            "Script checks API reachability and WAgent container health",
        ]),

        ("theory", "Production deployment requirements (Ch.5)", [
            "Full OpenStack Neutron with ML2 plugin and network agent on compute nodes",
            "IoTronic Conductor + WAgent deployed as OpenStack services (not Docker lab compose)",
            "Board Lightning-Rod agent version compatible with IoTronic ports API version",
            "Network UUIDs managed via Horizon Network panel or neutron CLI",
            "SLICES RI testbeds (Ch.10) provide production-grade Neutron for experimenters",
            "Reference repo: github.com/AssemblingSmartCPS/ch05 — Neutron port specs",
        ], "Ch.5 · production checklist · ch05 repo"),

        ("content", "Module E checklist & reference", [
            "□ attach-port.sh boards lists Active board from Module A",
            "□ Port attach API call attempted (or documented why Neutron UUID unavailable)",
            "□ WAgent logs inspected for orchestration messages",
            "□ Student can explain VN vs WSTUN difference",
            "Reference: Book Ch.5 tables · github.com/AssemblingSmartCPS/ch05",
        ]),
    ]
