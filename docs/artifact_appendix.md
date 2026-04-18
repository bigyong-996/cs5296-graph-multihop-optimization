# Artifact Appendix Draft

## Primary artifact scope

The primary reproducible artifact is the local benchmark pipeline for:

- `facebook_full` on `Neo4j + PostgreSQL`
- `twitter_top10000` on `Neo4j + PostgreSQL`

JanusGraph is included as a secondary enhancement path only.

## Repository entrypoints

- Data preparation: `scripts/prepare_dataset.py`
- Neo4j import: `scripts/load_neo4j.py`
- PostgreSQL import: `scripts/load_postgres.py`
- JanusGraph import: `scripts/load_janusgraph.py`
- Benchmark execution: `scripts/run_benchmark.py`
- Result aggregation: `scripts/aggregate_results.py`
- Plot generation: `scripts/plot_results.py`
- Experiment notes: `docs/experiment_notes.md`

## Minimal verification commands

1. `python3 -m pytest -q`
2. `python3 scripts/smoke_test_core_backends.py`
3. `python3 scripts/smoke_test_core_backends.py --node-id 964 --left-id 0 --right-id 1`
4. `python3 scripts/smoke_test_core_backends.py --node-id 21409847 --left-id 12 --right-id 13`
5. `python3 scripts/run_benchmark.py --backend neo4j --dataset-name facebook_full --workload-file benchmarks/facebook_full.json --output results/raw/neo4j-facebook-full.jsonl`
6. `python3 scripts/run_benchmark.py --backend postgres --dataset-name facebook_full --workload-file benchmarks/facebook_full.json --output results/raw/postgres-facebook-full.jsonl`
7. `python3 scripts/run_benchmark.py --backend neo4j --dataset-name twitter_top10000 --workload-file benchmarks/twitter_top10000.json --output results/raw/neo4j-twitter-top10000.jsonl`
8. `python3 scripts/run_benchmark.py --backend postgres --dataset-name twitter_top10000 --workload-file benchmarks/twitter_top10000.json --output results/raw/postgres-twitter-top10000.jsonl`
9. `python3 scripts/load_janusgraph.py --dataset-dir datasets/derived/facebook_full`
10. `python3 scripts/smoke_test_janusgraph.py --node-id 1`

## Expected result artifacts

- `results/summary/facebook-full-comparison.csv`
- `results/summary/facebook-full-p50-latency.png`
- `results/summary/twitter-top10000-comparison.csv`
- `results/summary/twitter-top10000-p50-latency.png`

These files form the main report-ready evidence bundle.

## Notes on interpretation

- The Facebook and Twitter main results compare `Neo4j` online traversal against `PostgreSQL + closure_3`
- This is a meaningful systems comparison, but it is not a fully symmetric engine-only benchmark
- JanusGraph should be described as a secondary validation/enhancement path rather than part of the main matrix
- The current artifact includes JanusGraph full-data smoke validation on `facebook_full`, but not a full JanusGraph benchmark matrix
