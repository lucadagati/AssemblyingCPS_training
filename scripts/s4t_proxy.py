#!/usr/bin/env python3
"""
Reverse HTTP proxy for S4T lab services.
Exposes a single port so browser/tunnel can reach Horizon, LR, Conductor, InfluxDB.

Usage:
  python s4t_proxy.py [--port 9080]

Routes:
  /           -> http://127.0.0.1:80/          (Horizon)
  /lr/        -> http://127.0.0.1:1474/       (Lightning-Rod UI)
  /conductor/ -> http://127.0.0.1:8812/      (IoTronic API)
  /influx/    -> http://127.0.0.1:8086/      (InfluxDB)
"""
from __future__ import annotations

import argparse
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

ROUTES = [
    ("/lr/", "http://127.0.0.1:1474/"),
    ("/conductor/", "http://127.0.0.1:8812/"),
    ("/influx/", "http://127.0.0.1:8086/"),
    ("/", "http://127.0.0.1:80/"),
]


def pick_backend(path: str) -> tuple[str, str]:
    for prefix, base in ROUTES:
        if path.startswith(prefix):
            if prefix == "/":
                suffix = path
            else:
                suffix = path[len(prefix):]
            return base, suffix
    return "http://127.0.0.1:80/", path


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print(f"[proxy] {self.address_string()} {fmt % args}")

    def _proxy(self):
        base, suffix = pick_backend(self.path)
        target = base.rstrip("/") + "/" + suffix.lstrip("/") if suffix else base
        if "?" in self.path:
            target = target.split("?")[0] + "?" + self.path.split("?", 1)[1]

        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in ("host", "connection", "proxy-connection")}
        data = None
        if self.command in ("POST", "PUT", "PATCH"):
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length) if length else None

        req = urllib.request.Request(target, data=data, method=self.command, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = resp.read()
                self.send_response(resp.status)
                for k, v in resp.headers.items():
                    if k.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(k, v)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read()
            self.send_response(e.code)
            self.send_header("Content-Type", e.headers.get("Content-Type", "text/plain"))
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            msg = f"Proxy error: {e}".encode()
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def do_GET(self):
        self._proxy()

    def do_POST(self):
        self._proxy()

    def do_PUT(self):
        self._proxy()

    def do_HEAD(self):
        self._proxy()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=9080)
    p.add_argument("--bind", default="0.0.0.0")
    args = p.parse_args()
    server = HTTPServer((args.bind, args.port), ProxyHandler)
    print(f"S4T reverse proxy listening on http://{args.bind}:{args.port}")
    print("  /horizon via /  |  /lr/  |  /conductor/  |  /influx/")
    server.serve_forever()


if __name__ == "__main__":
    main()
