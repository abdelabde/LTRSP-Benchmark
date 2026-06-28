# LTRSP Benchmark Instances

Anonymized and scaled weekly instances (demand, supply, and vehicles capacity are scaled) for the **Log-Truck Routing and Scheduling Problem
(LTRSP)**.

This repository supports the paper:

> Abdellaoui, A., Benabbou, L., El Hallaoui, I., Aubé, F., Amazouz, M.
> *Real-World, Large-Scale, Multi-Period Log Truck Routing and Scheduling:
> Application to Canadian Forestry.*
> International Journal of Production Research (under revision).

To our knowledge, no public benchmark previously existed for this problem at
real industrial scale: prior exact and matheuristic formulations were validated
only on small synthetic instances. We release this dataset to enable
reproducible comparison of future methods.

---

## Contents
ltrsp-benchmark/

├── README.md                  ← this file

├── load_instance.py           ← reference Python loader

└── instances/

    ├── W01.json

    ├── W02.json

    ├── …

    └── W20.json

Each `instances/W##.json` file is **self-contained**: it carries all the data
needed to rebuild the routing network and solve the LTRSP on that week.

---

## Anonymization

All physical identifiers are replaced by sequential anonymized labels:

| Real identifier             | Anonymized label |
|-----------------------------|------------------|
| Mill code                   | `M1, M2, …`      |
| Forest block ID             | `F1, F2, …`      |
| Truck ID                    | `V1, V2, …`      |
| Contractor / home base name | `HB1, HB2, …`    |
| Product code                | `P1, P2, …`      |

GPS coordinates are **not** released. Only the **distance and travel-time
matrices** (computed from the original network with the operationally
observed speeds) are included, which is sufficient to reproduce the
routing-network construction and all the experimental results of the paper
without exposing the underlying geography.

---

## Quick start (Python)

```python
from load_instance import load_instance

inst = load_instance("instances/W05.json")

print(inst["metadata"]["instance_id"])         # → 'W05'
print(inst["cardinalities"])                   # → counts of F, M, P, V, HB

M = inst["sets"]["mills"]
P = inst["sets"]["products"]
print(f"Demand at {M[0]} for {P[0]}:",
      inst["demand_d_mp"].get((M[0], P[0]), 0))

# Travel time from forest F[i] to mill M[j], in minutes
F = inst["sets"]["forests"]
i, j = 0, 0
print(f"Time from {F[i]} to {M[j]}:",
      inst["time_matrices"]["forest_to_mill_min"][i][j], "min")
```

See `load_instance.py` for a fully documented reference loader.

---

## What's in a JSON file

Each instance file carries the following fields:

- **metadata** — instance ID, planning week, units.
- **sets** — anonymized lists `F, M, P, V, HB`.
- **cardinalities** — convenience counts.
- **vehicles_info** — per truck: capacity (GMT), self-loading flag.
- **home_bases_info** — which trucks belong to each home base.
- **mills_info** — daily opening and closing time of each mill (HH:MM, 24-hour).
- **demand_d_mp** — weekly demand `(mill, product) → GMT`.
- **supply_s_fp** — weekly supply `(forest, product) → GMT`.
- **distance_matrices** — 4 matrices (km) for all relevant origin–destination pairs.
- **time_matrices** — 4 matrices (min) corresponding to the distance matrices,
  computed with the operationally observed seasonal speeds.

All matrices follow the order of the `sets` lists. For example,
`forest_to_mill_km[i][j]` is the distance from `F[i]` to `M[j]`.

## Citation

If you use these instances, please cite the paper:

```bibtex
@article{Abdellaoui2026LTRSP,
  author  = {Abdellaoui, Abdelhakim and Benabbou, Loubna and El Hallaoui, Issmail
             and Aub{\'e}, Fran{\c{c}}ois and Amazouz, Mouloud},
  title   = {Real-World, Large-Scale, Multi-Period Log Truck Routing and Scheduling:
             Application to Canadian Forestry},
  journal = {International Journal of Production Research},
  year    = {2026},
  note    = {Under revision}
}
```

---

## Contact

For questions about the data or the paper:
**Abdelhakim Abdellaoui** — abdelhakim.abdellaoui@polymtl.ca
Polytechnique Montréal / GERAD / CanmetENERGY-Varennes (NRCan)
