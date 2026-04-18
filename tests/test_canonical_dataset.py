from pathlib import Path

from graph_bench.canonical import read_edge_list, top_degree_subgraph


def test_read_edge_list_symmetrizes_undirected_graph() -> None:
    dataset = read_edge_list(
        Path("tests/fixtures/raw/facebook_tiny.txt"),
        dataset_name="facebook_tiny",
        directed=False,
        symmetrize=True,
    )

    assert dataset.metadata.dataset_name == "facebook_tiny"
    assert dataset.metadata.node_count == 4
    assert (1, 2) in dataset.edges
    assert (2, 1) in dataset.edges
    assert (4, 3) in dataset.edges


def test_top_degree_subgraph_keeps_highest_degree_nodes() -> None:
    dataset = read_edge_list(
        Path("tests/fixtures/raw/facebook_tiny.txt"),
        dataset_name="facebook_tiny",
        directed=False,
        symmetrize=True,
    )

    sampled = top_degree_subgraph(dataset, max_nodes=3, sampled_name="facebook_top3")

    assert sampled.metadata.dataset_name == "facebook_top3"
    assert sampled.nodes == {1, 2, 3}
    assert (3, 4) not in sampled.edges
