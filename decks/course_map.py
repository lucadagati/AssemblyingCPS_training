"""Course map deck — modular training paths."""


def slides() -> list:
    return [
        ("title", "S4T Modular Training — Course Map",
         "3h core → 6h standard → 9h full · Lab VM {{VM_IP}}",
         "Assembling Smart CPS · Part II hands-on"),

        ("section", "Training philosophy", "Theory from the book · demo on the lab VM"),

        ("theory", "How to use these decks", [
            "Each module combines book theory with live lab exercises on the Stack4Things VM.",
            "Core path (3h): Modules A + B + C — deploy, plugins, environmental data service.",
            "Standard (6h): Core plus multi-board fleet, virtual networking, and web services.",
            "Full (9h): All modules including federated learning, blueprint, and FaaS concepts.",
            "Lab URLs use {{VM_IP}} — resolved automatically when slides are built.",
            "Run validation scripts after each module to confirm the environment is healthy.",
        ], "training/docs/MODULES.md · placeholders.py"),

        ("theory", "Modular timing model", [
            "Minimum (3h): Modules A + B + C — deploy, plugins, environmental publisher.",
            "Standard (6h): Core + D Multi-board + E Virtual Networking + F Web Services.",
            "Full (9h): Core + all extensions + G FL + H Blueprint + I FaaS theory.",
            "Module E (Virtual Networking) is optional when Neutron backend is unavailable.",
            "Modules G and H should not run on the same VM simultaneously (RAM ≥ 8 GB).",
            "Each deck is self-contained; pick the path that matches your session length.",
        ], "training/docs/MODULES.md"),

        ("content", "Training paths — pick one", [
            "3h  CORE     → A+B+C · deliverable: Active board + HelloName + InfluxDB rows",
            "6h  STANDARD → Core + D fleet + E VN (opt.) + F WoT/WSTUN tunnels",
            "9h  FULL     → Standard + G FL rounds + H Blueprint/K3s + I FaaS taxonomy",
            "Credentials: Horizon {{HZ_CRED}} · Lightning-Rod {{LR_CRED}}",
            "Materials: github.com/lucadagati/AssemblyingCPS_training",
        ]),

        ("section", "Lab workflow", "End-to-end pipeline — UML sequence"),

        ("theory", "Training lab workflow — five steps", [
            "Step 1: Clone AssemblingSmartCPS org repos (ch13, ch14, ch15, ch05, ch19, ch11) via scripts/clone-repos.sh.",
            "Step 2: Start Stack4Things with Docker Compose + training/patches/docker-compose.lab.yml overlay.",
            "Step 3: Run validate/validate-all.sh — all module checks must PASS before the session.",
            "Step 4: Use pre-built PPTX in slides/ or regenerate with scripts/generate_diagrams.py + generate_slides_modular_en.py.",
            "Step 5: Deliver modules A–I using Module*.pptx decks; re-run module validators after each lab block.",
            "Public repo: github.com/lucadagati/AssemblyingCPS_training",
        ], "scripts/build-all.sh · INSTRUCTOR_PLAYBOOK.md"),

        ("image", "UML — End-to-end training workflow",
         "diagrams/seq-training-workflow.png",
         "Clone repos → Docker up → validate → generate slides → teach modules A–I"),

        ("theory", "Per-module UML sequence diagrams", [
            "Each module deck includes sequence diagrams for the primary hands-on workflow (not only architecture boxes).",
            "Module A: board onboarding — Horizon → Conductor → Crossbar → Lightning-Rod → Active.",
            "Module B: sync Plugin Call — inject → WAMP rpc → Worker.run() → result to Horizon.",
            "Module C: async loop — Start plugin → CSV row → InfluxDB every 30s.",
            "Module D: fleet inject to three boards · Module F: ServiceEnable + WSTUN tunnel.",
            "Module G: Flower FedAvg round across three edge clients.",
        ], "diagrams/seq-*.png · generate_diagrams.py"),

        ("section", "Book coverage map", "Part II hands-on chapters → training modules"),

        ("theory", "Part I background — when to read before labs", [
            "Ch.1–3: cloud continuum foundations — context for why S4T extends OpenStack to IoT.",
            "Ch.8: authentication and authorization — explains Keystone role in Horizon login.",
            "Ch.9: heterogeneous compute — motivates edge vs cloud placement decisions in plugins.",
            "Ch.10: SLICES research infrastructure — precursor to Ch.11 Blueprint module.",
            "Ch.12: summary chapter — useful recap after completing core Modules A–C.",
            "Part I is referenced throughout decks; deep read of Ch.4 before Module A is essential.",
        ], "Book Part I · Ch.1–12 · intro.tex"),

        ("theory", "Core modules — Ch.4, Ch.13–15", [
            "Ch.4  I/Ocloud foundations → context for Module A (Virtual Nodes, IoTronic)",
            "Ch.13 Docker deploy + board onboarding → Module A: Active board deliverable",
            "Ch.14 Plugins, fleet, web services → Module B sync HelloName + fleet preview",
            "Ch.15 Environmental publisher + TOO(L)SMART → Module C async → InfluxDB",
            "Part I chapters (Ch.1–12) provide theory referenced throughout core decks",
            "Students should read Ch.13 abstract before Module A lab session",
        ], "Book Part II · intro.tex · Ch.4 I/Ocloud"),

        ("theory", "Extension modules — Ch.5, Ch.6, Ch.14", [
            "Ch.5  Virtual networking attach-port → Module E: IoTronic ports API workflow",
            "Ch.6  Web of Things layered model → Module F: gateway WoT before WSTUN demo",
            "Ch.14 Fleet operations + Web Services Manager → Module D fleet inject + Module F",
            "Extension tier adds +45–60 min per module; D is prerequisite for G (FL clients)",
            "Module F contrasts book weather server :8080 with lab nginx :50000 tunnel demo",
            "All extension decks use {{VM_IP}} for Horizon, API, and curl examples",
        ], "Ch.5 · Ch.6 · Ch.14 §14.2–14.3"),

        ("theory", "Advanced modules — Ch.7, Ch.11, Ch.19", [
            "Ch.19 Federated Learning on edge boards → Module G: Flower + 3 LR clients",
            "Ch.11 SLICES Blueprint + Crossplane + K3s → Module H: declarative IoT GitOps",
            "Ch.7  FaaS / Deviceless paradigm → Module I: sync vs async plugin contrast",
            "Advanced tier: theory-heavy; Module H benefits from a pre-provisioned K3s cluster.",
            "Module G needs Module D complete (3 Active boards on :1474/:1475/:1476)",
            "Module H K3s install should run overnight — do NOT concurrent with Module G",
        ], "Ch.7 · Ch.11 · Ch.19"),

        ("content", "Module A — Deploy I/Ocloud (CORE, 60 min)", [
            "Ch.13 + Ch.4 · Docker Compose + board onboarding → Active board in Horizon",
            "Deck: ModuleA_Deploy_IOcloud_EN.pptx",
            "Validate: ./training/validate-lab.sh (18 core checks)",
        ]),

        ("content", "Module B — Plugins & Services (CORE, 60 min)", [
            "Ch.14 · HelloName sync Plugin Call + optional Docker lifecycle + fleet preview",
            "Deck: ModuleB_Plugin_Services_EN.pptx",
            "Builds on Module A — board must be Active before inject",
        ]),

        ("content", "Module C — Environmental IoT Computation (CORE, 60 min)", [
            "Ch.15 · Async environmental_data publisher → InfluxDB · TOO(L)SMART wrap-up",
            "Deck: ModuleC_IoT_Computation_EN.pptx",
            "Contrasts with Module B sync plugin — continuous PaaS-style service",
        ]),

        ("content", "Module D — Multi-board & Fleet (EXT, +45–60 min)", [
            "Ch.13–14 · 3 LR instances :1474/1475/1476 · fleet inject HelloName",
            "Deck: ModuleD_MultiBoard_EN.pptx",
            "Prerequisite for Module G (Federated Learning needs 3 clients)",
        ]),

        ("content", "Module E — Virtual Networking (EXT, +45–60 min, OPTIONAL)", [
            "Ch.5 attach-port · IoTronic ports API · WAgent orchestration",
            "Deck: ModuleE_VirtualNetworking_EN.pptx",
            "Skip if short on time or Neutron L3 incomplete in Docker lab",
        ]),

        ("content", "Module F — Web Services, WSTUN & WoT (EXT, +30–45 min)", [
            "Ch.6 + Ch.14 · WSTUN tunnel · Designate optional · book weather vs lab nginx",
            "Deck: ModuleF_WebServices_WoT_EN.pptx",
            "Validate: ./training/validate-lab-wstun.sh",
        ]),

        ("content", "Module G — Federated Learning (ADV, +60–90 min)", [
            "Ch.19 · Flower server · 3 edge clients · requires Module D complete",
            "Deck: ModuleG_FederatedLearning_EN.pptx",
            "Do NOT run simultaneously with Module H (K3s RAM gate)",
        ]),

        ("content", "Module H — SLICES Blueprint & K3s (ADV, +45–60 min)", [
            "Ch.11 · Crossplane provider + K3s deploy · GitOps for IoT fleets",
            "Deck: ModuleH_Blueprint_K3s_EN.pptx",
            "K3s cluster should be installed before the session on a dedicated VM.",
        ]),

        ("content", "Module I — FaaS & Deviceless (ADV, +30–45 min)", [
            "Ch.7 theory · sync HelloName vs async environmental on same LR",
            "Deck: ModuleI_FaaS_Deviceless_EN.pptx",
            "No new infrastructure — conceptual bridge across Modules B, C, F",
        ]),

        ("content", "Validation scripts & lab hygiene", [
            "./training/validate-lab.sh — core 18 checks after Module A–C",
            "./training/validate-lab-multiboard.sh · validate-lab-vn.sh",
            "./training/validate-lab-wstun.sh · validate-lab-fl.sh",
            "Run relevant script before each module; fix failures before proceeding",
        ]),

        ("content", "Lab prerequisites", [
            "Docker and Docker Compose installed; user in the docker group.",
            "Horizon: http://{{VM_IP}}/horizon — credentials {{HZ_CRED}}.",
            "Lightning-Rod UI: http://{{VM_IP}}:1474 — credentials {{LR_CRED}}.",
            "At least 4 GB free RAM (8 GB if running Module G or H).",
        ]),
    ]
