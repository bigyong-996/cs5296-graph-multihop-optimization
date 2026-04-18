from pathlib import Path

from scripts.aggregate_results import aggregate_jsonl


def test_aggregate_jsonl_produces_summary_table(tmp_path: Path) -> None:
    input_path = tmp_path / "raw.jsonl"
    input_path.write_text(
        "\n".join(
            [
                '{"backend":"neo4j","dataset":"tiny","query_type":"neighbors","run_id":0,"latency_ms":1.0,"success":true,"result_size":2}',
                '{"backend":"neo4j","dataset":"tiny","query_type":"neighbors","run_id":1,"latency_ms":3.0,"success":true,"result_size":2}',
            ]
        ),
        encoding="utf-8",
    )

    summary = aggregate_jsonl(input_path)

    assert summary.loc[0, "backend"] == "neo4j"
    assert summary.loc[0, "p50_latency_ms"] == 2.0
