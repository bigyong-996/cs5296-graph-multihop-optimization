from pathlib import Path


def test_runbook_mentions_core_commands() -> None:
    runbook = Path("docs/runbook.md").read_text(encoding="utf-8")
    appendix = Path("docs/artifact_appendix.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    experiment_notes = Path("docs/experiment_notes.md").read_text(encoding="utf-8")

    assert "scripts/prepare_dataset.py" in runbook
    assert "scripts/run_benchmark.py" in appendix
    assert "docker compose -f infra/docker-compose.yml up -d neo4j postgres" in readme
    assert "facebook_full.json" in runbook
    assert "twitter_top10000.json" in runbook
    assert "twitter-top10000-p50-latency.png" in appendix
    assert "PostgreSQL + closure_3" in experiment_notes
