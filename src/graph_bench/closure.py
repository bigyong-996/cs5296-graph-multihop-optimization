from __future__ import annotations

from collections import deque

from graph_bench.models import GraphDataset


def build_bounded_closure(
    dataset: GraphDataset,
    *,
    max_depth: int,
) -> set[tuple[int, int, int]]:
    adjacency: dict[int, set[int]] = {node_id: set() for node_id in dataset.nodes}
    for src, dst in dataset.edges:
        adjacency.setdefault(src, set()).add(dst)

    closure_rows: set[tuple[int, int, int]] = set()
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
                    if neighbor != source:
                        closure_rows.add((source, neighbor, next_depth))
    return closure_rows
