#!/usr/bin/env python3
"""Capture authenticated Horizon / IoT / Plugin UI screenshots."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ASSETS = Path(__file__).resolve().parent.parent / "assets"
VM_IP_FILE = Path(__file__).resolve().parent.parent / "vm-ip.txt"


def lab_host() -> str:
    if (h := __import__("os").environ.get("S4T_LAB_HOST")):
        return h.strip()
    if VM_IP_FILE.is_file():
        return VM_IP_FILE.read_text().strip() or "127.0.0.1"
    return "127.0.0.1"


def main():
    host = lab_host()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        # Horizon login
        page.goto(f"http://{host}/horizon", wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(1500)
        # Try OpenStack login form
        for sel in ['input[name="username"]', '#id_username', 'input[type="text"]']:
            if page.locator(sel).count():
                page.fill(sel, "admin")
                break
        for sel in ['input[name="password"]', '#id_password', 'input[type="password"]']:
            if page.locator(sel).count():
                page.fill(sel, "s4t")
                break
        for sel in ['button[type="submit"]', 'input[type="submit"]', 'text=Sign In', 'text=Log in']:
            if page.locator(sel).count():
                page.locator(sel).first.click()
                break
        page.wait_for_timeout(4000)
        page.screenshot(path=str(ASSETS / "chapter13/horizon-after-login.png"), full_page=True)
        print("OK horizon-after-login")

        # IoT / boards — common Horizon paths
        for path, name in [
        ("/horizon/project/iotronic/boards/", "chapter13/horizon-boards-ui.png"),
            ("/horizon/iot/", "chapter13/horizon-boards-dashboard.png"),
            ("/horizon/iot/plugins/", "chapter14/plugin-list-live.png"),
            ("/horizon/iot/fleets/", "chapter14/fleets-live.png"),
        ]:
            try:
                page.goto(f"http://{host}{path}", wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(2000)
                out = ASSETS / name
                out.parent.mkdir(parents=True, exist_ok=True)
                page.screenshot(path=str(out), full_page=True)
                print(f"OK {name}")
            except Exception as e:
                print(f"SKIP {name}: {e}")

        # LR UI
        page.goto(f"http://{host}:1474/", wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(ASSETS / "chapter13/lr-ui-full.png"), full_page=True)
        print("OK lr-ui-full")

        browser.close()

if __name__ == "__main__":
    main()
