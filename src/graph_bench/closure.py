from __future__ import annotations

from collections import deque
import csv
from pathlib import Path

from graph_bench.models import GraphDataset


def build_bounded_closure(
    dataset: GraphDataset,
    *,
    max_depth: int,
) -> set[tuple[int, int, int]]:
    return set(iter_bounded_closure_rows(dataset, max_depth=max_depth))


def write_bounded_closure_csv(
    dataset: GraphDataset,
    *,
    max_depth: int,
    output_path: Path,
) -> None:
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["src", "dst", "depth"])
        for src, dst, depth in iter_bounded_closure_rows(dataset, max_depth=max_depth):
            writer.writerow([src, dst, depth])


def iter_bounded_closure_rows(
    dataset: GraphDataset,
    *,
    max_depth: int,
):
    adjacency: dict[int, set[int]] = {node_id: set() for node_id in dataset.nodes}
    for src, dst in dataset.edges:
        adjacency.setdefault(src, set()).add(dst)

    for source in sorted(dataset.nodes):
        queue = deque([(source, 0)])
        seen_depth: dict[int, int] = {source: 0}
        while queue:
            current, depth = queue.popleft()
            if depth == max_depth:
                continue
            for neighbor in sorted(adjacency.get(current, set())):
                next_depth = depth + 1
                if neighbor not in seen_depth or next_depth < seen_depth[neighbor]:
                    seen_depth[neighbor] = next_depth
                    queue.append((neighbor, next_depth))
        for target, depth in sorted(seen_depth.items()):
            if target != source:
                yield (source, target, depth)
