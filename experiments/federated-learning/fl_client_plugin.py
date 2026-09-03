# =============================================================================
# Federated Learning client plugin (Flower + PyTorch) - Stack4Things Ch.19 lab
# =============================================================================
#
# WHAT & WHY
# ---------
# This async Lightning-Rod plugin runs a Flower (flwr) edge client on a board.
# It trains a small neural network on LOCAL telemetry (predictive maintenance CSV),
# then sends weight updates to the central Flower server on the cloud VM. The server
# aggregates updates with FedAvg; no raw sensor data leaves the board.
#
# One plugin ("fl-client") is shared by ALL boards. Boards differ only through
# the JSON start parameters passed when the plugin is started (PluginStart).
#
# HOW TO USE (Horizon -> IoT -> Federated Learning)
# ------------------------------------------------
# 1. Create / update the cloud plugin once ("Create / update FL client plugin").
# 2. Map each online board to "fl-client" and inject the plugin on that board.
# 3. Set per-board Start parameters (JSON) - see below.
# 4. Start Flower server from the panel, then "Start all clients".
# 5. Watch live topology at the bottom of the FL panel.
#
# START PARAMETERS (JSON) - per-board differentiation
# ---------------------------------------------------
# Pass these keys in the JSON textarea when starting the plugin on each board:
#
#   server_address   Host:port of the Flower gRPC server (cloud VM).
#                    Example: "172.18.0.1:8087"
#   csv_file         Path to the LOCAL training CSV on this board (LR container).
#                    Example: "/opt/fl/machine_1.csv"
#   board_name       Label for live dashboard / logs (match IoTronic board name).
#                    Example: "board-alpha"
#   dashboard_url    HTTP URL of the FL live dashboard (for edge event posts).
#                    Example: "http://172.18.0.1:8090"
#
# CSV schema (predictive maintenance - one file per production line):
#   vibration_rms, vibration_peak, temperature_c, motor_current_a,
#   load_pct, hours_since_service, target (0=healthy, 1=failure imminent)
#
# Global lab settings (rounds, server host, dashboard host) are managed in
# "Lab parameters" in the Horizon panel; server_address and dashboard_url in
# the JSON are filled from those settings when you save or start clients.
#
# Example JSON for board-beta (conveyor motor / machine_2):
#
#   {
#     "board_name": "board-beta",
#     "csv_file": "/opt/fl/machine_2.csv",
#     "dashboard_url": "http://172.18.0.1:8090",
#     "server_address": "172.18.0.1:8087"
#   }
#
# Example JSON for board-gamma (pump line / machine_3):
#
#   {
#     "board_name": "board-gamma",
#     "csv_file": "/opt/fl/machine_3.csv",
#     "dashboard_url": "http://172.18.0.1:8090",
#     "server_address": "172.18.0.1:8087"
#   }
#
# REQUIREMENTS on the edge board (LR container)
# -------------------------------------------
# - Python packages: flwr, torch, pandas, scikit-learn
# - Dataset CSV mounted at csv_file path (install-fl-on-boards.sh for the lab)
#
# =============================================================================

"""Federated Learning Flower client for Lightning-Rod (async plugin)."""
from __future__ import annotations

import os
import threading
import urllib.error
import urllib.request
from collections import OrderedDict

import flwr as fl
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from iotronic_lightningrod.modules.plugins import Plugin
from oslo_log import log as logging
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, TensorDataset

LOG = logging.getLogger(__name__)


def _dashboard_post(url: str, payload: dict) -> None:
    if not url:
        return
    try:
        data = __import__("json").dumps(payload).encode()
        req = urllib.request.Request(
            url.rstrip("/") + "/api/client-event",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=2)
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        LOG.debug("Dashboard notify skipped: %s", exc)


class Net(nn.Module):
    def __init__(self, input_dim: int):
        super().__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)


def _get_weights(model):
    return [val.cpu().numpy() for _, val in model.state_dict().items()]


def _set_weights(model, parameters):
    keys = list(model.state_dict().keys())
    state_dict = OrderedDict({k: torch.tensor(v) for k, v in zip(keys, parameters)})
    model.load_state_dict(state_dict, strict=True)


def _load_data(csv_file: str):
    if not os.path.isfile(csv_file):
        raise FileNotFoundError(f"Dataset not found: {csv_file}")
    df = pd.read_csv(csv_file)
    if "target" not in df.columns:
        raise ValueError("CSV must contain a 'target' column")
    df = df.dropna()
    x = df.drop("target", axis=1).values.astype("float32")
    y = df["target"].values.astype("int64")
    x = StandardScaler().fit_transform(x)
    x = torch.tensor(x)
    y = torch.tensor(y)
    split = int(0.8 * len(x))
    return (x[:split], y[:split]), (x[split:], y[split:]), x.shape[1]


class MaintenanceClient(fl.client.NumPyClient):
    def __init__(self, csv_file: str, board_name: str = "board-alpha", dashboard_url: str = ""):
        (self.x_train, self.y_train), (self.x_test, self.y_test), input_dim = _load_data(csv_file)
        self.model = Net(input_dim)
        self.loss_fn = nn.CrossEntropyLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.board_name = board_name
        self.dashboard_url = dashboard_url

    def get_parameters(self, config):
        return _get_weights(self.model)

    def fit(self, parameters, config):
        rnd = config.get("round", "?")
        _dashboard_post(
            self.dashboard_url,
            {
                "kind": "local_train",
                "client": self.board_name,
                "message": f"{self.board_name}: local training (round {rnd})",
                "phase": "local_training",
                "client_status": "training",
                "round": rnd,
            },
        )
        _set_weights(self.model, parameters)
        self.model.train()
        loader = DataLoader(TensorDataset(self.x_train, self.y_train), batch_size=16, shuffle=True)
        for x_batch, y_batch in loader:
            self.optimizer.zero_grad()
            out = self.model(x_batch)
            loss = self.loss_fn(out, y_batch)
            loss.backward()
            self.optimizer.step()
        weights = _get_weights(self.model)
        _dashboard_post(
            self.dashboard_url,
            {
                "kind": "upload",
                "client": self.board_name,
                "message": f"{self.board_name}: uploading weight update",
                "phase": "upload_weights",
                "client_status": "uploaded",
                "samples": len(self.x_train),
                "round": rnd,
            },
        )
        return weights, len(self.x_train), {}

    def evaluate(self, parameters, config):
        _set_weights(self.model, parameters)
        self.model.eval()
        with torch.no_grad():
            out = self.model(self.x_test)
            loss = self.loss_fn(out, self.y_test).item()
            acc = (out.argmax(1) == self.y_test).float().mean().item()
        return loss, len(self.x_test), {"accuracy": acc}


class Worker(Plugin.Plugin):
    def __init__(self, uuid, name, q_result=None, params=None):
        super().__init__(uuid, name, q_result, params)
        self.server_address = (params or {}).get("server_address", "172.18.0.1:8087")
        self.csv_file = (params or {}).get("csv_file", "/opt/fl/machine_1.csv")
        self.board_name = (params or {}).get("board_name", "board-alpha")
        self.dashboard_url = (params or {}).get(
            "dashboard_url", os.environ.get("FL_DASHBOARD_URL", "http://172.18.0.1:8090")
        )
        self._thread = None

    def run(self):
        LOG.info(
            "FL plugin %s starting - server=%s csv=%s board=%s",
            self.name, self.server_address, self.csv_file, self.board_name,
        )
        _dashboard_post(
            self.dashboard_url,
            {
                "kind": "connect",
                "client": self.board_name,
                "message": f"{self.board_name}: connecting to Flower server",
                "client_status": "connected",
            },
        )

        def _client_main():
            try:
                fl.client.start_numpy_client(
                    server_address=self.server_address,
                    client=MaintenanceClient(self.csv_file, self.board_name, self.dashboard_url),
                )
            except Exception as exc:
                LOG.error("Flower client failed: %s", exc)
                if self.q_result is not None:
                    self.q_result.put(f"FL client error: {exc}")

        self._thread = threading.Thread(target=_client_main, daemon=True)
        self._thread.start()
