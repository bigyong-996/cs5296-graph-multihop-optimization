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


def _drain_scalar(response):
    result = response.all()
    if hasattr(result, "result"):
        result = result.result()
    if not result:
        return None
    return result[0]


def load_dataset(client, dataset_dir: Path) -> None:
    _drain(client.submit("g.V().drop().iterate()"))
    vertex_ids: dict[int, int] = {}

    with (dataset_dir / "nodes.csv").open(encoding="utf-8") as node_file:
        for row in csv.DictReader(node_file):
            node_id = int(row["node_id"])
            vertex_ids[node_id] = int(
                _drain_scalar(
                    client.submit(
                        "g.addV('user').property('id', node_id).id().next()",
                        {"node_id": node_id},
                    )
                )
            )

    with (dataset_dir / "edges.csv").open(encoding="utf-8") as edge_file:
        for row in csv.DictReader(edge_file):
            _drain(
                client.submit(
                    "g.V(src_vertex).as('src').V(dst_vertex).addE('link').from('src').iterate()",
                    {
                        "src_vertex": vertex_ids[int(row["src"])],
                        "dst_vertex": vertex_ids[int(row["dst"])],
                    },
                )
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    args = parser.parse_args()

    client = Client(load_settings().janusgraph_url, "g")
    dataset_dir = Path(args.dataset_dir)
    load_dataset(client, dataset_dir)


if __name__ == "__main__":
    main()
