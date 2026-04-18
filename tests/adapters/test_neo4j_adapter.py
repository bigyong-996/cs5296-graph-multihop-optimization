from graph_bench.adapters.neo4j_adapter import Neo4jAdapter


class FakeResult:
    def __init__(self, value):
        self._value = value

    def single(self):
        return {"value": self._value}


class FakeSession:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def run(self, query, **params):
        self.calls.append((query, params))
        return FakeResult(self.values.pop(0))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeDriver:
    def __init__(self, values):
        self.session_obj = FakeSession(values)

    def session(self):
        return self.session_obj


def test_neighbor_count_uses_bounded_relationship_length() -> None:
    driver = FakeDriver([5])
    adapter = Neo4jAdapter(driver)

    result = adapter.neighbor_count(node_id=1, hops=2)

    assert result == 5
    query, params = driver.session_obj.calls[0]
    assert "*1..2" in query
    assert params == {"node_id": 1}
