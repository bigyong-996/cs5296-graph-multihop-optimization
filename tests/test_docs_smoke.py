from pathlib import Path


def test_runbook_mentions_core_commands() -> None:
    runbook = Path("docs/runbook.md").read_text(encoding="utf-8")
    appendix = Path("docs/artifact_appendix.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "scripts/prepare_dataset.py" in runbook
    assert "scripts/run_benchmark.py" in appendix
    assert "docker compose -f infra/docker-compose.yml up -d neo4j postgres" in readme
