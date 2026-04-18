from graph_bench.adapters.janusgraph_adapter import JanusGraphAdapter


class FakeResponse:
    def __init__(self, value):
        self._value = value

    def all(self):
        return [self._value]


class FakeClient:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def submit(self, query, bindings=None):
        self.calls.append((query, bindings))
        value = self.values.pop(0)
        return FakeResponse(value)


def test_neighbor_count_uses_repeat_both_times_hops() -> None:
    client = FakeClient([5])
    adapter = JanusGraphAdapter(client)

    result = adapter.neighbor_count(node_id=9, hops=2)

    assert result == 5
    query, bindings = client.calls[0]
    assert "repeat(both('link')).times(hops)" in query
    assert bindings == {"node_id": 9, "hops": 2}
