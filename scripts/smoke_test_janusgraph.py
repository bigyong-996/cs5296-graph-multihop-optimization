from __future__ import annotations

from gremlin_python.driver.client import Client

from graph_bench.adapters.janusgraph_adapter import JanusGraphAdapter
from graph_bench.config import load_settings


def main() -> None:
    client = Client(load_settings().janusgraph_url, "g")
    adapter = JanusGraphAdapter(client)
    print({"neighbors_1hop": adapter.neighbor_count(node_id=1, hops=1)})


if __name__ == "__main__":
    main()
