# Runbook

## Core local startup

1. `python3 -m pip install -e ".[dev]"`
2. `docker compose -f infra/docker-compose.yml up -d neo4j postgres`
3. `python3 scripts/prepare_dataset.py --input tests/fixtures/raw/facebook_tiny.txt --dataset-name facebook_tiny --symmetrize --output-dir datasets/derived/facebook_tiny`
4. `python3 scripts/load_neo4j.py --dataset-dir datasets/derived/facebook_tiny`
5. `python3 scripts/load_postgres.py --dataset-dir datasets/derived/facebook_tiny`
6. `python3 scripts/smoke_test_core_backends.py`

## Primary benchmark path

Important note:

- The local `Neo4j` and `PostgreSQL` containers hold one dataset at a time
- Before running a smoke test or benchmark, load the corresponding dataset into both backends

### Facebook main path

1. Prepare data:
   - `python3 scripts/prepare_dataset.py --input datasets/raw/facebook_combined.txt --dataset-name facebook_full --symmetrize --output-dir datasets/derived/facebook_full`
2. Load both backends:
   - `python3 scripts/load_neo4j.py --dataset-dir datasets/derived/facebook_full`
   - `python3 scripts/load_postgres.py --dataset-dir datasets/derived/facebook_full`
3. Run the parameterized smoke check:
   - `python3 scripts/smoke_test_core_backends.py --node-id 964 --left-id 0 --right-id 1`
4. Run benchmarks:
   - `python3 scripts/run_benchmark.py --backend neo4j --dataset-name facebook_full --workload-file benchmarks/facebook_full.json --output results/raw/neo4j-facebook-full.jsonl`
   - `python3 scripts/run_benchmark.py --backend postgres --dataset-name facebook_full --workload-file benchmarks/facebook_full.json --output results/raw/postgres-facebook-full.jsonl`
5. Aggregate and plot:
   - `python3 scripts/aggregate_results.py --input results/raw/neo4j-facebook-full.jsonl --output results/summary/neo4j-facebook-full.csv`
   - `python3 scripts/aggregate_results.py --input results/raw/postgres-facebook-full.jsonl --output results/summary/postgres-facebook-full.csv`
   - `python3 scripts/plot_results.py --input results/summary/facebook-full-comparison.csv --output results/summary/facebook-full-p50-latency.png`

### Twitter main path

1. Prepare raw data:
   - `curl -L https://snap.stanford.edu/data/twitter_combined.txt.gz -o datasets/raw/twitter_combined.txt.gz`
   - `gzip -dc datasets/raw/twitter_combined.txt.gz > datasets/raw/twitter_combined.txt`
2. Prepare canonical data:
   - `python3 scripts/prepare_dataset.py --input datasets/raw/twitter_combined.txt --dataset-name twitter --symmetrize --max-nodes 10000 --output-dir datasets/derived/twitter_top10000`
3. Regenerate workload from real nodes:
   - `benchmarks/twitter_top10000.json`
4. Load both backends:
   - `python3 scripts/load_neo4j.py --dataset-dir datasets/derived/twitter_top10000`
   - `python3 scripts/load_postgres.py --dataset-dir datasets/derived/twitter_top10000`
5. Run the parameterized smoke check:
   - `python3 scripts/smoke_test_core_backends.py --node-id 21409847 --left-id 12 --right-id 13`
6. Run benchmarks:
   - `python3 scripts/run_benchmark.py --backend neo4j --dataset-name twitter_top10000 --workload-file benchmarks/twitter_top10000.json --output results/raw/neo4j-twitter-top10000.jsonl`
   - `python3 scripts/run_benchmark.py --backend postgres --dataset-name twitter_top10000 --workload-file benchmarks/twitter_top10000.json --output results/raw/postgres-twitter-top10000.jsonl`
7. Aggregate and plot:
   - `python3 scripts/aggregate_results.py --input results/raw/neo4j-twitter-top10000.jsonl --output results/summary/neo4j-twitter-top10000.csv`
   - `python3 scripts/aggregate_results.py --input results/raw/postgres-twitter-top10000.jsonl --output results/summary/postgres-twitter-top10000.csv`
   - `python3 scripts/plot_results.py --input results/summary/twitter-top10000-comparison.csv --output results/summary/twitter-top10000-p50-latency.png`

## JanusGraph path

JanusGraph is a secondary enhancement path, not part of the primary comparison matrix.

1. Start the JanusGraph profile:
   - `docker compose -f infra/docker-compose.yml --profile janusgraph up -d cassandra janusgraph`
2. Run the tiny validation path:
   - `python3 scripts/load_janusgraph.py --dataset-dir datasets/derived/facebook_tiny`
   - `python3 scripts/smoke_test_janusgraph.py --node-id 1`
3. Optional enhancement path:
   - `python3 scripts/load_janusgraph.py --dataset-dir datasets/derived/facebook_full`
   - `python3 scripts/smoke_test_janusgraph.py --node-id 1`
   - Use `benchmarks/facebook_full_probe10.json` only if you want to continue beyond smoke validation
   - Do not treat JanusGraph as part of the primary report matrix
