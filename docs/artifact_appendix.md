# Artifact Appendix Draft

## Repository entrypoints

- Data preparation: `scripts/prepare_dataset.py`
- Neo4j import: `scripts/load_neo4j.py`
- PostgreSQL import: `scripts/load_postgres.py`
- JanusGraph import: `scripts/load_janusgraph.py`
- Benchmark execution: `scripts/run_benchmark.py`
- Result aggregation: `scripts/aggregate_results.py`
- Plot generation: `scripts/plot_results.py`

## Minimal verification commands

1. `python3 -m pytest tests/test_package_smoke.py tests/test_canonical_dataset.py tests/test_closure.py tests/adapters/test_neo4j_adapter.py tests/adapters/test_postgres_adapter.py tests/test_benchmark_runner.py -q`
2. `python3 scripts/smoke_test_core_backends.py`
3. `python3 scripts/run_benchmark.py --backend neo4j --dataset-name facebook_full --workload-file benchmarks/facebook.json --output results/raw/neo4j-facebook.jsonl`
4. `docker compose -f infra/docker-compose.yml --profile janusgraph up -d cassandra janusgraph`
5. `python3 scripts/smoke_test_janusgraph.py`
