from __future__ import annotations


class Neo4jAdapter:
    def __init__(self, driver) -> None:
        self._driver = driver

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        if hops not in {1, 2, 3}:
            raise ValueError("hops must be 1, 2, or 3")
        query = _neighbor_count_query(hops)
        with self._driver.session() as session:
            return int(session.run(query, node_id=node_id).single()["value"])

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        query = (
            "MATCH (:User {id: $left_id})-[:LINK]->(common:User)<-[:LINK]-(:User {id: $right_id}) "
            "WHERE common.id <> $left_id AND common.id <> $right_id "
            "RETURN count(DISTINCT common) AS value"
        )
        with self._driver.session() as session:
            return int(session.run(query, left_id=left_id, right_id=right_id).single()["value"])

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        query = (
            "MATCH (left:User {id: $left_id}), (right:User {id: $right_id}) "
            "OPTIONAL MATCH p = shortestPath((left)-[:LINK*..3]->(right)) "
            "RETURN CASE WHEN p IS NULL THEN NULL ELSE length(p) END AS value"
        )
        with self._driver.session() as session:
            return session.run(query, left_id=left_id, right_id=right_id).single()["value"]


def _neighbor_count_query(hops: int) -> str:
    if hops == 1:
        return (
            "MATCH (:User {id: $node_id})-[:LINK]->(target:User) "
            "WHERE target.id <> $node_id "
            "RETURN count(DISTINCT target) AS value"
        )
    if hops == 2:
        return (
            "MATCH (start:User {id: $node_id}) "
            "CALL { "
            "  WITH start "
            "  MATCH (start)-[:LINK]->(n1:User) "
            "  WHERE n1.id <> start.id "
            "  RETURN collect(DISTINCT n1.id) AS hop1 "
            "} "
            "CALL { "
            "  WITH start, hop1 "
            "  WITH start, hop1, CASE WHEN size(hop1) = 0 THEN [NULL] ELSE hop1 END AS hop1_ids "
            "  UNWIND hop1_ids AS hop1_id "
            "  OPTIONAL MATCH (:User {id: hop1_id})-[:LINK]->(n2:User) "
            "  WITH start, hop1, collect(DISTINCT n2.id) AS hop2_ids "
            "  RETURN [id IN hop2_ids "
            "    WHERE id IS NOT NULL AND id <> start.id AND NOT id IN hop1] AS hop2 "
            "} "
            "RETURN size(hop1) + size(hop2) AS value"
        )
    return (
        "MATCH (start:User {id: $node_id}) "
        "CALL { "
        "  WITH start "
        "  MATCH (start)-[:LINK]->(n1:User) "
        "  WHERE n1.id <> start.id "
        "  RETURN collect(DISTINCT n1.id) AS hop1 "
        "} "
        "CALL { "
        "  WITH start, hop1 "
        "  WITH start, hop1, CASE WHEN size(hop1) = 0 THEN [NULL] ELSE hop1 END AS hop1_ids "
        "  UNWIND hop1_ids AS hop1_id "
        "  OPTIONAL MATCH (:User {id: hop1_id})-[:LINK]->(n2:User) "
        "  WITH start, hop1, collect(DISTINCT n2.id) AS hop2_ids "
        "  RETURN [id IN hop2_ids "
        "    WHERE id IS NOT NULL AND id <> start.id AND NOT id IN hop1] AS hop2 "
        "} "
        "CALL { "
        "  WITH start, hop1, hop2 "
        "  WITH start, hop1, hop2, "
        "    CASE WHEN size(hop1) + size(hop2) = 0 THEN [NULL] ELSE hop1 + hop2 END AS frontier_ids "
        "  UNWIND frontier_ids AS frontier_id "
        "  OPTIONAL MATCH (:User {id: frontier_id})-[:LINK]->(n3:User) "
        "  WITH start, hop1, hop2, collect(DISTINCT n3.id) AS hop3_ids "
        "  RETURN [id IN hop3_ids "
        "    WHERE id IS NOT NULL AND id <> start.id AND NOT id IN hop1 AND NOT id IN hop2] AS hop3 "
        "} "
        "RETURN size(hop1) + size(hop2) + size(hop3) AS value"
    )
