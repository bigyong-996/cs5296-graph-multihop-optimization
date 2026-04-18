from pathlib import Path


def test_core_smoke_script_uses_both_primary_adapters() -> None:
    contents = Path("scripts/smoke_test_core_backends.py").read_text(encoding="utf-8")

    assert "Neo4jAdapter" in contents
    assert "PostgresAdapter" in contents
