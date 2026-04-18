from pathlib import Path

from scripts.load_janusgraph import load_dataset


class FakeFuture:
    def __init__(self, value):
        self._value = value

    def result(self):
        if self._value is None:
            return []
        return [self._value]


class FakeResponse:
    def __init__(self, value):
        self._value = value

    def all(self):
        return FakeFuture(self._value)


class FakeClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, int] | None]] = []

    def submit(self, query, bindings=None):
        self.calls.append((query, bindings))
        if "id().next()" in query:
            return FakeResponse(bindings["node_id"] + 1000)
        return FakeResponse(None)


def test_load_dataset_uses_internal_vertex_ids_for_edges(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "dataset"
    dataset_dir.mkdir()
    (dataset_dir / "nodes.csv").write_text("node_id\n1\n2\n", encoding="utf-8")
    (dataset_dir / "edges.csv").write_text("src,dst\n1,2\n2,1\n", encoding="utf-8")
    client = FakeClient()

    load_dataset(client, dataset_dir)

    queries = [query for query, _ in client.calls]
    bindings = [bindings for _, bindings in client.calls]
    assert queries[0] == "g.V().drop().iterate()"
    assert "g.addV('user').property('id', node_id).id().next()" in queries[1]
    assert "g.V(src_vertex).as('src').V(dst_vertex).addE('link').from('src').iterate()" in queries[3]
    assert bindings[3] == {"src_vertex": 1001, "dst_vertex": 1002}
    assert bindings[4] == {"src_vertex": 1002, "dst_vertex": 1001}
