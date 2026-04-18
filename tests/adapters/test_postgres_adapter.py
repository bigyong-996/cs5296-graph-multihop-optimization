from graph_bench.adapters.postgres_adapter import PostgresAdapter


class FakeCursor:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def execute(self, query, params):
        self.calls.append((query, params))

    def fetchone(self):
        return {"value": self.values.pop(0)}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self, values):
        self.cursor_obj = FakeCursor(values)

    def cursor(self, row_factory=None):
        return self.cursor_obj


def test_neighbor_count_reads_from_bounded_closure_table() -> None:
    connection = FakeConnection([7])
    adapter = PostgresAdapter(connection)

    result = adapter.neighbor_count(node_id=11, hops=3)

    assert result == 7
    query, params = connection.cursor_obj.calls[0]
    assert "closure_3" in query
    assert params == {"node_id": 11, "max_depth": 3}
