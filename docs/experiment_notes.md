# Experiment Notes

## Scope

This repository now has two primary report-ready benchmark paths:

- `facebook_full` on `Neo4j + PostgreSQL`
- `twitter_top10000` on `Neo4j + PostgreSQL`

JanusGraph remains a secondary enhancement path and is not part of the primary comparison matrix.

## Dataset Matrix

| Dataset | Nodes | Directed edges | Closure rows | Status |
| --- | ---: | ---: | ---: | --- |
| `facebook_full` | 4,039 | 176,468 | 6,874,481 | Main benchmark complete |
| `twitter_top10000` | 10,000 | 829,032 | 74,833,209 | Main benchmark complete |
| `facebook_tiny` | 4 | 8 | small | Tiny smoke path complete |

## Main Findings

### Facebook

`facebook_full` favors `PostgreSQL + closure_3`.

| Backend | Query | p50 ms | p95 ms | p99 ms |
| --- | --- | ---: | ---: | ---: |
| Neo4j | common_neighbors | 0.513 | 0.999 | 1.231 |
| Neo4j | neighbors | 2.059 | 17.063 | 20.191 |
| Neo4j | shortest_path | 0.550 | 0.929 | 1.061 |
| PostgreSQL | common_neighbors | 0.332 | 0.744 | 1.029 |
| PostgreSQL | neighbors | 0.295 | 0.416 | 0.513 |
| PostgreSQL | shortest_path | 0.174 | 0.306 | 0.530 |

### Twitter

`twitter_top10000` changes the balance.

| Backend | Query | p50 ms | p95 ms | p99 ms |
| --- | --- | ---: | ---: | ---: |
| Neo4j | common_neighbors | 0.435 | 0.798 | 1.259 |
| Neo4j | neighbors | 2.556 | 88.687 | 120.082 |
| Neo4j | shortest_path | 0.440 | 0.760 | 1.038 |
| PostgreSQL | common_neighbors | 74.680 | 79.140 | 91.636 |
| PostgreSQL | neighbors | 57.685 | 66.315 | 84.737 |
| PostgreSQL | shortest_path | 0.206 | 0.281 | 0.304 |

## Report-Safe Claims

The following claims are supported by the current artifact:

1. `facebook_full` favors `PostgreSQL + closure_3` across all three query families.
2. `twitter_top10000` favors `Neo4j` on `neighbors` and `common_neighbors`, while `PostgreSQL` remains strongest on `shortest_path`.
3. Query behavior depends strongly on whether the workload benefits from precomputed bounded reachability or from online graph traversal on a denser subgraph.

## Caveat

The primary caveat must be stated explicitly in the report:

- this is `PostgreSQL + closure_3`
- versus `Neo4j` online traversal

So the artifact compares a relational baseline with bounded precomputation against a graph database with online traversal. This is a valid systems comparison, but not a pure apples-to-apples engine comparison.

## JanusGraph Status

JanusGraph is intentionally treated as a secondary enhancement path.

- tiny benchmark path: complete
- full-data smoke validation on `facebook_full`: complete
- full benchmark path: downgraded
- `facebook_full_probe10` benchmark attempt: started, but only the initial `neighbors` cases completed within an acceptable time window

Reason for downgrade:

- the first `facebook_full` import path exposed unstable full-scan behavior
- a later cleanup/import attempt hit a Gremlin evaluation timeout on `g.V().drop().iterate()`
- the repository now includes a more stable internal-vertex-id edge loading path, which is sufficient for full-data smoke validation
- a later `probe10` attempt on `facebook_full` stalled after the initial `neighbors` cases, so the backend was kept out of the primary benchmark matrix
- JanusGraph is still not used as part of the main matrix

The final write-up should present JanusGraph as:

- a validated secondary path
- a path with completed full-data smoke validation on `facebook_full`
- not a blocker for the primary conclusion
- not part of the primary two-backend comparison figures
