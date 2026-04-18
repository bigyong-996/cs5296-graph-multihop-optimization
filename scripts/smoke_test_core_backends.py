from __future__ import annotations

import psycopg
from neo4j import GraphDatabase

from graph_bench.adapters.neo4j_adapter import Neo4jAdapter
from graph_bench.adapters.postgres_adapter import PostgresAdapter
from graph_bench.config import load_settings


def main() -> None:
    settings = load_settings()

    neo4j_driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    postgres_connection = psycopg.connect(settings.postgres_dsn)

    neo4j_adapter = Neo4jAdapter(neo4j_driver)
    postgres_adapter = PostgresAdapter(postgres_connection)

    print(
        {
            "neo4j_neighbors_1hop": neo4j_adapter.neighbor_count(node_id=1, hops=1),
            "postgres_neighbors_1hop": postgres_adapter.neighbor_count(node_id=1, hops=1),
            "neo4j_common_neighbors": neo4j_adapter.common_neighbor_count(left_id=1, right_id=2),
            "postgres_common_neighbors": postgres_adapter.common_neighbor_count(left_id=1, right_id=2),
        }
    )


if __name__ == "__main__":
    main()
