"""Parametric placeholders for lab-specific values — never hardcode VM IP in deck text."""
from __future__ import annotations

import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# Tokens used in all deck source files (hand-authored slide text).
TOKEN_VM_IP = "{{VM_IP}}"
TOKEN_HZ_CRED = "{{HZ_CRED}}"
TOKEN_LR_CRED = "{{LR_CRED}}"

DEFAULTS = {
    TOKEN_VM_IP: TOKEN_VM_IP,  # keep token visible in PPTX if unset
    TOKEN_HZ_CRED: "admin / s4t",
    TOKEN_LR_CRED: "me / arancino",
}


def lab_context(*, resolve_ip: bool | None = None) -> dict[str, str]:
    """Build placeholder map for deck substitution.

    By default slides keep ``{{VM_IP}}`` so each student replaces it with their
    own host IP. Set env ``S4T_RESOLVE_VM_IP=1`` (or pass ``resolve_ip=True``)
    to bake in ``S4T_LAB_HOST`` / ``vm-ip.txt`` for instructor-only builds.
    """
    if resolve_ip is None:
        resolve_ip = os.environ.get("S4T_RESOLVE_VM_IP", "").strip() in ("1", "true", "yes")

    ip = TOKEN_VM_IP
    if resolve_ip:
        ip = os.environ.get("S4T_LAB_HOST", "").strip()
        if not ip:
            ip_file = BASE / "vm-ip.txt"
            if ip_file.is_file():
                ip = ip_file.read_text().strip()
        if not ip:
            ip = TOKEN_VM_IP

    return {
        TOKEN_VM_IP: ip,
        TOKEN_HZ_CRED: os.environ.get("S4T_HORIZON_CRED", DEFAULTS[TOKEN_HZ_CRED]),
        TOKEN_LR_CRED: os.environ.get("S4T_LR_CRED", DEFAULTS[TOKEN_LR_CRED]),
    }


def substitute(value, ctx: dict[str, str]):
    if isinstance(value, str):
        for k, v in ctx.items():
            value = value.replace(k, v)
        return value
    if isinstance(value, (list, tuple)):
        return type(value)(substitute(v, ctx) for v in value)
    return value


def substitute_deck(items: list, ctx: dict[str, str] | None = None) -> list:
    ctx = ctx or lab_context()
    return [substitute(item, ctx) for item in items]
