from __future__ import annotations

import argparse
from pathlib import Path

import psycopg

from graph_bench.config import load_settings


def copy_csv(cursor, csv_path: Path, table_name: str, columns: str) -> None:
    with csv_path.open("r", encoding="utf-8") as handle:
        with cursor.copy(
            f"COPY {table_name} ({columns}) FROM STDIN WITH (FORMAT csv, HEADER true)"
        ) as copy:
            while chunk := handle.read(1024 * 1024):
                copy.write(chunk)


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
            cursor.execute("CREATE TABLE users (node_id BIGINT NOT NULL)")
            cursor.execute("CREATE TABLE edges (src BIGINT NOT NULL, dst BIGINT NOT NULL)")
            cursor.execute(
                "CREATE TABLE closure_3 (src BIGINT NOT NULL, dst BIGINT NOT NULL, depth INT NOT NULL)"
            )

            copy_csv(cursor, dataset_dir / "nodes.csv", "users", "node_id")
            copy_csv(cursor, dataset_dir / "edges.csv", "edges", "src, dst")
            copy_csv(cursor, dataset_dir / "closure_3.csv", "closure_3", "src, dst, depth")

            cursor.execute("ALTER TABLE users ADD PRIMARY KEY (node_id)")
            cursor.execute("ALTER TABLE edges ADD PRIMARY KEY (src, dst)")
            cursor.execute("ALTER TABLE closure_3 ADD PRIMARY KEY (src, dst)")
        connection.commit()


if __name__ == "__main__":
    main()
