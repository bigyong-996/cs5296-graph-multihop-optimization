from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import random


@dataclass(frozen=True)
class WorkloadCase:
    query_type: str
    node_id: int | None = None
    left_id: int | None = None
    right_id: int | None = None
    hops: int = 1


def generate_workloads(nodes: list[int], *, per_type: int) -> list[WorkloadCase]:
    rng = random.Random(5296)
    ordered = sorted(nodes)
    pairs = list(zip(ordered[::2], ordered[1::2]))
    workloads: list[WorkloadCase] = []

    for hops in (1, 2, 3):
        for node_id in rng.sample(ordered, k=min(per_type, len(ordered))):
            workloads.append(WorkloadCase(query_type="neighbors", node_id=node_id, hops=hops))

    for left_id, right_id in pairs[:per_type]:
        workloads.append(
            WorkloadCase(query_type="common_neighbors", left_id=left_id, right_id=right_id)
        )
        workloads.append(
            WorkloadCase(query_type="shortest_path", left_id=left_id, right_id=right_id, hops=3)
        )

    return workloads


def write_workloads(workloads: list[WorkloadCase], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps([asdict(workload) for workload in workloads], indent=2),
        encoding="utf-8",
    )
