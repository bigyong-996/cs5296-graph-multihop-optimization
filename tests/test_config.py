from graph_bench.config import load_settings


def test_load_settings_uses_local_defaults() -> None:
    settings = load_settings()

    assert settings.neo4j_uri == "bolt://localhost:7687"
    assert settings.postgres_dsn == "postgresql://postgres:postgres@localhost:5432/graphbench"
    assert settings.janusgraph_url == "ws://localhost:8182/gremlin"
