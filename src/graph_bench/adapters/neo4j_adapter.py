from __future__ import annotations


class Neo4jAdapter:
    def __init__(self, driver) -> None:
        self._driver = driver

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        if hops not in {1, 2, 3}:
            raise ValueError("hops must be 1, 2, or 3")
        query = (
            f"MATCH (:User {{id: $node_id}})-[:LINK*1..{hops}]-(target:User) "
            "WHERE target.id <> $node_id "
            "RETURN count(DISTINCT target) AS value"
        )
        with self._driver.session() as session:
            return int(session.run(query, node_id=node_id).single()["value"])

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        query = (
            "MATCH (:User {id: $left_id})-[:LINK]-(common:User)-[:LINK]-(:User {id: $right_id}) "
            "WHERE common.id <> $left_id AND common.id <> $right_id "
            "RETURN count(DISTINCT common) AS value"
        )
        with self._driver.session() as session:
            return int(session.run(query, left_id=left_id, right_id=right_id).single()["value"])

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        query = (
            "MATCH (left:User {id: $left_id}), (right:User {id: $right_id}) "
            "OPTIONAL MATCH p = shortestPath((left)-[:LINK*..3]-(right)) "
            "RETURN CASE WHEN p IS NULL THEN NULL ELSE length(p) END AS value"
        )
        with self._driver.session() as session:
            return session.run(query, left_id=left_id, right_id=right_id).single()["value"]
