from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def aggregate_jsonl(input_path: Path) -> pd.DataFrame:
    frame = pd.read_json(input_path, lines=True)
    summary = (
        frame.groupby(["backend", "dataset", "query_type"], as_index=False)
        .agg(
            p50_latency_ms=("latency_ms", "median"),
            p95_latency_ms=("latency_ms", lambda series: round(series.quantile(0.95), 3)),
            avg_result_size=("result_size", "mean"),
            success_rate=("success", "mean"),
        )
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    aggregate_jsonl(Path(args.input)).to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
