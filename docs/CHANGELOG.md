# Changelog — Assembling Smart CPS Training Lab

Documented lab overlays and operational fixes synced from the editorial workspace
into this publish repository. Dates are lab VM workdays (Europe/Rome).

---

## 2026-09-06 — Network-independent demo URLs + dual Tailscale

### WoT / WSTUN public URLs (`/lab-ws/<port>/`)
- Apache reverse proxy on Horizon `:80` maps `/lab-ws/50001/` … `/lab-ws/50100/` to
  the corresponding host `docker-proxy` ports (`host.docker.internal:<port>`).
- Horizon **Web Services (WoT)** panel builds Public URLs as
  `http://<HTTP_Host>/lab-ws/<public_port>/` so lukkinen Tailscale, gmerlino
  Tailscale, and LAN (`192.168.100.11`) share the **same path**.
- Files: `patches/apache-wot-ws-proxy.conf`, `patches/iotronic-ui-lab-entrypoint.sh`,
  `patches/docker-compose.lab.yml`, `patches/iotronic_ui_lab/.../iot_wot/wot_helpers.py`.

### Dual Tailscale on one VM (`lab-secondary`)
- Second `tailscaled` instance (systemd `tailscaled2`) for a second account/tailnet.
- State `/var/lib/tailscale2/`, socket `/run/tailscale2/tailscaled.sock`, TUN `tailscale1`, UDP `41642`.
- Helper: `/usr/local/bin/lab-secondary-ts` (not in git; recreate with unit file docs).
- Documented in `docs/LAB_NETWORK_ACCESS.md`.

---

## 2026-09-05 — SWC2026 ops, fleets, board logs, SSH-in-LR

### SWC2026 folder (`swc2026/`)
- Scripts to create/destroy manual Lightning-Rod boards without auto-register.
- Port model: LR UI always `:1474` **inside** container; host maps alpha `:1474` … zeta `:1479`, manuals `:1482+`.
- `01-run-manual-lr.sh` installs OpenSSH **inside** the container (no host SSH port publish)
  and sets `root` password (default `arancino`, override `ROOT_PASS`).

### Fleet create fix
- Upstream `openstack_dashboard.api.iotronic.fleet_create` omitted `return` →
  Create Fleet failed with `'NoneType' object has no attribute 'uuid'`.
- Entrypoint patches `return` on UI boot; CreateFleetForm recovers by name if needed.
- Delete fleet fails with FK if boards still reference the fleet — clear members first
  (or delete boards that still hold `fleet` UUID).

### Board log panel
- `lr-log-proxy` now prefers `/var/log/iotronic/lightning-rod.log` inside the container
  (where `LOG.info` / PluginCall land) instead of only `docker logs` stdout.

### Plugin IDE / Worker snippets
- Horizon plugin templates use `class Worker(Plugin.Plugin)` + `run()` (LR 0.4.17).
- Sync Call vs async Start/Stop documented in UI help.

### Conductor board delete
- Patch `except Exception` (was invalid `except exception`) for Create LR Container teardown.

### FL panel UX
- Select plugin no longer auto-runs the full scenario; use **Start server**.
- Partial client start → warning instead of hard fail when 0 clients.

---

## Earlier lab overlays (still current)

- Multi-board LR 2–6, FL mounts, metrics gateway, Grafana, fleets panel ops,
  Create Lab Board + LR provision via `lr-log-proxy`, English Horizon force,
  WoT/Metrics/FL live iframes.

See also: `docs/LAB_NETWORK_ACCESS.md`, `PORT_FORWARDING.md`, `swc2026/README.md`,
`GUIDA_SETUP_CORSISTI.md`.
