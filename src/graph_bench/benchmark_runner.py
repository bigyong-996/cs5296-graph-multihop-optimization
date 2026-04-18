from __future__ import annotations

from pathlib import Path
from time import perf_counter

from graph_bench.results import BenchmarkRow, append_rows
from graph_bench.workloads import WorkloadCase


def _execute_case(backend, workload: WorkloadCase) -> int | None:
    if workload.query_type == "neighbors":
        return backend.neighbor_count(node_id=workload.node_id, hops=workload.hops)
    if workload.query_type == "common_neighbors":
        return backend.common_neighbor_count(
            left_id=workload.left_id,
            right_id=workload.right_id,
        )
    if workload.query_type == "shortest_path":
        return backend.shortest_path_up_to_3(
            left_id=workload.left_id,
            right_id=workload.right_id,
        )
    raise ValueError(f"unsupported query type: {workload.query_type}")


def run_benchmark(
    *,
    backend_name: str,
    dataset_name: str,
    backend,
    workloads: list[WorkloadCase],
    warmup_count: int,
    measured_count: int,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("", encoding="utf-8")

    for workload in workloads:
        for _ in range(warmup_count):
            _execute_case(backend, workload)

        measured_rows: list[BenchmarkRow] = []
        for run_id in range(measured_count):
            start = perf_counter()
            result = _execute_case(backend, workload)
            latency_ms = round((perf_counter() - start) * 1000, 3)
            measured_rows.append(
                BenchmarkRow(
                    backend=backend_name,
                    dataset=dataset_name,
                    query_type=workload.query_type,
                    run_id=run_id,
                    latency_ms=latency_ms,
                    success=True,
                    result_size=result,
                )
            )
        append_rows(measured_rows, output_path)
