from __future__ import annotations

from collections import Counter, defaultdict

from graph_bench.models import GraphDataset


def hash_partition(dataset: GraphDataset, *, partition_count: int) -> dict[int, int]:
    return {node_id: node_id % partition_count for node_id in sorted(dataset.nodes)}


def locality_aware_partition(
    dataset: GraphDataset,
    *,
    partition_count: int,
) -> dict[int, int]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    degree: Counter[int] = Counter()
    for src, dst in dataset.edges:
        adjacency[src].add(dst)
        adjacency[dst].add(src)
        degree[src] += 1
        degree[dst] += 1

    seeds = [node_id for node_id, _ in degree.most_common(partition_count)]
    assignments: dict[int, int] = {seed: index for index, seed in enumerate(seeds)}
    frontier = list(seeds)

    while frontier:
        current = frontier.pop(0)
        current_partition = assignments[current]
        for neighbor in sorted(adjacency[current]):
            if neighbor in assignments:
                continue
            assignments[neighbor] = current_partition
            frontier.append(neighbor)

    unassigned = [node_id for node_id in sorted(dataset.nodes) if node_id not in assignments]
    for index, node_id in enumerate(unassigned):
        assignments[node_id] = index % partition_count

    return assignments


def edge_cut_ratio(dataset: GraphDataset, assignments: dict[int, int]) -> float:
    crossing = 0
    for src, dst in dataset.edges:
        if assignments[src] != assignments[dst]:
            crossing += 1
    return round(crossing / max(1, len(dataset.edges)), 4)
