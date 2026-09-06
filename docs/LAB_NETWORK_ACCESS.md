# Lab network access — ports, URLs, external boards

How clients reach the Stack4Things lab host and how to attach boards that are
**not** Docker containers on that host.

Use a single placeholder **`{{VM_IP}}`** (or `vm-ip.txt` / `S4T_LAB_HOST`) for
the address participants use to open Horizon — LAN, VPN, or any routable IP of
the lab machine. Do not hardcode site-specific addresses in slides or handouts.

---

## 1. Lab host address

| Source | Purpose |
|--------|---------|
| `vm-ip.txt` (gitignored; from `vm-ip.txt.example`) | Default IP printed by scripts |
| `S4T_LAB_HOST` | Environment override for the same value |
| Browser Host header | Horizon WoT panel builds demo URLs from the host you used to open the UI |

Docker publishes Stack4Things ports on **`0.0.0.0`**, so the same TCP ports answer
on every address assigned to the lab host.

---

## 2. Ports exposed on the lab host

| Port | Service | Needed by an external board? |
|-----:|---------|------------------------------|
| **80** | Horizon UI | No (browser) |
| **8181** | Crossbar WAMP (`wss`) | **Yes** (registration + stay online) |
| **8080** | WSTUN control | Yes (cloud services / tunnels) |
| **50001–50100** | WSTUN public tunnels | Yes when enabling HTTP/SSH services |
| 8812 | IoTronic API | No (server-side / Horizon) |
| 5000 | Keystone | No |
| 1474–1479+ | Lightning-Rod UIs (lab containers) | No |

**Not published:** `iotronic-wagent` (Docker network only). Boards talk to
**Crossbar**, not directly to wagent.

Docker DNS names (`crossbar`, `iotronic-wstun`) resolve **only** inside the
compose network. External devices must use `{{VM_IP}}` and/or `/etc/hosts`
aliases (see below).

---

## 3. Demo / WoT public URLs

Horizon builds Public URLs as **direct published ports** on the same host used
for the dashboard:

```text
http://{{VM_IP}}:<public_port>/
```

Examples (replace `{{VM_IP}}` and ports with your lab values):

| Service (typical) | URL |
|-------------------|-----|
| wot-fritzing | `http://{{VM_IP}}:50006/` |
| weather-wot | `http://{{VM_IP}}:50064/` |
| lr-nginx-demo | `http://{{VM_IP}}:50008/` |

Do **not** use `http://127.0.0.1:<port>/` from a remote browser: that address is
the client machine, not the lab host.

---

## 4. External board (physical or VM outside Docker)

Goal: a board on the same IP network (or VPN) as the lab host, online in IoTronic.

### 4.1 Create the board in Horizon
IoT → Create Board → copy the **registration code**.

### 4.2 Match the Crossbar TLS name (recommended)
The lab Crossbar certificate uses CN `crossbar`. On the board:

```bash
# Point names at the lab host IP the board can route to
echo "{{VM_IP}} crossbar iotronic-wstun" | sudo tee -a /etc/hosts
```

Install the lab CA (from the lab host):

```bash
docker exec crossbar cat /node/.crossbar/ssl/iotronic_CA.pem
# install into the Lightning-Rod trust store on the board
# (typically under /var/lib/iotronic/ssl/)
```

### 4.3 Lightning-Rod first-boot Config

| Field | Value |
|-------|--------|
| WAMP / urlwagent | `wss://crossbar:8181/` |
| Code | registration code from Horizon |
| Hostname | board name |
| Realm | `s4t` (lab default) |

Alternative without `/etc/hosts`: `wss://{{VM_IP}}:8181/` — TLS verification often
fails (CN ≠ IP); prefer the hosts alias.

### 4.4 Connectivity checks from the board

```bash
ping -c2 {{VM_IP}}
nc -vz crossbar 8181
nc -vz iotronic-wstun 8080
```

### 4.5 Cloud services (SSH tunnel, HTTP expose)
Ensure WSTUN is reachable (hosts entry or `wstun_ip` = lab host IP). Exposed HTTP
services are then reachable at `http://{{VM_IP}}:<public_port>/`.

---

## 5. Operator quick reference

```bash
# Address used by scripts
cat vm-ip.txt
echo "$S4T_LAB_HOST"

# Published listeners on the lab host
ss -lntp | grep -E ':8181|:8080|:80 |:8812'

# Demo health (example ports — adjust to your deployment)
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:50006/
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:50006/api/circuit
```

---

## 6. Related files

| Path | Role |
|------|------|
| `vm-ip.txt` / `vm-ip.txt.example` | Operator-facing lab host IP for scripts |
| `PORT_FORWARDING.md` | Browser URL tables |
| `lab-ops/` | Manual Lightning-Rod create/destroy helpers |
| `experiments/multiboard/lr_log_proxy.py` | LR provision + log tail |
