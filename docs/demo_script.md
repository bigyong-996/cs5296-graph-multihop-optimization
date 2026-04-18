# Demo Script

1. Open with the research question:
   - How do `Neo4j`, `PostgreSQL + closure_3`, and an optional `JanusGraph` path behave on multi-hop social graph queries?
2. Show the local-first environment:
   - `infra/docker-compose.yml`
   - `scripts/prepare_dataset.py`
   - `scripts/run_benchmark.py`
3. Show the tiny smoke path in one minute:
   - `facebook_tiny`
   - `scripts/smoke_test_core_backends.py`
4. Show the first real result:
   - `facebook_full`
   - `results/summary/facebook-full-comparison.csv`
   - `results/summary/facebook-full-p50-latency.png`
5. Show the second real result:
   - `twitter_top10000`
   - `results/summary/twitter-top10000-comparison.csv`
   - `results/summary/twitter-top10000-p50-latency.png`
6. Explain the key interpretation:
   - `PostgreSQL + closure_3` is very strong on `facebook_full`
   - `Neo4j` becomes stronger on `twitter_top10000` for `neighbors` and `common_neighbors`
   - `shortest_path` remains fastest on `PostgreSQL`
7. State the caveat explicitly:
   - This compares `PostgreSQL + closure_3` against `Neo4j` online traversal
8. Close with the secondary JanusGraph path and the partitioning extension:
   - JanusGraph remains a secondary enhancement path
   - `hash` vs `locality-aware` partitioning is included as a lightweight research extension
