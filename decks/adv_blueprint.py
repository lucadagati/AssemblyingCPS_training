"""Module H — SLICES Blueprint & K3s (Ch.11)."""


def slides() -> list:
    return [
        ("title", "Module H — SLICES Cloud Continuum Blueprint",
         "Ch.11 · Advanced · VM {{VM_IP}}",
         "Advanced · Ch.11 — Blueprint & K3s · do NOT run with Module G FL simultaneously"),

        ("section", "Blueprint theory", "Ch.11 — Crossplane + K8s + S4T before kubectl hands-on"),

        ("theory", "SLICES Cloud Continuum Blueprint (Ch.11 abstract)", [
            "Replicable software + hardware + methodologies for distributed edge–fog–cloud experiments",
            "Three resource layers: Infrastructure / Service / Workflow (application/experiment)",
            "Crossplane: Kubernetes-native control plane provisioning internal + external resources",
            "Enables reproducible experiments on SLICES RI testbeds across European research sites",
            "Blueprint decouples experiment definition (YAML) from underlying infrastructure provider",
            "Book chapter bridges Part I Cloud Continuum theory (Ch.2–3) with Part II S4T ops (Ch.13+)",
        ], "Ch.11 · SLICES Blueprint chapter · abstract"),

        ("theory", "Three resource layers explained (Ch.11)", [
            "Infrastructure layer: compute, network, storage — physical machines or virtual instances",
            "Service layer: system features — Pub/Sub overlay, inter-cluster L3, distributed storage access",
            "Workflow layer: application/experiment workloads — echo services, FL pipelines, IoT plugins",
            "Decoupling lets experimenters compose environments declaratively without manual provisioning",
            "Crossplane Composite Resources (XRs) map layers to provider-specific implementations",
            "Same Blueprint manifest deploys on SLICES site A or lab VM with provider config change only",
        ], "Ch.11 § methodology · three-layer model"),

        ("theory", "Infrastructure layer detail (Ch.11)", [
            "Compute: VMs, bare metal, K3s worker nodes — including S4T edge boards as K3s agents",
            "Network: Neutron overlays (Ch.5), Istio service mesh, MetalLB load balancer IPs",
            "Storage: Ceph, Longhorn, or local PV for experiment artifact persistence",
            "Crossplane Provider Config connects to OpenStack, AWS, or local K3s API endpoint",
            "Lab Module H: K3s on {{VM_IP}} provides Infrastructure layer substrate",
            "Docker Compose S4T (Modules A–F) coexists as separate runtime on same VM",
        ], "Ch.11 · Infrastructure layer · K3s edge deployment"),

        ("theory", "Service layer detail (Ch.11)", [
            "Pub/Sub overlay: Crossbar WAMP in S4T stack — already running in Docker compose lab",
            "Inter-cluster L3: Neutron + Istio enable pod-to-board connectivity across clusters",
            "Identity: Keystone in OpenStack S4T; Kubernetes RBAC + OIDC/Keycloak in Blueprint deploy",
            "Service layer resources defined as Crossplane Compositions — reusable across experiments",
            "CEP (Cloud Edge Platform) echo demo in ch11 repo validates service layer connectivity",
            "Students map Module A Crossbar service to Service layer in three-layer taxonomy",
        ], "Ch.11 · Service layer · CEP echo demo listing"),

        ("theory", "Workflow layer detail (Ch.11)", [
            "Experiment workloads: IoT plugin injection, FL training job, environmental publisher",
            "Workflow manifests reference Service + Infrastructure outputs as dependencies",
            "GitOps: workflow YAML in git repo → Crossplane reconciles desired state continuously",
            "Ch.14 plugin CRD: inject HelloName on fleet defined as Kubernetes custom resource",
            "Ch.19 FL workflow: Flower server + client plugins as Workflow layer composition",
            "Module H demo: kubectl apply S4T K3s manifests → Workflow-ready cluster substrate",
        ], "Ch.11 · Workflow layer · experiment composition"),

        ("theory", "Experiment type taxonomy (Ch.11)", [
            "Type 1: architectural paradigms — hybrid cloud, edge-cloud, serverless, microservices",
            "Type 2: performance & optimization — latency, autoscaling, data placement strategies",
            "Type 3: security & trust — RBAC, OIDC/Keycloak, multi-tenant isolation patterns",
            "Type 4: AI/ML workflows — federated learning, inference at edge, model serving",
            "Training modules map: G=Type4, I=Type1 serverless, D+F=Type1 microservices at edge",
            "Blueprint lets researchers declare experiment type in metadata for reproducibility",
        ], "Ch.11 § four experiment categories"),

        ("theory", "Keycloak / OIDC identity for experiments (Ch.11)", [
            "Blueprint integrates Keycloak as OpenID Connect provider for experiment access control.",
            "Experiment groups map to Kubernetes RBAC roles — who may apply Crossplane CRDs.",
            "OIDC tokens authenticate researchers against SLICES-RI Resource Catalogue entries.",
            "Contrasts with lab Docker Compose: Keystone provides Horizon auth in Modules A–F.",
            "Production Blueprint deploys Keycloak alongside Crossplane on the K3s control plane.",
            "Enables multi-tenant experiment namespaces with federated identity across SLICES sites.",
        ], "Ch.11 § Keycloak · OIDC · experiment groups"),

        ("theory", "CEP echo demo — Cloud Edge Platform (Ch.11)", [
            "CEP (Cloud Edge Platform) provider orchestrates multi-cluster echo services.",
            "Reference implementation validates Service layer connectivity across experiment sites.",
            "Echo pods prove L3 reachability between cloud VM and edge board before S4T workload.",
            "Repo ch11_s4t-k3s-deploy includes CEP-related manifests for classroom YAML review.",
            "Lab Module H: review manifests + optional kubectl apply when K3s is pre-provisioned.",
            "Workflow layer experiments (plugins, FL) assume CEP-validated network substrate.",
        ], "Ch.11 · CEP echo demo · ch11_s4t-k3s-deploy README"),

        ("theory", "Crossplane + S4T provider (Ch.11)", [
            "Crossplane Provider for S4T: boards, plugins, fleets as Kubernetes CRDs",
            "Declarative manifests → provider controller translates to IoTronic REST API calls",
            "Repo: github.com/AssemblingSmartCPS/ch11_xplane-provider-for-s4t",
            "Enables GitOps-style IoT fleet management from kubectl apply -f fleet.yaml",
            "Provider watches CRD status — reports Active/Error analogous to Horizon board status",
            "Bridges Kubernetes ecosystem (Helm, ArgoCD) with S4T IoTronic operational model",
        ], "Ch.11 · Crossplane provider footnote · ch11_xplane-provider-for-s4t"),

        ("theory", "S4T on Kubernetes — full stack (Ch.11)", [
            "Complete S4T stack as K8s pods: conductor, UI, Crossbar, WSTUN, MariaDB, WAgent, …",
            "K3s: lightweight Kubernetes — single binary, suitable for edge/single-node lab deployments",
            "MetalLB: bare-metal load balancer — assigns external IPs to K8s Services",
            "Istio: service mesh — mTLS, traffic management between S4T microservices",
            "Repo: github.com/AssemblingSmartCPS/ch11_s4t-k3s-deploy — YAML manifests + README",
            "Lab: light deploy verifies pod scheduling — full Istio/MetalLB optional for classroom",
        ], "Ch.11 · Stack4Things IoTronic on K8s · ch11_s4t-k3s-deploy"),

        ("theory", "SLICES RI integration (Ch.10–11 bridge)", [
            "SLICES: distributed research infrastructure across European academic/industry sites",
            "Resource Catalogue + Slice Central Controller coordinate multi-site experiment setup",
            "CIP/CEP Crossplane providers provision experiment namespaces on SLICES nodes",
            "IoT boards join experiments via S4T plugin CRD injection at runtime on edge sites",
            "Blueprint ensures experiment reproducibility: same YAML on SLICES-IT and SLICES-FR sites",
            "Module H lab on {{VM_IP}} simulates single-site Blueprint deployment pattern",
        ], "Ch.10 SLICES RI · Ch.11 CEP echo demo · Slice Central Controller"),

        ("theory", "K3s lifecycle plugin for IoT boards (Ch.11 + Ch.14)", [
            "Ch.14 documents K3s join plugin — attaches physical boards as K3s worker nodes",
            "Board runs k3s agent — registers with K3s server on cloud/edge controller node",
            "Enables running Kubernetes pods directly on IoT hardware at the edge",
            "Blueprint Workflow layer can schedule pods onto board-workers by node label",
            "Theory→ops bridge: Module D fleet boards could become K3s workers in advanced setup",
            "Not fully exercised in classroom lab — documented for research/experiment context",
        ], "Ch.11 + Ch.14 K3s lifecycle plugin · edge worker pattern"),

        ("image", "Blueprint three layers",
         "diagrams/blueprint-layers.png",
         "Infrastructure / Service / Workflow — Crossplane orchestration"),

        ("content", "Module H — learning objectives", [
            "Explain Ch.11 three-layer Blueprint model and four experiment type categories",
            "Understand Crossplane + S4T provider CRD mapping to IoTronic API",
            "Install K3s and verify kubectl get nodes shows Ready",
            "Optional: kubectl apply S4T K3s manifests — observe pods Running",
            "Articulate Docker Compose S4T vs K3s S4T coexistence on same VM",
        ]),

        ("content", "Module H — 50-minute timeline", [
            "0–20 min  — Blueprint theory: layers, taxonomy, Crossplane, SLICES RI",
            "20–25 min — DEMO GOAL review + RAM gate check (≥ 8 GB, no Module G FL)",
            "25–40 min — HANDS-ON: K3s install (or verify pre-provisioned) + kubectl basics",
            "40–50 min — Optional light S4T K3s deploy + checklist wrap-up",
        ]),

        ("demo", "What Module H demonstrates — demo goals", [
            "Same VM hosts Docker S4T (Modules A–F) AND K3s (separate containerd runtime)",
            "kubectl apply from ch11 manifests deploys S4T microservices as Kubernetes pods",
            "Crossplane CRDs bridge K8s GitOps workflow with IoTronic REST API operations",
            "K3s lifecycle plugin (Ch.14) theory connects IoT boards to K8s worker model",
            "Students classify training modules within Ch.11 experiment type taxonomy",
            "Blueprint provides research-grade reproducibility framework beyond Docker lab compose",
        ]),

        ("content", "Reference repos & RAM gate", [
            "github.com/AssemblingSmartCPS/ch11_xplane-provider-for-s4t",
            "github.com/AssemblingSmartCPS/ch11_s4t-k3s-deploy",
            "RAM: ≥ 8 GB recommended for K3s + Docker S4T coexistence",
            "Do NOT run Module G FL and Module H K3s on same VM simultaneously",
            "K3s cluster can be pre-provisioned before the session to save install time.",
        ]),

        ("section", "Hands-on — K3s prerequisite check", "RAM gate before cluster install"),

        ("hands_on", "Step 1 — RAM gate + prerequisite check", [
            "$ free -h    # ≥ 8 GB recommended; stop Module G FL if running",
            "$ training/experiments/blueprint/k3s-prereq.sh",
            "If RAM insufficient: use dedicated VM for Blueprint or skip optional pod deploy",
        ]),

        ("theory", "Docker S4T vs K3s S4T on same VM (Ch.11)", [
            "Docker Compose S4T uses dockerd; K3s uses containerd — separate container runtimes",
            "Both can coexist on {{VM_IP}} — but compete for RAM and CPU during class",
            "Recommended classroom pattern: Docker stack during Modules A–F; K3s demo in Module H only",
            "Alternative: dedicated VM for Blueprint module — cleaner resource isolation",
            "Port conflicts: K3s API :6443, Docker S4T services unchanged on existing ports",
            "Pre-provision K3s overnight when session time is limited.",
        ], "Ch.11 + instructor playbook · resource planning"),

        ("section", "Lab: K3s install and verify", "Single-node cluster on training VM"),

        ("hands_on", "Step 2 — Install K3s (instructor pre-step if needed)", [
            "$ curl -sfL https://get.k3s.io | sh -",
            "$ export KUBECONFIG=/etc/rancher/k3s/k3s.yaml",
            "$ kubectl get nodes",
            "Expected: single node Ready — hostname of {{VM_IP}} lab VM",
        ]),

        ("hands_on", "Step 3 — Verify cluster health", [
            "$ kubectl get pods -A",
            "Expected: kube-system pods Running (coredns, metrics-server, local-path-provisioner)",
            "$ kubectl cluster-info",
        ]),

        ("section", "Hands-on — optional S4T K3s light deploy", "Follow ch11_s4t-k3s-deploy README"),

        ("hands_on", "Step 4 — Light deploy S4T pods (optional)", [
            "$ cd training/repos/ch11_s4t-k3s-deploy",
            "# Follow README: kubectl apply -f yaml_file/",
            "$ kubectl get pods -A",
            "Look for S4T conductor, crossbar, or UI pods — Running status",
        ]),

        ("theory", "Crossplane provider demo workflow (Ch.11)", [
            "Install Crossplane on K3s: helm install crossplane — namespace crossplane-system",
            "Install Provider S4T: kubectl apply provider.yaml from ch11_xplane-provider-for-s4t",
            "Apply Board CRD manifest: kubectl apply -f examples/board-alpha.yaml",
            "Provider controller calls IoTronic API at {{VM_IP}}:8812 — creates board resource",
            "Status field on CRD reflects Active/Error — parallel to Horizon board panel",
            "Full provider demo optional — theory slides sufficient if time constrained",
        ], "ch11_xplane-provider-for-s4t · ProviderConfig example"),

        ("theory", "GitOps workflow for IoT fleets (Ch.11)", [
            "Fleet YAML in git: defines board members + plugin inject specifications",
            "ArgoCD or Flux watches git repo — reconciles cluster state on every commit",
            "Change plugin version in git → Crossplane provider re-injects on all fleet members",
            "Audit trail: git history records who changed fleet configuration and when",
            "Production SLICES sites use this pattern for multi-site experiment reproducibility",
            "Contrasts with Horizon manual inject in Module D — operational maturity step",
        ], "Ch.11 · GitOps · Crossplane composition pattern"),

        ("section", "Validate & wrap-up", "K3s Ready + optional pods Running"),

        ("hands_on", "Step 5 — Blueprint module validation", [
            "$ training/experiments/blueprint/k3s-prereq.sh",
            "$ kubectl get nodes -o wide",
            "Document: K3s Ready + (optional) S4T pods Running",
        ]),

        ("content", "Module H checklist", [
            "□ k3s-prereq.sh passes · free -h shows adequate RAM",
            "□ kubectl get nodes shows Ready",
            "□ (Optional) S4T pods Running in K3s cluster",
            "□ Student can explain three Blueprint layers with S4T examples",
            "□ Do NOT run with Module G FL simultaneously",
            "Reference: github.com/AssemblingSmartCPS/ch11_xplane-provider-for-s4t · ch11_s4t-k3s-deploy",
        ]),
    ]
