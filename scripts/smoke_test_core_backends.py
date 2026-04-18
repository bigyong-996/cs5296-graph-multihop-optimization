from __future__ import annotations

import argparse

import psycopg
from neo4j import GraphDatabase

from graph_bench.adapters.neo4j_adapter import Neo4jAdapter
from graph_bench.adapters.postgres_adapter import PostgresAdapter
from graph_bench.config import load_settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", type=int, default=1)
    parser.add_argument("--left-id", type=int, default=1)
    parser.add_argument("--right-id", type=int, default=2)
    return parser


def run_smoke(neo4j_adapter, postgres_adapter, *, node_id: int, left_id: int, right_id: int) -> dict[str, int]:
    return {
        "neo4j_neighbors_1hop": neo4j_adapter.neighbor_count(node_id=node_id, hops=1),
        "postgres_neighbors_1hop": postgres_adapter.neighbor_count(node_id=node_id, hops=1),
        "neo4j_common_neighbors": neo4j_adapter.common_neighbor_count(
            left_id=left_id,
            right_id=right_id,
        ),
        "postgres_common_neighbors": postgres_adapter.common_neighbor_count(
            left_id=left_id,
            right_id=right_id,
        ),
    }


def main() -> None:
    args = build_parser().parse_args()
    settings = load_settings()

    neo4j_driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    postgres_connection = psycopg.connect(settings.postgres_dsn)

    neo4j_adapter = Neo4jAdapter(neo4j_driver)
    postgres_adapter = PostgresAdapter(postgres_connection)

    print(
        run_smoke(
            neo4j_adapter,
            postgres_adapter,
            node_id=args.node_id,
            left_id=args.left_id,
            right_id=args.right_id,
        )
    )


if __name__ == "__main__":
    main()
