from __future__ import annotations

import argparse
import csv
from pathlib import Path

import psycopg

from graph_bench.config import load_settings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    args = parser.parse_args()

    settings = load_settings()
    dataset_dir = Path(args.dataset_dir)
    with psycopg.connect(settings.postgres_dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS closure_3")
            cursor.execute("DROP TABLE IF EXISTS edges")
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("CREATE TABLE users (node_id BIGINT PRIMARY KEY)")
            cursor.execute(
                "CREATE TABLE edges (src BIGINT NOT NULL, dst BIGINT NOT NULL, PRIMARY KEY (src, dst))"
            )
            cursor.execute(
                "CREATE TABLE closure_3 (src BIGINT NOT NULL, dst BIGINT NOT NULL, depth INT NOT NULL, PRIMARY KEY (src, dst))"
            )
            with (dataset_dir / "nodes.csv").open(encoding="utf-8") as node_file:
                for row in csv.DictReader(node_file):
                    cursor.execute(
                        "INSERT INTO users (node_id) VALUES (%s)",
                        (int(row["node_id"]),),
                    )
            with (dataset_dir / "edges.csv").open(encoding="utf-8") as edge_file:
                for row in csv.DictReader(edge_file):
                    cursor.execute(
                        "INSERT INTO edges (src, dst) VALUES (%s, %s)",
                        (int(row["src"]), int(row["dst"])),
                    )
            with (dataset_dir / "closure_3.csv").open(encoding="utf-8") as closure_file:
                for row in csv.DictReader(closure_file):
                    cursor.execute(
                        "INSERT INTO closure_3 (src, dst, depth) VALUES (%s, %s, %s)",
                        (int(row["src"]), int(row["dst"]), int(row["depth"])),
                    )
        connection.commit()


if __name__ == "__main__":
    main()
