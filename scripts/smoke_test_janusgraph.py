from __future__ import annotations

import argparse

from gremlin_python.driver.client import Client

from graph_bench.adapters.janusgraph_adapter import JanusGraphAdapter
from graph_bench.config import load_settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", type=int, default=1)
    return parser


def run_smoke(adapter, *, node_id: int) -> dict[str, int]:
    return {"neighbors_1hop": adapter.neighbor_count(node_id=node_id, hops=1)}


def main() -> None:
    args = build_parser().parse_args()
    client = Client(load_settings().janusgraph_url, "g")
    adapter = JanusGraphAdapter(client)
    print(run_smoke(adapter, node_id=args.node_id))


if __name__ == "__main__":
    main()
