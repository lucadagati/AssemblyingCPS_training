#!/usr/bin/env python3
"""Create 3 boards via API and configure Lightning-Rod instances (1474/1475/1476)."""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
VM_IP_FILE = ROOT / "vm-ip.txt"
HOST = os.environ.get("S4T_LAB_HOST", VM_IP_FILE.read_text().strip() if VM_IP_FILE.is_file() else "127.0.0.1")
LR_USER = os.environ.get("S4T_LR_USER", "me")
LR_PASS = os.environ.get("S4T_LR_PASS", "arancino")
WAMP_URL = "wss://crossbar:8181"

BOARDS = [
    ("board-alpha", "board-alpha-lab2026", 1474),
    ("board-beta", "board-beta-lab2026", 1475),
    ("board-gamma", "board-gamma-lab2026", 1476),
]


def keystone_token() -> str:
    body = json.dumps({
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": "admin",
                        "domain": {"name": "Default"},
                        "password": "s4t",
                    }
                },
            },
            "scope": {
                "project": {"name": "admin", "domain": {"name": "Default"}},
            },
        }
    }).encode()
    req = urllib.request.Request(
        f"http://{HOST}:5000/v3/auth/tokens",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        token = resp.headers.get("X-Subject-Token")
        if not token:
            raise RuntimeError("No X-Subject-Token from Keystone")
        return token


def ensure_board(token: str, name: str, code: str) -> dict:
    headers = {"Content-Type": "application/json", "X-Auth-Token": token}
    list_req = urllib.request.Request(f"http://{HOST}:8812/v1/boards/", headers=headers)
    try:
        with urllib.request.urlopen(list_req, timeout=15) as resp:
            boards = json.loads(resp.read().decode())
    except Exception:
        boards = []
    if isinstance(boards, dict):
        boards = boards.get("boards", boards.get("items", []))
    for b in boards:
        if b.get("name") == name or b.get("code") == code:
            print(f"EXISTS {name} uuid={b.get('uuid')} status={b.get('status')}")
            return b
    payload = json.dumps({
        "name": name,
        "code": code,
        "type": "virtual",
        "location": [{"latitude": "38.19", "longitude": "15.55", "altitude": "0"}],
    }).encode()
    req = urllib.request.Request(
        f"http://{HOST}:8812/v1/boards/",
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            board = json.loads(resp.read().decode())
            print(f"CREATED {name} uuid={board.get('uuid')}")
            return board
    except urllib.error.HTTPError as e:
        if e.code == 409:
            try:
                with urllib.request.urlopen(list_req, timeout=15) as resp:
                    boards = json.loads(resp.read().decode())
                if isinstance(boards, dict):
                    boards = boards.get("boards", boards.get("items", []))
                for b in boards:
                    if b.get("name") == name or b.get("code") == code:
                        print(f"EXISTS (409) {name} uuid={b.get('uuid')}")
                        return b
            except Exception as exc:
                print(f"WARN list boards after 409: {exc} — using code {code} for LR config")
                return {"name": name, "code": code, "uuid": "unknown"}
        raise


def configure_lr(page, port: int, code: str) -> bool:
    page.goto(f"http://{HOST}:{port}/", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(500)
    if page.locator('input[name="username"]').count():
        page.fill('input[name="username"]', LR_USER)
        page.fill('input[name="password"]', LR_PASS)
        page.locator('input[type="submit"], button[type="submit"]').first.click()
        page.wait_for_timeout(2000)
    page.goto(f"http://{HOST}:{port}/config", wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(500)
    # Skip if already configured (not first_boot)
    if page.locator("text=first_boot").count() == 0 and page.locator("text=Not connected").count() == 0:
        print(f"  LR :{port} may already be configured")
    for sel in ['input[placeholder*="WAGENT"]', 'input[name*="url"]', 'input[type="text"]']:
        loc = page.locator(sel)
        if loc.count():
            loc.first.fill(WAMP_URL)
            break
    else:
        page.get_by_label("Registration Agent URL:").fill(WAMP_URL)
    page.get_by_label("Registration Code:").fill(code)
    page.locator('input[value="CONFIGURE"], button:has-text("CONFIGURE")').first.click()
    page.wait_for_timeout(8000)
    page.goto(f"http://{HOST}:{port}/status", wait_until="networkidle", timeout=30000)
    text = page.content().lower()
    ok = "connected" in text and "not connected" not in text
    print(f"  LR :{port} status page — connected={'yes' if ok else 'pending'}")
    return ok


def wait_crossbar(timeout: int = 120) -> None:
    import socket
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            s = socket.create_connection((HOST, 8181), timeout=3)
            s.close()
            print("OK Crossbar :8181 reachable from host")
            return
        except OSError:
            time.sleep(3)
    print("WARN Crossbar :8181 not reachable — LR may stay offline")


def main() -> int:
    print(f"=== Onboard multiboard on {HOST} ===")
    wait_crossbar()
    token = keystone_token()
    boards = [ensure_board(token, n, c) for n, c, _ in BOARDS]
    ok_count = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        for (_, code, port), board in zip(BOARDS, boards):
            print(f"Configure {code} on LR :{port}")
            if configure_lr(page, port, code):
                ok_count += 1
        browser.close()
    print(f"Done — {ok_count}/{len(BOARDS)} LR instances report connected")
    return 0 if ok_count >= 1 else 1


if __name__ == "__main__":
    sys.exit(main())
