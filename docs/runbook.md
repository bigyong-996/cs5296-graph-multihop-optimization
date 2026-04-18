# Runbook

## Core local startup

1. `python3 -m pip install -e ".[dev]"`
2. `docker compose -f infra/docker-compose.yml up -d neo4j postgres`
3. `python3 scripts/prepare_dataset.py --input tests/fixtures/raw/facebook_tiny.txt --dataset-name facebook_tiny --symmetrize --output-dir datasets/derived/facebook_tiny`
4. `python3 scripts/load_neo4j.py --dataset-dir datasets/derived/facebook_tiny`
5. `python3 scripts/load_postgres.py --dataset-dir datasets/derived/facebook_tiny`
6. `python3 scripts/smoke_test_core_backends.py`

## Benchmark path

1. Generate the real dataset directory under `datasets/derived/`
2. Write workload JSON under `benchmarks/`
3. Run `python3 scripts/run_benchmark.py --backend neo4j --dataset-name facebook_full --workload-file benchmarks/facebook.json --output results/raw/neo4j-facebook.jsonl`
4. Run `python3 scripts/run_benchmark.py --backend postgres --dataset-name facebook_full --workload-file benchmarks/facebook.json --output results/raw/postgres-facebook.jsonl`
5. Run `python3 scripts/aggregate_results.py --input results/raw/neo4j-facebook.jsonl --output results/summary/neo4j-facebook.csv`

## JanusGraph path

1. Start the JanusGraph profile with `docker compose -f infra/docker-compose.yml --profile janusgraph up -d cassandra janusgraph`
2. The local Docker configuration intentionally caps JanusGraph and Cassandra heap sizes for laptop-friendly execution
3. Run `python3 scripts/load_janusgraph.py --dataset-dir datasets/derived/facebook_tiny`
4. Run `python3 scripts/smoke_test_janusgraph.py`
