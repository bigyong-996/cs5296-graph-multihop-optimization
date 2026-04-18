# Report Scaffold Notes

> This file is a writing scaffold and evidence pack, not a submit-ready report.  
> Use it to draft your own final report in your own words.

## 1. Title And Authorship

Suggested working title:

`Scalable Multi-Hop Query Evaluation on Social Graphs with Neo4j, PostgreSQL, and a JanusGraph Validation Path`

Author block checklist:

- Group ID
- Member names
- Student IDs
- Course name: `CS5296 Cloud Computing`

## 2. Abstract Notes

Target:

- fewer than `250` words
- one paragraph
- no detailed numbers beyond 2-4 headline facts

Must cover:

- problem: multi-hop queries on social graphs
- systems compared: `Neo4j`, `PostgreSQL + closure_3`
- datasets: `facebook_full`, `twitter_top10000`
- key finding:
  - `facebook_full` favors `PostgreSQL + closure_3`
  - `twitter_top10000` favors `Neo4j` on `neighbors` and `common_neighbors`
- JanusGraph positioning:
  - validation/enhancement path only

Do not write it like marketing copy. Keep it factual and compact.

## 3. Introduction Notes

Paragraph 1:

- introduce social graph queries
- mention examples:
  - 1-hop neighbors
  - 2-hop / 3-hop reachability
  - common neighbors
  - shortest path
- explain why these queries matter for social analysis and recommendation-style workloads

Paragraph 2:

- explain the systems question:
  - graph database traversal vs relational precomputation
- frame this as a cloud/data systems decision problem
- mention that a single result on one dataset is not enough because graph density and workload shape matter

Paragraph 3:

- summarize your methodology:
  - reproducible local benchmark artifact
  - `Neo4j` and `PostgreSQL` as primary systems
  - `JanusGraph` as secondary validation path
  - two real SNAP-based datasets

Paragraph 4:

- summarize the main findings in one sentence each
- end with a clear contributions sentence

Safe contribution framing:

1. A reproducible local-first benchmark artifact for bounded multi-hop graph queries.
2. A comparison of `Neo4j` and `PostgreSQL + closure_3` on `facebook_full` and `twitter_top10000`.
3. A secondary JanusGraph validation path and a lightweight partitioning extension.

## 4. System Design / Method Notes

### 4.1 Overall Pipeline

Explain this flow:

1. download SNAP raw edge list
2. canonicalize into `nodes.csv`, `edges.csv`, `metadata.json`
3. generate `closure_3.csv` for bounded relational queries
4. generate deterministic benchmark workload JSON
5. import into each backend
6. run warmup + measured benchmark loops
7. aggregate into summary CSV and PNG plots

Mention concrete repo entrypoints:

- [scripts/prepare_dataset.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/prepare_dataset.py)
- [scripts/run_benchmark.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/run_benchmark.py)
- [scripts/aggregate_results.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/aggregate_results.py)

### 4.2 Backend Design

For `Neo4j`:

- online traversal queries
- graph-native representation
- multi-hop logic expressed directly in traversal query form

For `PostgreSQL`:

- relational representation with `users`, `edges`, `closure_3`
- bounded 3-hop precomputation
- very strong when query pattern aligns with precomputed reachability

For `JanusGraph`:

- not part of the main matrix
- kept as a validation/enhancement path

### 4.3 Workload Definition

State the five query families:

- `1-hop neighbors`
- `2-hop neighbors`
- `3-hop neighbors`
- `common neighbors`
- `shortest path up to 3`

State benchmark execution settings:

- `warmup_count = 2`
- `measured_count = 5`
- `125` workload cases per dataset
- `625` measured rows per backend per dataset

## 5. Experimental Setup Notes

### 5.1 Datasets

Use this table:

| Dataset | Nodes | Directed edges | Closure rows | Role |
| --- | ---: | ---: | ---: | --- |
| `facebook_full` | 4,039 | 176,468 | 6,874,481 | Primary benchmark |
| `twitter_top10000` | 10,000 | 829,032 | 74,833,209 | Primary benchmark |
| `facebook_tiny` | 4 | 8 | small | Smoke validation |

Important wording:

- `edges.csv` is symmetrized for undirected social graph semantics
- `closure_3` is bounded to 3 hops because the benchmark stops at 3 hops

### 5.2 Environment

Mention:

- Docker-based local environment
- `Neo4j`, `PostgreSQL`, `Cassandra`, `JanusGraph`
- reproducible scripts and local runbook

You do not need to oversell this as cloud deployment in the final report if the actual evidence is local-first.

## 6. Results Notes

### 6.1 Facebook Results

Use [results/summary/facebook-full-comparison.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-comparison.csv) and [facebook-full-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-p50-latency.png).

Key facts:

- `PostgreSQL` wins across all three query families on `facebook_full`
- strongest gap appears in `neighbors`

Use these numbers:

| Backend | Query | p50 ms | p95 ms | p99 ms |
| --- | --- | ---: | ---: | ---: |
| Neo4j | common_neighbors | 0.513 | 0.999 | 1.231 |
| Neo4j | neighbors | 2.059 | 17.063 | 20.191 |
| Neo4j | shortest_path | 0.550 | 0.929 | 1.061 |
| PostgreSQL | common_neighbors | 0.332 | 0.744 | 1.029 |
| PostgreSQL | neighbors | 0.295 | 0.416 | 0.513 |
| PostgreSQL | shortest_path | 0.174 | 0.306 | 0.530 |

Interpretation prompts:

- why does bounded closure help here?
- why might the smaller Facebook graph favor precomputation?
- why is shortest path still strong for `PostgreSQL` under bounded depth?

### 6.2 Twitter Results

Use [results/summary/twitter-top10000-comparison.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-comparison.csv) and [twitter-top10000-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-p50-latency.png).

Key facts:

- `Neo4j` wins on `neighbors` and `common_neighbors`
- `PostgreSQL` remains strongest on `shortest_path`

Use these numbers:

| Backend | Query | p50 ms | p95 ms | p99 ms |
| --- | --- | ---: | ---: | ---: |
| Neo4j | common_neighbors | 0.435 | 0.798 | 1.259 |
| Neo4j | neighbors | 2.556 | 88.687 | 120.082 |
| Neo4j | shortest_path | 0.440 | 0.760 | 1.038 |
| PostgreSQL | common_neighbors | 74.680 | 79.140 | 91.636 |
| PostgreSQL | neighbors | 57.685 | 66.315 | 84.737 |
| PostgreSQL | shortest_path | 0.206 | 0.281 | 0.304 |

Interpretation prompts:

- why does the denser `twitter_top10000` subgraph shift the balance?
- why might closure tables become expensive for broad neighborhood-style queries?
- why does bounded shortest path still stay favorable to `PostgreSQL`?

### 6.3 Cross-Dataset Discussion

This should be one of the strongest sections in the report.

Safe claims you can support:

1. Backend preference is workload- and dataset-dependent.
2. Precomputation can dominate on smaller graphs with bounded reachability queries.
3. Online graph traversal can become more competitive, or clearly superior, when neighborhood-style queries dominate on denser subgraphs.

## 7. Caveat Notes

This caveat must be explicit:

- the comparison is `PostgreSQL + closure_3`
- versus `Neo4j` online traversal

Suggested wording direction:

- This is a systems comparison between two valid implementation strategies for bounded multi-hop queries.
- It should not be over-claimed as a pure engine-only benchmark.

## 8. JanusGraph Notes

How to describe it safely:

- tiny benchmark path completed
- `facebook_full` full-data smoke validation completed
- full benchmark matrix intentionally downgraded

Reasoning you can use:

- JanusGraph worked as a validation/enhancement path
- it did not reach the same stability level as the primary two-backend matrix for report-grade benchmarking
- therefore it was kept out of the main figure set

Do not present JanusGraph as a failed system. Present it as a secondary path that was not prioritized into the final matrix.

## 9. Conclusion Notes

Target:

- `3-4` sentences
- no new claims

Must say:

- what was compared
- what the main empirical pattern was
- why the result matters
- what remained secondary / future work

## 10. References Checklist

You should add real citations for:

- SNAP dataset site
- Neo4j official website/docs
- JanusGraph official website/docs
- PostgreSQL official docs
- any graph query / closure table / social graph background sources you cite

Use IEEE style as required by the course brief.

## 11. Figure Placement Notes

Recommended report figure set:

1. One pipeline/system overview figure or table
2. One Facebook latency comparison figure
3. One Twitter latency comparison figure
4. Optional small table summarizing dataset sizes

Avoid too many redundant charts. Two strong comparison figures are enough for a first draft.

## 12. Writing Checklist

Before finalizing your own report:

- make sure every section is written by you in your own words
- keep the story consistent with the actual artifact
- do not claim JanusGraph is part of the main benchmark matrix
- do not hide the `PostgreSQL + closure_3` caveat
- make sure figure captions explain the takeaway, not just the file content
