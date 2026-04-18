from __future__ import annotations

import argparse
from pathlib import Path

from graph_bench.canonical import read_edge_list
from graph_bench.partitioning import edge_cut_ratio, hash_partition, locality_aware_partition


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--partitions", type=int, default=4)
    args = parser.parse_args()

    dataset = read_edge_list(
        Path(args.input),
        dataset_name="partition_eval",
        directed=False,
        symmetrize=True,
    )
    hash_assignments = hash_partition(dataset, partition_count=args.partitions)
    locality_assignments = locality_aware_partition(dataset, partition_count=args.partitions)
    print(
        {
            "hash_edge_cut": edge_cut_ratio(dataset, hash_assignments),
            "locality_edge_cut": edge_cut_ratio(dataset, locality_assignments),
        }
    )


if __name__ == "__main__":
    main()
