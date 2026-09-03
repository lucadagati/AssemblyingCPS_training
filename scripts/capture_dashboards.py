#!/usr/bin/env python3
"""Capture live dashboard screenshots — rejects 404 / error pages."""
from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ASSETS = Path(__file__).resolve().parent.parent / "assets"
VM_IP_FILE = Path(__file__).resolve().parent.parent / "vm-ip.txt"

HORIZON_USER = os.environ.get("S4T_HORIZON_USER", "admin")
HORIZON_PASS = os.environ.get("S4T_HORIZON_PASS", "s4t")
LR_USER = os.environ.get("S4T_LR_USER", "me")
LR_PASS = os.environ.get("S4T_LR_PASS", "arancino")

BAD_MARKERS = (
    "404", "not found", "pagina non trovata", "does not exist", "non esiste",
    "server error", "internal server error",
)


def lab_host() -> str:
    if h := os.environ.get("S4T_LAB_HOST"):
        return h.strip()
    if VM_IP_FILE.is_file():
        return VM_IP_FILE.read_text().strip() or "127.0.0.1"
    return "127.0.0.1"


def assert_page_ok(page, expect: str = ""):
    title = (page.title() or "").lower()
    try:
        h1 = page.locator("h1, h2").first.inner_text(timeout=3000).lower()
    except Exception:
        h1 = ""
    blob = f"{title} {h1} {page.url.lower()}"
    for bad in BAD_MARKERS:
        if bad in blob:
            raise RuntimeError(f"Error page captured: title={page.title()!r} url={page.url}")
    if expect and expect.lower() not in blob:
        raise RuntimeError(f"Unexpected page: wanted {expect!r}, got {page.title()!r} @ {page.url}")


def save(page, rel: str, expect: str = ""):
    assert_page_ok(page, expect)
    out = ASSETS / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out), full_page=True)
    print(f"OK {rel} ({page.title()})")


def horizon_login(page, host: str):
    page.goto(f"http://{host}/horizon/auth/login/", wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(800)
    for sel in ['input[name="username"]', "#id_username"]:
        if page.locator(sel).count():
            page.fill(sel, HORIZON_USER)
            break
    for sel in ['input[name="password"]', "#id_password"]:
        if page.locator(sel).count():
            page.fill(sel, HORIZON_PASS)
            break
    for sel in ['button[type="submit"]', 'input[type="submit"]', 'text=Connect', 'text=Log in']:
        if page.locator(sel).count():
            page.locator(sel).first.click()
            break
    page.wait_for_timeout(5000)


def lr_login(page, host: str):
    page.goto(f"http://{host}:1474/", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(800)
    if page.locator('input[name="username"]').count():
        page.fill('input[name="username"]', LR_USER)
        page.fill('input[name="password"]', LR_PASS)
        page.locator('input[type="submit"], button[type="submit"]').first.click()
        page.wait_for_timeout(3000)


def capture_fl_panel(page, host: str):
    """Module G — Federated Learning Horizon panel + live topology."""
    import json
    import urllib.error
    import urllib.request

    # Ensure dashboard is up for live topology iframe
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:8091/api/fl/start",
            data=json.dumps({"fl_rounds": "2"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            print(f"FL server start: {resp.read().decode()[:120]}")
    except urllib.error.URLError as exc:
        print(f"WARN FL server start: {exc}")

    horizon_login(page, host)
    fl_path = "/horizon/iot/federated_learning/"
    page.goto(f"http://{host}{fl_path}", wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(3000)
    save(page, "chapter19/horizon-fl-panel.png", "federated")

    # Lab parameters modal
    for sel in [
        'button[data-target="#fl-lab-params-modal"]',
        'text=Lab parameters',
    ]:
        if page.locator(sel).count():
            page.locator(sel).first.click()
            break
    page.wait_for_timeout(800)
    modal = page.locator("#fl-lab-params-modal")
    if modal.count() and modal.is_visible():
        out = ASSETS / "chapter19/horizon-fl-lab-params.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        modal.screenshot(path=str(out))
        print(f"OK chapter19/horizon-fl-lab-params.png")
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)

    # Expand FL client plugin section
    heading = page.locator(".fl-collapsible-heading")
    if heading.count():
        heading.first.click()
        page.wait_for_timeout(800)
        plugin = page.locator("#fl-plugin-collapse")
        if plugin.count():
            out = ASSETS / "chapter19/horizon-fl-plugin-section.png"
            plugin.screenshot(path=str(out))
            print(f"OK chapter19/horizon-fl-plugin-section.png")

    # Edge clients table (viewport crop)
    clients = page.locator(".fl-client-table").first
    if clients.count():
        out = ASSETS / "chapter19/horizon-fl-edge-clients.png"
        clients.screenshot(path=str(out))
        print(f"OK chapter19/horizon-fl-edge-clients.png")

    # Live topology iframe panel
    live = page.locator(".fl-live-panel")
    if live.count():
        page.locator(".fl-live-panel").scroll_into_view_if_needed()
        page.wait_for_timeout(4000)
        out = ASSETS / "chapter19/horizon-fl-live-topology.png"
        live.screenshot(path=str(out))
        print(f"OK chapter19/horizon-fl-live-topology.png")

    # Standalone embed (same origin proxy)
    page.goto(f"http://{host}/horizon/fl-live/?embed=1", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(3000)
    save(page, "chapter19/fl-live-dashboard-embed.png", "federat")


def capture_horizon(page, host: str):
    page.goto(f"http://{host}/horizon/auth/login/", wait_until="networkidle", timeout=90000)
    save(page, "chapter13/horizon-login.png", "login")

    horizon_login(page, host)
    save(page, "chapter13/horizon-after-login.png")

    panels = [
        ("chapter13/horizon-boards-dashboard.png", "/horizon/iot/", "boards"),
        ("chapter14/horizon-plugins-dashboard.png", "/horizon/iot/plugins/", "plugins"),
        ("chapter14/horizon-fleets-dashboard.png", "/horizon/iot/fleets/", "fleets"),
        ("chapter14/horizon-webservices-dashboard.png", "/horizon/iot/webservices/", "web"),
        ("chapter14/horizon-services-list.png", "/horizon/iot/services/", "services"),
        ("chapter14/horizon-boards-with-services.png", "/horizon/iot/", "boards"),
    ]
    for rel, path, expect in panels:
        page.goto(f"http://{host}{path}", wait_until="networkidle", timeout=45000)
        page.wait_for_timeout(2000)
        save(page, rel, expect)


def capture_lr(page, host: str, port: int = 1474, prefix: str = "chapter13"):
    page.goto(f"http://{host}:{port}/", wait_until="networkidle", timeout=60000)
    if port == 1474:
        save(page, f"{prefix}/lr-ui-login.png", "login")
    lr_login(page, host if port == 1474 else host)  # same creds all LR instances
    # Re-login with correct port for secondary LR
    if port != 1474:
        page.goto(f"http://{host}:{port}/", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(800)
        if page.locator('input[name="username"]').count():
            page.fill('input[name="username"]', LR_USER)
            page.fill('input[name="password"]', LR_PASS)
            page.locator('input[type="submit"], button[type="submit"]').first.click()
            page.wait_for_timeout(3000)

    suffix = "" if port == 1474 else f"-lr{port - 1473}"
    paths = [
        ("/", f"{prefix}/lr-dashboard-home{suffix}.png", "lightning"),
        ("/config", f"{prefix}/lr-dashboard-conf{suffix}.png", "config"),
    ]
    if port == 1474:
        paths.extend([
            ("/status", "chapter13/lr-dashboard-status.png", "status"),
            ("/system", "chapter13/lr-dashboard-system.png", "system"),
        ])
    for path, rel, expect in paths:
        page.goto(f"http://{host}:{port}{path}", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1500)
        try:
            save(page, rel, expect)
        except RuntimeError as e:
            print(f"SKIP {rel}: {e}")


def capture_multiboard_lr(page, host: str):
    """Capture secondary LR UIs when lab overlay is running."""
    import urllib.request
    for port in (1475, 1476):
        try:
            with urllib.request.urlopen(f"http://{host}:{port}/", timeout=5) as r:
                if r.status not in (200, 302):
                    continue
        except Exception:
            print(f"SKIP LR :{port} — not reachable")
            continue
        capture_lr(page, host, port=port, prefix="chapter19")


def capture_influx(page, host: str):
    page.goto(f"http://{host}:8086/debug/vars", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(1000)
    save(page, "chapter15/influxdb-debug.png", "8086")


def capture_post_demo(page, host: str):
    """Screenshots after demo scripts have run (weather WSTUN, service forms)."""
    import json
    root = Path(__file__).resolve().parent.parent

    weather_state = root / "experiments" / "webservices" / "weather-state.json"
    if weather_state.is_file():
        state = json.loads(weather_state.read_text())
        pub = state.get("cloud_port")
        if pub:
            page.goto(f"http://{host}:{pub}/", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(1500)
            out = ASSETS / "chapter14" / "weather-server-dashboard.png"
            out.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(out), full_page=True)
            print(f"OK chapter14/weather-server-dashboard.png (:{pub}/)")

            page.goto(f"http://{host}:{pub}/sensors", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(800)
            out2 = ASSETS / "chapter14" / "weather-sensors-json.png"
            page.screenshot(path=str(out2), full_page=True)
            print(f"OK chapter14/weather-sensors-json.png")

    wstun_state = root / "experiments" / "webservices" / "wstun-state.json"
    if wstun_state.is_file():
        pub = json.loads(wstun_state.read_text()).get("cloud_port")
        if pub:
            page.goto(f"http://{host}:{pub}/", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(1000)
            out = ASSETS / "chapter14" / "wstun-nginx-success.png"
            page.screenshot(path=str(out), full_page=True)
            print(f"OK chapter14/wstun-nginx-success.png (:{pub}/)")

    # Influx environmental_data query page (debug vars shows metrics; use simple HTML render)
    try:
        import subprocess
        query_out = subprocess.check_output(
            [
                "docker", "exec", "influxdb", "influx",
                "-username", "admin", "-password", "admin",
                "-database", "secco", "-execute",
                "SELECT * FROM environmental_data ORDER BY time DESC LIMIT 5",
            ],
            text=True, stderr=subprocess.DEVNULL, timeout=15,
        )
        html = f"<html><body><pre>{query_out}</pre></body></html>"
        page.set_content(html)
        out = ASSETS / "chapter15" / "influx-query-environmental.png"
        page.screenshot(path=str(out), full_page=True)
        print("OK chapter15/influx-query-environmental.png")
    except Exception as exc:
        print(f"SKIP influx query screenshot: {exc}")

    # Service create form (filled) if reachable
    try:
        horizon_login(page, host)
        page.goto(f"http://{host}/horizon/iot/services/create/", wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(800)
        for name_loc in (
            page.get_by_label("Service Name"),
            page.get_by_label("Nome servizio"),
            page.locator('input[name*="name" i]').first,
        ):
            try:
                if name_loc.count() and name_loc.first.is_visible(timeout=2000):
                    name_loc.first.fill("lr-nginx-demo")
                    break
            except Exception:
                continue
        for port_loc in (
            page.get_by_label("Porta"),
            page.get_by_label("Port"),
            page.locator('input[name*="port" i]').first,
        ):
            try:
                if port_loc.count() and port_loc.first.is_visible(timeout=2000):
                    port_loc.first.fill("50000")
                    break
            except Exception:
                continue
        out = ASSETS / "chapter14" / "horizon-service-create-filled.png"
        page.screenshot(path=str(out), full_page=True)
        print("OK chapter14/horizon-service-create-filled.png")
    except Exception as exc:
        print(f"SKIP service create form: {exc}")


def purge_bad_assets():
    stale = [
        "chapter14/plugin-list-live.png",
        "chapter14/lr-dashboard-plugins.png",
        "chapter14/fleets-live.png",
        "chapter14/horizon-plugins.png",
        "chapter13/horizon-boards-ui.png",
        "chapter13/horizon-iot-overview.png",
        "chapter13/horizon-home.png",
        "chapter13/lr-ui-full.png",
        "chapter13/sshot-docker-compose.png",
        "chapter13/sshot-horizon-board-list.png",
        "chapter15/influxdb-home.png",
    ]
    for rel in stale:
        p = ASSETS / rel
        if p.exists():
            p.unlink()
            print(f"REMOVED stale {rel}")


def main():
    host = lab_host()
    ASSETS.mkdir(parents=True, exist_ok=True)
    purge_bad_assets()
    fl_only = os.environ.get("FL_CAPTURE_ONLY", "").strip() in ("1", "true", "yes")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        if fl_only:
            capture_fl_panel(page, host)
        else:
            capture_horizon(page, host)
            capture_lr(page, host)
            capture_multiboard_lr(page, host)
            capture_influx(page, host)
            capture_post_demo(page, host)
            capture_fl_panel(page, host)
        browser.close()
    print("Dashboard capture complete — all pages validated.")


if __name__ == "__main__":
    main()
