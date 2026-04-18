from __future__ import annotations

from typing import Protocol


class GraphBackend(Protocol):
    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        """Return the unique reachable node count within a hop budget."""

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        """Return the direct common-neighbor count for two nodes."""

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        """Return the shortest path length up to 3 hops, or None if absent."""
