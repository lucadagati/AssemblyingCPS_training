# -*- coding: utf-8 -*-
"""WSTUN tunnel discovery for Horizon WoT panel (Python 2.7)."""

import logging
import os

LOG = logging.getLogger(__name__)


def lab_host(request):
    host = os.environ.get("S4T_LAB_HOST", "").strip()
    if host:
        return host.split(":")[0]
    http_host = request.META.get("HTTP_HOST", "")
    if http_host:
        return http_host.split(":")[0]
    return "127.0.0.1"


def public_url(host, public_port, path="/"):
    if not public_port:
        return ""
    path = path or "/"
    if not path.startswith("/"):
        path = "/" + path
    return "http://{0}:{1}{2}".format(host, int(public_port), path)


def collect_wot_tunnels(request, boards):
    """List WSTUN-exposed HTTP services (board local port -> cloud public port)."""
    host = lab_host(request)
    tunnels = []
    for board in boards:
        board_name = getattr(board, "name", "") or ""
        board_uuid = getattr(board, "uuid", "") or ""
        board_status = getattr(board, "status", "") or ""
        try:
            from openstack_dashboard.api import iotronic

            exposed = iotronic.services_on_board(request, board_uuid, True)
        except Exception as exc:
            LOG.warning("services_on_board failed for %s: %s", board_name, exc)
            continue

        if not exposed:
            continue

        for svc in exposed:
            public_port = int(svc.get("public_port") or 0)
            if public_port < 1:
                continue
            name = svc.get("name") or ""
            if name in ("webservice", "webservice_ssl"):
                continue
            local_port = svc.get("port") or ""
            tunnels.append(
                {
                    "board_name": board_name,
                    "board_uuid": board_uuid,
                    "board_status": board_status,
                    "service_name": name,
                    "protocol": svc.get("protocol") or "TCP",
                    "local_port": local_port,
                    "public_port": public_port,
                    "public_url": public_url(host, public_port, "/"),
                    "stream_key": "{0}|{1}|{2}".format(
                        board_uuid, name, public_port
                    ),
                }
            )

    tunnels.sort(key=_tunnel_sort_key)
    return host, tunnels


def _tunnel_sort_key(tunnel):
    """Demo apps first; connectivity-test entries last."""
    name = (tunnel.get("service_name") or "").lower()
    if "wot-fritzing" in name or name == "wot-fritzing":
        rank = 0
    elif "nginx-demo" in name or name == "lr-nginx-demo":
        rank = 9
    else:
        rank = 1
    return (
        rank,
        tunnel.get("board_name") or "",
        tunnel.get("service_name") or "",
    )
