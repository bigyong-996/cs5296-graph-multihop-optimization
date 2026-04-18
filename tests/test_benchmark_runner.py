import json
from pathlib import Path

from graph_bench.benchmark_runner import run_benchmark
from graph_bench.workloads import WorkloadCase


class FakeBackend:
    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        return node_id + hops

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        return left_id + right_id

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        return 2


def test_run_benchmark_emits_only_measured_rows(tmp_path: Path) -> None:
    output_path = tmp_path / "results.jsonl"
    workloads = [
        WorkloadCase(query_type="neighbors", node_id=1, hops=1),
        WorkloadCase(query_type="shortest_path", left_id=1, right_id=3, hops=3),
    ]

    run_benchmark(
        backend_name="fake",
        dataset_name="tiny",
        backend=FakeBackend(),
        workloads=workloads,
        warmup_count=1,
        measured_count=2,
        output_path=output_path,
    )

    rows = [json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 4
    assert {row["query_type"] for row in rows} == {"neighbors", "shortest_path"}
