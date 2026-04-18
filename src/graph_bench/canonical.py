from __future__ import annotations

from collections import Counter
import csv
from pathlib import Path

from graph_bench.models import GraphDataset, GraphMetadata


def read_edge_list(
    path: Path,
    *,
    dataset_name: str,
    directed: bool,
    symmetrize: bool,
) -> GraphDataset:
    nodes: set[int] = set()
    edges: set[tuple[int, int]] = set()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        left_text, right_text = line.split()
        left = int(left_text)
        right = int(right_text)
        nodes.update({left, right})
        edges.add((left, right))
        if symmetrize and left != right:
            edges.add((right, left))

    metadata = GraphMetadata(
        dataset_name=dataset_name,
        directed=directed and not symmetrize,
        node_count=len(nodes),
        edge_count=len(edges),
    )
    return GraphDataset(metadata=metadata, nodes=nodes, edges=edges)


def top_degree_subgraph(
    dataset: GraphDataset,
    *,
    max_nodes: int,
    sampled_name: str,
) -> GraphDataset:
    degrees: Counter[int] = Counter()
    for left, right in dataset.edges:
        degrees[left] += 1
        degrees[right] += 1

    chosen_nodes = {
        node_id
        for node_id, _ in sorted(
            degrees.items(),
            key=lambda item: (-item[1], item[0]),
        )[:max_nodes]
    }
    sampled_edges = {
        (left, right)
        for left, right in dataset.edges
        if left in chosen_nodes and right in chosen_nodes
    }
    metadata = GraphMetadata(
        dataset_name=sampled_name,
        directed=dataset.metadata.directed,
        node_count=len(chosen_nodes),
        edge_count=len(sampled_edges),
    )
    return GraphDataset(metadata=metadata, nodes=chosen_nodes, edges=sampled_edges)


def write_canonical_dataset(dataset: GraphDataset, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "nodes.csv").open("w", encoding="utf-8", newline="") as node_file:
        writer = csv.writer(node_file)
        writer.writerow(["node_id"])
        for node_id in sorted(dataset.nodes):
            writer.writerow([node_id])

    with (output_dir / "edges.csv").open("w", encoding="utf-8", newline="") as edge_file:
        writer = csv.writer(edge_file)
        writer.writerow(["src", "dst"])
        for src, dst in sorted(dataset.edges):
            writer.writerow([src, dst])

    dataset.metadata.to_json(output_dir / "metadata.json")
