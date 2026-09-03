"""Shared FL visualization state (server + dashboard + edge plugins)."""
from __future__ import annotations

import json
import math
import threading
import time
from pathlib import Path
from typing import Any

STATE_PATH = Path("/tmp/fl_dashboard_state.json")
_lock = threading.Lock()

PHASES = (
    "idle",
    "waiting_clients",
    "broadcast",
    "local_training",
    "upload_weights",
    "aggregating",
    "evaluating",
    "round_complete",
    "finished",
)

BOARD_ALIASES = {
    "board-alpha": "board-alpha",
    "board-beta": "board-beta",
    "board-gamma": "board-gamma",
    "alpha": "board-alpha",
    "beta": "board-beta",
    "gamma": "board-gamma",
}


def _empty_state() -> dict[str, Any]:
    return {
        "phase": "idle",
        "round": 0,
        "total_rounds": int(__import__("os").environ.get("FL_ROUNDS", "2")),
        "accuracy": [],
        "loss": [],
        "clients": {
            "board-alpha": {"status": "offline", "samples": 0, "last_action": ""},
            "board-beta": {"status": "offline", "samples": 0, "last_action": ""},
            "board-gamma": {"status": "offline", "samples": 0, "last_action": ""},
        },
        "events": [],
        "updated_at": time.time(),
    }


def _load() -> dict[str, Any]:
    if STATE_PATH.is_file():
        try:
            return json.loads(STATE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return _empty_state()


def _json_safe(value: Any) -> Any:
    """Ensure state is serializable in browsers (no NaN/Infinity)."""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    return value


def _save(state: dict[str, Any]) -> None:
    state["updated_at"] = time.time()
    safe = _json_safe(state)
    STATE_PATH.write_text(json.dumps(safe, indent=0, allow_nan=False))


def reset(total_rounds: int | None = None) -> None:
    with _lock:
        state = _empty_state()
        if total_rounds is not None:
            state["total_rounds"] = total_rounds
        _save(state)


def _normalize_client(name: str) -> str:
    key = name.lower().strip()
    for token, canonical in BOARD_ALIASES.items():
        if token in key:
            return canonical
    return name


def _push_event(state: dict[str, Any], kind: str, message: str, **extra: Any) -> None:
    evt = {"t": time.time(), "kind": kind, "message": message, **extra}
    state["events"].append(evt)
    state["events"] = state["events"][-80:]


def emit(kind: str, message: str = "", **extra: Any) -> None:
    with _lock:
        state = _load()
        if extra.get("phase") in PHASES:
            state["phase"] = extra["phase"]
        if "round" in extra:
            state["round"] = extra["round"]
        client = extra.get("client")
        if client:
            cid = _normalize_client(str(client))
            if cid in state["clients"]:
                c = state["clients"][cid]
                if extra.get("client_status"):
                    c["status"] = extra["client_status"]
                if extra.get("samples") is not None:
                    c["samples"] = extra["samples"]
                if message:
                    c["last_action"] = message
        if kind == "metrics" and "accuracy" in extra:
            rnd = extra.get("round", state["round"])
            state["accuracy"].append({"round": rnd, "value": extra["accuracy"]})
            if "loss" in extra:
                loss_val = _json_safe(extra["loss"])
                if loss_val is not None:
                    state["loss"].append({"round": rnd, "value": loss_val})
        clean_extra = {k: _json_safe(v) for k, v in extra.items()}
        _push_event(state, kind, message or kind, **clean_extra)
        _save(state)


def snapshot() -> dict[str, Any]:
    with _lock:
        return _json_safe(_load())
