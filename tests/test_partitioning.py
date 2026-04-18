from graph_bench.models import GraphDataset, GraphMetadata
from graph_bench.partitioning import edge_cut_ratio, hash_partition, locality_aware_partition


def test_locality_aware_partition_reduces_edge_cut_on_clustered_graph() -> None:
    dataset = GraphDataset(
        metadata=GraphMetadata(dataset_name="clustered", directed=False, node_count=6, edge_count=14),
        nodes={1, 2, 3, 4, 5, 6},
        edges={
            (1, 2),
            (2, 1),
            (2, 3),
            (3, 2),
            (1, 3),
            (3, 1),
            (4, 5),
            (5, 4),
            (5, 6),
            (6, 5),
            (4, 6),
            (6, 4),
            (3, 4),
            (4, 3),
        },
    )

    hash_assignments = hash_partition(dataset, partition_count=2)
    locality_assignments = locality_aware_partition(dataset, partition_count=2)

    assert edge_cut_ratio(dataset, locality_assignments) < edge_cut_ratio(dataset, hash_assignments)
