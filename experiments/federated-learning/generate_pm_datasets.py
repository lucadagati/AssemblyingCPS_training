#!/usr/bin/env python3
"""Generate synthetic predictive-maintenance CSVs for Module G FL lab.

Each edge board monitors a different production line (non-IID telemetry):
  machine_1.csv -> board-alpha  (CNC spindle — vibration-driven failures)
  machine_2.csv -> board-beta   (conveyor motor — temperature-driven)
  machine_3.csv -> board-gamma  (pump line — current + vibration)

Columns: vibration_rms, vibration_peak, temperature_c, motor_current_a,
         load_pct, hours_since_service, target (0=healthy, 1=failure imminent)
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES = [
    "vibration_rms",
    "vibration_peak",
    "temperature_c",
    "motor_current_a",
    "load_pct",
    "hours_since_service",
]

PROFILES = {
    1: {
        "name": "CNC spindle (board-alpha)",
        "seed": 19,
        "n": 120,
        "healthy": dict(vibration_rms=(1.2, 0.25), vibration_peak=(2.5, 0.4),
                        temperature_c=(45, 4), motor_current_a=(8.5, 0.8),
                        load_pct=(55, 10), hours_since_service=(120, 40)),
        "failure": dict(vibration_rms=(4.8, 0.6), vibration_peak=(9.5, 1.0),
                        temperature_c=(62, 5), motor_current_a=(11.0, 1.0),
                        load_pct=(78, 8), hours_since_service=(480, 60)),
    },
    2: {
        "name": "Conveyor motor (board-beta)",
        "seed": 29,
        "n": 120,
        "healthy": dict(vibration_rms=(0.9, 0.2), vibration_peak=(1.8, 0.3),
                        temperature_c=(38, 3), motor_current_a=(5.5, 0.5),
                        load_pct=(40, 8), hours_since_service=(200, 50)),
        "failure": dict(vibration_rms=(2.2, 0.4), vibration_peak=(4.5, 0.6),
                        temperature_c=(78, 6), motor_current_a=(7.8, 0.7),
                        load_pct=(65, 10), hours_since_service=(600, 80)),
    },
    3: {
        "name": "Pump line (board-gamma)",
        "seed": 37,
        "n": 120,
        "healthy": dict(vibration_rms=(1.0, 0.18), vibration_peak=(2.0, 0.35),
                        temperature_c=(42, 3.5), motor_current_a=(6.2, 0.6),
                        load_pct=(50, 9), hours_since_service=(150, 45)),
        "failure": dict(vibration_rms=(3.5, 0.5), vibration_peak=(7.0, 0.8),
                        temperature_c=(58, 4), motor_current_a=(10.5, 0.9),
                        load_pct=(82, 7), hours_since_service=(520, 70)),
    },
}


def _sample(rng: np.random.Generator, spec: dict, n: int) -> pd.DataFrame:
    rows = {}
    for col in FEATURES:
        mu, sigma = spec[col]
        rows[col] = rng.normal(mu, sigma, n).clip(0.01, None)
    return pd.DataFrame(rows)


def generate_machine(machine_id: int) -> pd.DataFrame:
    profile = PROFILES[machine_id]
    rng = np.random.default_rng(profile["seed"])
    n = profile["n"]
    n_fail = max(18, n // 4)
    n_ok = n - n_fail
    healthy = _sample(rng, profile["healthy"], n_ok)
    failing = _sample(rng, profile["failure"], n_fail)
    df = pd.concat([healthy, failing], ignore_index=True)
    df["target"] = [0] * n_ok + [1] * n_fail
    df = df.sample(frac=1, random_state=profile["seed"]).reset_index(drop=True)
    return df[FEATURES + ["target"]]


def generate_test(rng_seed: int = 99) -> pd.DataFrame:
    """Held-out mix from all lines for server-side evaluation."""
    rng = np.random.default_rng(rng_seed)
    parts = []
    for mid in (1, 2, 3):
        profile = PROFILES[mid]
        n = 40
        n_fail = 10
        healthy = _sample(rng, profile["healthy"], n - n_fail)
        failing = _sample(rng, profile["failure"], n_fail)
        part = pd.concat([healthy, failing], ignore_index=True)
        part["target"] = [0] * (n - n_fail) + [1] * n_fail
        parts.append(part)
    df = pd.concat(parts, ignore_index=True)
    return df.sample(frac=1, random_state=rng_seed).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "repos" / "ch19",
    )
    args = parser.parse_args()
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    for mid, profile in PROFILES.items():
        path = out / f"machine_{mid}.csv"
        df = generate_machine(mid)
        df.to_csv(path, index=False)
        fail_rate = df["target"].mean()
        print(f"Wrote {path} ({len(df)} rows, failure rate {fail_rate:.1%}) — {profile['name']}")

    test_path = out / "data_test.csv"
    test_df = generate_test()
    test_df.to_csv(test_path, index=False)
    print(f"Wrote {test_path} ({len(test_df)} rows, failure rate {test_df['target'].mean():.1%})")


if __name__ == "__main__":
    main()
