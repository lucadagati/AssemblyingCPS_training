#!/usr/bin/env python3
"""Capture live UI screenshots from S4T stack (localhost on VM)."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ASSETS = Path(__file__).resolve().parent.parent / "assets"
VM_IP_FILE = ASSETS.parent / "vm-ip.txt"


def lab_host() -> str:
    import os
    if h := os.environ.get("S4T_LAB_HOST"):
        return h.strip()
    if VM_IP_FILE.is_file():
        return VM_IP_FILE.read_text().strip() or "127.0.0.1"
    return "127.0.0.1"


def shots(host: str):
    return [
        ("chapter13/horizon-login.png", f"http://{host}/horizon", 1280, 800),
        ("chapter13/horizon-home.png", f"http://{host}/", 1280, 800),
        ("chapter13/lr-ui-login.png", f"http://{host}:1474/", 1280, 800),
        ("chapter14/horizon-plugins.png", f"http://{host}/horizon", 1280, 800),
    ]

def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for rel, url, w, h in shots(lab_host()):
            out = ASSETS / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                page = browser.new_page(viewport={"width": w, "height": h})
                page.goto(url, wait_until="networkidle", timeout=60000)
                page.wait_for_timeout(2000)
                page.screenshot(path=str(out), full_page=True)
                print(f"OK {out}")
            except Exception as e:
                print(f"SKIP {rel}: {e}")
            finally:
                page.close()
        browser.close()

if __name__ == "__main__":
    main()
