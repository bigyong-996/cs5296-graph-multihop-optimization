from graph_bench.closure import build_bounded_closure
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
