from __future__ import annotations

import argparse
import csv
from pathlib import Path

from neo4j import GraphDatabase

from graph_bench.config import load_settings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    args = parser.parse_args()

    settings = load_settings()
    dataset_dir = Path(args.dataset_dir)
    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        session.run(
            "CREATE CONSTRAINT user_id IF NOT EXISTS "
            "FOR (u:User) REQUIRE u.id IS UNIQUE"
        )
        with (dataset_dir / "nodes.csv").open(encoding="utf-8") as node_file:
            for row in csv.DictReader(node_file):
                session.run("MERGE (:User {id: $node_id})", node_id=int(row["node_id"]))
        with (dataset_dir / "edges.csv").open(encoding="utf-8") as edge_file:
            for row in csv.DictReader(edge_file):
                session.run(
                    "MATCH (src:User {id: $src}), (dst:User {id: $dst}) "
                    "MERGE (src)-[:LINK]->(dst)",
                    src=int(row["src"]),
                    dst=int(row["dst"]),
                )


if __name__ == "__main__":
    main()
