from __future__ import annotations


class JanusGraphAdapter:
    def __init__(self, client) -> None:
        self._client = client

    def _submit_scalar(self, query: str, bindings: dict[str, int]) -> int | None:
        rows = self._client.submit(query, bindings=bindings).all()
        if not rows:
            return None
        return rows[0]

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        query = (
            "g.V().has('user','id',node_id)"
            ".repeat(both('link')).times(hops)"
            ".dedup()"
            ".where(values('id').is(neq(node_id)))"
            ".count().next()"
        )
        return int(self._submit_scalar(query, {"node_id": node_id, "hops": hops}))

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        query = (
            "g.V().has('user','id',left_id).both('link').aggregate('left_neighbors')"
            ".V().has('user','id',right_id).both('link')"
            ".where(within('left_neighbors')).dedup().count().next()"
        )
        return int(self._submit_scalar(query, {"left_id": left_id, "right_id": right_id}))

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        query = (
            "g.V().has('user','id',left_id)"
            ".repeat(both('link').simplePath()).times(3)"
            ".emit()"
            ".has('id', right_id)"
            ".path().limit(1).count(local).next() - 1"
        )
        return self._submit_scalar(query, {"left_id": left_id, "right_id": right_id})
