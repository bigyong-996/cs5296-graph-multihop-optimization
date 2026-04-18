from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    pivot = frame.pivot(index="query_type", columns="backend", values="p50_latency_ms")
    pivot.plot(kind="bar", ylabel="p50 latency (ms)", rot=0)
    plt.tight_layout()
    plt.savefig(args.output, dpi=200)


if __name__ == "__main__":
    main()
