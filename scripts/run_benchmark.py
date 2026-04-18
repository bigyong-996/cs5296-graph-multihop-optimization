from __future__ import annotations

import argparse
import json
from pathlib import Path

from gremlin_python.driver.client import Client
import psycopg
from neo4j import GraphDatabase

from graph_bench.adapters.janusgraph_adapter import JanusGraphAdapter
from graph_bench.adapters.neo4j_adapter import Neo4jAdapter
from graph_bench.adapters.postgres_adapter import PostgresAdapter
from graph_bench.benchmark_runner import run_benchmark
from graph_bench.config import load_settings
from graph_bench.workloads import WorkloadCase


def _load_workloads(path: Path) -> list[WorkloadCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [WorkloadCase(**row) for row in payload]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--backend",
        required=True,
        choices=["neo4j", "postgres", "janusgraph"],
    )
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--workload-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--warmup-count", type=int, default=2)
    parser.add_argument("--measured-count", type=int, default=5)
    args = parser.parse_args()

    settings = load_settings()
    workloads = _load_workloads(Path(args.workload_file))

    if args.backend == "neo4j":
        driver = GraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
        )
        backend = Neo4jAdapter(driver)
    elif args.backend == "postgres":
        backend = PostgresAdapter(psycopg.connect(settings.postgres_dsn))
    else:
        backend = JanusGraphAdapter(Client(settings.janusgraph_url, "g"))

    run_benchmark(
        backend_name=args.backend,
        dataset_name=args.dataset_name,
        backend=backend,
        workloads=workloads,
        warmup_count=args.warmup_count,
        measured_count=args.measured_count,
        output_path=Path(args.output),
    )


if __name__ == "__main__":
    main()
