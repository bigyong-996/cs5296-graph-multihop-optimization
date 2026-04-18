from __future__ import annotations

import argparse
import csv
from pathlib import Path

from gremlin_python.driver.client import Client

from graph_bench.config import load_settings


def _drain(response) -> None:
    result = response.all()
    if hasattr(result, "result"):
        result.result()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    args = parser.parse_args()

    client = Client(load_settings().janusgraph_url, "g")
    dataset_dir = Path(args.dataset_dir)
    _drain(client.submit("g.V().drop().iterate()"))

    with (dataset_dir / "nodes.csv").open(encoding="utf-8") as node_file:
        for row in csv.DictReader(node_file):
            _drain(
                client.submit(
                    "g.addV('user').property('id', node_id).iterate()",
                    {"node_id": int(row["node_id"])},
                )
            )

    with (dataset_dir / "edges.csv").open(encoding="utf-8") as edge_file:
        for row in csv.DictReader(edge_file):
            _drain(
                client.submit(
                    "g.V().has('user','id',src).as('src').V().has('user','id',dst)"
                    ".addE('link').from('src').iterate()",
                    {"src": int(row["src"]), "dst": int(row["dst"])},
                )
            )


if __name__ == "__main__":
    main()
