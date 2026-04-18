from __future__ import annotations

from psycopg.rows import dict_row


class PostgresAdapter:
    def __init__(self, connection) -> None:
        self._connection = connection

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        query = (
            "SELECT COUNT(DISTINCT dst) AS value "
            "FROM closure_3 "
            "WHERE src = %(node_id)s AND depth <= %(max_depth)s"
        )
        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, {"node_id": node_id, "max_depth": hops})
            return int(cursor.fetchone()["value"])

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        query = (
            "SELECT COUNT(*) AS value "
            "FROM ("
            "  SELECT dst FROM closure_3 WHERE src = %(left_id)s AND depth = 1 "
            "  INTERSECT "
            "  SELECT dst FROM closure_3 WHERE src = %(right_id)s AND depth = 1"
            ") AS common_neighbors"
        )
        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, {"left_id": left_id, "right_id": right_id})
            return int(cursor.fetchone()["value"])

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        query = (
            "SELECT MIN(depth) AS value "
            "FROM closure_3 "
            "WHERE src = %(left_id)s AND dst = %(right_id)s"
        )
        with self._connection.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, {"left_id": left_id, "right_id": right_id})
            return cursor.fetchone()["value"]
