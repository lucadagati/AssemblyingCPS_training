#!/usr/bin/env python3
"""Lab HTTP proxy: tail Lightning-Rod container logs for Horizon fleet panel."""
from __future__ import annotations

import os
import re
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

# Lab board name -> docker container (Module D + verify boards)
LR_CONTAINER_BY_BOARD = {
    "board-alpha": "lightning-rod",
    "board-beta": "lightning-rod-2",
    "board-gamma": "lightning-rod-3",
    "board-delta": "lightning-rod-4",
    "board-epsilon": "lightning-rod-5",
    "board-zeta": "lightning-rod-6",
}

DEFAULT_TAIL = int(os.environ.get("LR_LOG_TAIL", "40"))
MAX_TAIL = int(os.environ.get("LR_LOG_MAX_TAIL", "200"))
DOCKER_BIN = os.environ.get("DOCKER_BIN", "docker")


def _tail_container(container: str, tail: int, grep: str | None) -> list[str]:
    cmd = [DOCKER_BIN, "logs", "--tail", str(tail), container]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, timeout=30)
    except subprocess.CalledProcessError as exc:
        text = exc.output.decode("utf-8", "replace") if exc.output else str(exc)
        return ["[error] docker logs failed: {0}".format(text.strip())]
    except Exception as exc:
        return ["[error] {0}".format(exc)]
    lines = out.decode("utf-8", "replace").splitlines()
    if grep:
        pat = re.compile(grep, re.I)
        lines = [ln for ln in lines if pat.search(ln)]
    return lines[-tail:]


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True})


@app.route("/api/lr-logs", methods=["GET"])
def api_lr_logs():
    boards_raw = request.args.get("boards", "")
    board_names = [b.strip() for b in boards_raw.split(",") if b.strip()]
    tail = min(max(int(request.args.get("tail", DEFAULT_TAIL)), 1), MAX_TAIL)
    grep = request.args.get("grep") or None
    result = {}
    for name in board_names:
        container = LR_CONTAINER_BY_BOARD.get(name)
        if not container:
            result[name] = {
                "container": None,
                "lines": ["[warn] no LR container mapping for {0}".format(name)],
            }
            continue
        result[name] = {
            "container": container,
            "lines": _tail_container(container, tail, grep),
        }
    return jsonify({"boards": result, "tail": tail})


if __name__ == "__main__":
    host = os.environ.get("LR_LOG_PROXY_HOST", "0.0.0.0")
    port = int(os.environ.get("LR_LOG_PROXY_PORT", "8092"))
    app.run(host=host, port=port, threaded=True, use_reloader=False)
