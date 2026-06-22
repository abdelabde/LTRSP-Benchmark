
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple, Union


PathLike = Union[str, Path]


def _parse_tuple_keys(d: Dict[str, int]) -> Dict[Tuple[str, str], int]:
    """Convert ``{"M3|P1": 120, ...}`` back to ``{("M3", "P1"): 120, ...}``."""
    out: Dict[Tuple[str, str], int] = {}
    for k, v in d.items():
        parts = k.split("|")
        if len(parts) != 2:
            raise ValueError(
                f"Malformed tuple key {k!r}: expected 'X|Y' (two parts), "
                f"got {len(parts)}."
            )
        out[(parts[0], parts[1])] = int(v)
    return out


def load_instance(path: PathLike) -> dict:
    
    with open(path, "r", encoding="utf-8") as f:
        inst = json.load(f)

    # Sanity-check mandatory top-level keys.
    required = {
        "metadata", "sets", "cardinalities",
        "vehicles_info", "home_bases_info", "mills_info",
        "demand_d_mp", "supply_s_fp",
        "distance_matrices", "time_matrices",
    }
    missing = required - inst.keys()
    if missing:
        raise ValueError(
            f"Instance file {path} is missing required field(s): "
            f"{sorted(missing)}"
        )

    inst["demand_d_mp"] = _parse_tuple_keys(inst["demand_d_mp"])
    inst["supply_s_fp"] = _parse_tuple_keys(inst["supply_s_fp"])
    return inst


def summarize_instance(inst: dict) -> None:
    """Print a short summary of an instance to stdout."""
    meta = inst["metadata"]
    card = inst["cardinalities"]
    total_demand = sum(inst["demand_d_mp"].values())
    total_supply = sum(inst["supply_s_fp"].values())

    print(f"Instance  : {meta['instance_id']}")
    print(f"Week      : {meta['week_dates']}")
    print(f"Mills     : {card['num_mills']}")
    print(f"Forests   : {card['num_forests']}")
    print(f"Products  : {card['num_products']}")
    print(f"Vehicles  : {card['num_vehicles']}")
    print(f"Homebases : {card['num_home_bases']}")
    print(f"Total demand : {total_demand} GMT")
    print(f"Total supply : {total_supply} GMT")

    sl = sum(1 for v in inst["vehicles_info"] if v["self_loading"])
    print(f"Self-loading trucks : {sl} / {card['num_vehicles']}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python load_instance.py <path-to-instance.json>")
        sys.exit(1)

    inst = load_instance(sys.argv[1])
    summarize_instance(inst)