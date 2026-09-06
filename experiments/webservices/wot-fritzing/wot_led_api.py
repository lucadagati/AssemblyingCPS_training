#!/usr/bin/env python3
"""WoT LED API backend for Fritzing demo (Python 3)."""

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

LED_STATE = {"on": False, "pin": 18, "updated_at": time.time()}


class WoTLEDHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/api/led/status", "/led/status"):
            self._json(200, {
                "state": "on" if LED_STATE["on"] else "off",
                "pin": LED_STATE["pin"],
                "updated_at": LED_STATE["updated_at"],
            })
        elif path == "/api/thing":
            self._json(200, {
                "title": "WoT Fritzing LED Thing",
                "actions": [
                    {"method": "POST", "href": "/led/toggle", "name": "toggle"},
                    {"method": "POST", "href": "/led/on", "name": "on"},
                    {"method": "POST", "href": "/led/off", "name": "off"},
                ],
                "properties": [
                    {"method": "GET", "href": "/api/led/status", "name": "led"},
                ],
            })
        else:
            self.send_error(404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/led/toggle":
            LED_STATE["on"] = not LED_STATE["on"]
        elif path == "/led/on":
            LED_STATE["on"] = True
        elif path == "/led/off":
            LED_STATE["on"] = False
        else:
            self.send_error(404)
            return
        LED_STATE["updated_at"] = time.time()
        self._json(200, {
            "state": "on" if LED_STATE["on"] else "off",
            "pin": LED_STATE["pin"],
            "updated_at": LED_STATE["updated_at"],
        })


def main():
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8091
    server = HTTPServer(("127.0.0.1", port), WoTLEDHandler)
    print("WoT LED API on 127.0.0.1:%d" % port)
    server.serve_forever()


if __name__ == "__main__":
    main()
