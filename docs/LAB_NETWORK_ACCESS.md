# Lab network access — Tailscale, LAN, external boards, demo URLs

This document explains how clients reach the Stack4Things lab VM and how to
attach boards that are **not** Docker containers on the lab host.

---

## 1. Addresses on the lab VM

| Interface | Typical address | Who uses it |
|-----------|-----------------|-------------|
| LAN `ens18` | `192.168.100.11/24` | Same L2/L3 campus/lab network |
| Tailscale primary `tailscale0` | e.g. `100.74.114.23` (`asseblingcps`) | Account A (instructor / lukkinen) |
| Tailscale secondary `tailscale1` | e.g. `100.123.142.39` (`lab-secondary`) | Account B (e.g. gmerlino) |

Docker publishes S4T ports on **`0.0.0.0`**, so the **same TCP ports** answer on
LAN and on every Tailscale IP of this VM.

Set `vm-ip.txt` (gitignored) to the IP you want scripts/`S4T_LAB_HOST` to print
for operators on **your** network (often the primary Tailscale IP).

---

## 2. Ports exposed on the VM (not only Docker-internal)

| Port | Service | Needed by external board? |
|-----:|---------|---------------------------|
| **80** | Horizon + `/lab-ws/` demo proxy | No (browser only) |
| **8181** | Crossbar WAMP (`wss`) | **Yes** (registration + online) |
| **8080** | WSTUN control | Yes (cloud services / tunnels) |
| **50001–50100** | WSTUN reverse tunnels | Yes when enabling HTTP/SSH services |
| 8812 | IoTronic API | No (Horizon/server-side) |
| 5000 | Keystone | No |
| 1474–1479+ | Lightning-Rod UIs (lab containers) | No |

**Not published:** `iotronic-wagent` (Docker-only). Boards talk to **Crossbar**,
not directly to wagent.

Docker DNS names (`crossbar`, `iotronic-wstun`) resolve **only** on the compose
network. External devices must use the VM IP and/or `/etc/hosts` aliases.

---

## 3. Demo / WoT URLs independent of Tailscale IP

Horizon shows Public URLs as:

```text
http://<host-you-used-for-Horizon>/lab-ws/<public_port>/
```

Examples (same path, different ingress):

| Ingress | wot-fritzing |
|---------|--------------|
| Primary Tailscale | `http://100.74.114.23/lab-ws/50006/` |
| Secondary Tailscale | `http://100.123.142.39/lab-ws/50006/` |
| LAN | `http://192.168.100.11/lab-ws/50006/` |

Direct URLs `http://<host>:50006/` still work (ports are published) but prefer
`/lab-ws/` in slides and student sheets.

Apache config: `patches/apache-wot-ws-proxy.conf` (enabled as `00-wot-ws-proxy.conf`).

---

## 4. Dual Tailscale (`lab-secondary`) — self-service

If a second account needs its own node on **this** VM:

| | Primary | Secondary |
|--|---------|-----------|
| systemd | `tailscaled` | `tailscaled2` |
| socket | `/run/tailscale/tailscaled.sock` | `/run/tailscale2/tailscaled.sock` |
| state | `/var/lib/tailscale/` | `/var/lib/tailscale2/` |
| TUN / UDP | `tailscale0` / 41641 | `tailscale1` / 41642 |
| CLI helper | `tailscale` | `lab-secondary-ts` |

```bash
sudo systemctl status tailscaled2
sudo systemctl start tailscaled2          # if down
lab-secondary-ts up --hostname=lab-secondary
lab-secondary-ts status
lab-secondary-ts ip -4
```

Users on the **secondary** tailnet open Horizon/demos via the secondary IP
(e.g. `100.123.142.39`), **not** the primary `100.74.114.23` (different tailnet).

---

## 5. External board on the same Tailscale (or LAN)

Goal: a physical/virtual board outside Docker, online in IoTronic.

### 5.1 Create the board in Horizon
IoT → Create Board → copy **registration code**.

### 5.2 Make TLS hostname match (recommended)
Crossbar cert CN is `crossbar`. On the board:

```bash
# Point names at the lab VM (use the Tailscale or LAN IP that board can route)
echo "<LAB_VM_IP> crossbar iotronic-wstun" | sudo tee -a /etc/hosts
```

Install the lab CA (from the VM):

```bash
docker exec crossbar cat /node/.crossbar/ssl/iotronic_CA.pem
# install into LR ssl trust store on the board (/var/lib/iotronic/ssl/ …)
```

### 5.3 Lightning-Rod first-boot Config
| Field | Value |
|-------|--------|
| WAMP / urlwagent | `wss://crossbar:8181/` |
| Code | registration code from Horizon |
| Hostname | board name |
| Realm | `s4t` (lab default) |

Alternative without `/etc/hosts`: `wss://<LAB_VM_IP>:8181/` — often fails TLS
verify (CN ≠ IP); avoid unless you disable verification.

### 5.4 Connectivity checks from the board

```bash
ping -c2 <LAB_VM_IP>
nc -vz crossbar 8181
nc -vz iotronic-wstun 8080
```

### 5.5 Cloud services (SSH tunnel, HTTP expose)
Ensure `wstun` is reachable (hosts entry or `wstun_ip` = lab VM IP). Public HTTP
services then appear under `/lab-ws/<port>/` when opened through Horizon.

---

## 6. Operator quick reference

```bash
# Which IP am I advertising?
tailscale ip -4
lab-secondary-ts ip -4 2>/dev/null || true
ip -4 addr show ens18 | grep inet

# Is Crossbar / wstun published?
ss -lntp | grep -E ':8181|:8080|:80 '

# Demo path health
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1/lab-ws/50006/
```

---

## 7. Related files

| Path | Role |
|------|------|
| `vm-ip.txt` / `vm-ip.txt.example` | Operator-facing IP for scripts |
| `PORT_FORWARDING.md` | Browser URL tables |
| `swc2026/` | Conference create/destroy LR helpers |
| `patches/apache-wot-ws-proxy.conf` | `/lab-ws/` proxy |
| `experiments/multiboard/lr_log_proxy.py` | LR provision + log tail |
