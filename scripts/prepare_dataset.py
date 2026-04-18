from __future__ import annotations

import argparse
from pathlib import Path

from graph_bench.canonical import read_edge_list, top_degree_subgraph, write_canonical_dataset
from graph_bench.closure import write_bounded_closure_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--symmetrize", action="store_true")
    parser.add_argument("--max-nodes", type=int)
    args = parser.parse_args()

    dataset = read_edge_list(
        Path(args.input),
        dataset_name=args.dataset_name,
        directed=not args.symmetrize,
        symmetrize=args.symmetrize,
    )
    if args.max_nodes:
        dataset = top_degree_subgraph(
            dataset,
            max_nodes=args.max_nodes,
            sampled_name=f"{args.dataset_name}_top{args.max_nodes}",
        )

    output_dir = Path(args.output_dir)
    write_canonical_dataset(dataset, output_dir)
    write_bounded_closure_csv(dataset, max_depth=3, output_path=output_dir / "closure_3.csv")


if __name__ == "__main__":
    main()
