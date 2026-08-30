# Training modules — book chapters → decks → repos

| ID | Module | Chapter | Deck | GitHub repo |
|----|--------|---------|------|-------------|
| A | Deploy I/Ocloud | Ch.4 + Ch.13 | `ModuleA_Deploy_IOcloud_EN.pptx` | [ch13](https://github.com/AssemblingSmartCPS/ch13) |
| B | Plugins & Services | Ch.14 | `ModuleB_Plugin_Services_EN.pptx` | [ch14](https://github.com/AssemblingSmartCPS/ch14) |
| C | IoT-hosted Computation | Ch.15 | `ModuleC_IoT_Computation_EN.pptx` | [ch15](https://github.com/AssemblingSmartCPS/ch15) |
| D | Multi-board & Fleet | Ch.13–14 | `ModuleD_MultiBoard_EN.pptx` | ch13 overlay |
| E | Virtual Networking | Ch.5 | `ModuleE_VirtualNetworking_EN.pptx` | [ch05](https://github.com/AssemblingSmartCPS/ch05) |
| F | Web Services & WoT | Ch.6 + Ch.14 | `ModuleF_WebServices_WoT_EN.pptx` | [ch14](https://github.com/AssemblingSmartCPS/ch14) demos |
| G | Federated Learning | Ch.19 | `ModuleG_FederatedLearning_EN.pptx` | [ch19](https://github.com/AssemblingSmartCPS/ch19) |
| H | Blueprint & K3s | Ch.11 | `ModuleH_Blueprint_K3s_EN.pptx` | [ch11_s4t-k3s-deploy](https://github.com/AssemblingSmartCPS/ch11_s4t-k3s-deploy), [ch11_xplane-provider-for-s4t](https://github.com/AssemblingSmartCPS/ch11_xplane-provider-for-s4t) |
| I | FaaS / Deviceless | Ch.7 | `ModuleI_FaaS_Deviceless_EN.pptx` | (theory — contrasts B/C/F on same stack) |

Clone all repos: `scripts/clone-repos.sh`

Generate slides: `.venv/bin/python generate_slides_modular_en.py`

Placeholders: `{{VM_IP}}`, `{{HZ_CRED}}`, `{{LR_CRED}}` — kept in PPTX for students; set `S4T_RESOLVE_VM_IP=1` only for instructor preview builds.
