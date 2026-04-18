from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class GraphMetadata:
    dataset_name: str
    directed: bool
    node_count: int
    edge_count: int

    def to_json(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")


@dataclass(frozen=True)
class GraphDataset:
    metadata: GraphMetadata
    nodes: set[int]
    edges: set[tuple[int, int]]
