from scripts.smoke_test_core_backends import build_parser as build_core_parser
from scripts.smoke_test_core_backends import run_smoke as run_core_smoke
from scripts.smoke_test_janusgraph import build_parser as build_janusgraph_parser
from scripts.smoke_test_janusgraph import run_smoke as run_janusgraph_smoke


class FakeCoreAdapter:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, int]]] = []

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        self.calls.append(("neighbor_count", {"node_id": node_id, "hops": hops}))
        return 7

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        self.calls.append(("common_neighbor_count", {"left_id": left_id, "right_id": right_id}))
        return 3


class FakeJanusGraphAdapter:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, int]]] = []

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        self.calls.append(("neighbor_count", {"node_id": node_id, "hops": hops}))
        return 5


def test_core_smoke_parser_accepts_custom_ids() -> None:
    args = build_core_parser().parse_args(["--node-id", "42", "--left-id", "11", "--right-id", "12"])

    assert args.node_id == 42
    assert args.left_id == 11
    assert args.right_id == 12


def test_core_smoke_uses_supplied_ids() -> None:
    neo4j_adapter = FakeCoreAdapter()
    postgres_adapter = FakeCoreAdapter()

    result = run_core_smoke(
        neo4j_adapter,
        postgres_adapter,
        node_id=42,
        left_id=11,
        right_id=12,
    )

    assert result == {
        "neo4j_neighbors_1hop": 7,
        "postgres_neighbors_1hop": 7,
        "neo4j_common_neighbors": 3,
        "postgres_common_neighbors": 3,
    }
    assert neo4j_adapter.calls == [
        ("neighbor_count", {"node_id": 42, "hops": 1}),
        ("common_neighbor_count", {"left_id": 11, "right_id": 12}),
    ]
    assert postgres_adapter.calls == [
        ("neighbor_count", {"node_id": 42, "hops": 1}),
        ("common_neighbor_count", {"left_id": 11, "right_id": 12}),
    ]


def test_janusgraph_smoke_parser_accepts_custom_node_id() -> None:
    args = build_janusgraph_parser().parse_args(["--node-id", "99"])

    assert args.node_id == 99


def test_janusgraph_smoke_uses_supplied_node_id() -> None:
    adapter = FakeJanusGraphAdapter()

    result = run_janusgraph_smoke(adapter, node_id=99)

    assert result == {"neighbors_1hop": 5}
    assert adapter.calls == [("neighbor_count", {"node_id": 99, "hops": 1})]
