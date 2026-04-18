import csv
from pathlib import Path

from graph_bench.closure import build_bounded_closure
from graph_bench.closure import write_bounded_closure_csv
from graph_bench.models import GraphDataset, GraphMetadata


def test_build_bounded_closure_stops_at_depth_three() -> None:
    dataset = GraphDataset(
        metadata=GraphMetadata(
            dataset_name="chain",
            directed=False,
            node_count=5,
            edge_count=8,
        ),
        nodes={1, 2, 3, 4, 5},
        edges={
            (1, 2),
            (2, 1),
            (2, 3),
            (3, 2),
            (3, 4),
            (4, 3),
            (4, 5),
            (5, 4),
        },
    )

    rows = build_bounded_closure(dataset, max_depth=3)

    assert (1, 4, 3) in rows
    assert (1, 5, 4) not in rows


def test_write_bounded_closure_csv_streams_expected_rows(tmp_path: Path) -> None:
    dataset = GraphDataset(
        metadata=GraphMetadata(
            dataset_name="triangle",
            directed=False,
            node_count=3,
            edge_count=6,
        ),
        nodes={1, 2, 3},
        edges={
            (1, 2),
            (2, 1),
            (2, 3),
            (3, 2),
            (1, 3),
            (3, 1),
        },
    )
    output_path = tmp_path / "closure_3.csv"

    write_bounded_closure_csv(dataset, max_depth=3, output_path=output_path)

    with output_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0] == {"src": "1", "dst": "2", "depth": "1"}
    assert {"src": "1", "dst": "3", "depth": "1"} in rows
    assert {"src": "2", "dst": "3", "depth": "1"} in rows
