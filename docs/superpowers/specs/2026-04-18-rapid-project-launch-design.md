# Rapid Project Launch Design

Date: 2026-04-18
Project: CS5296 Graph Multi-Hop Optimization
Status: Approved design draft for implementation planning

## 1. Context

This repository is currently at a documentation stage. It already contains the course brief, proposal, and an action guide, but it does not yet contain implementation code, reproducible experiment scripts, or artifact-ready project structure.

The course deliverables are due on 2026-04-24. As of 2026-04-18, the team has 6 days left. The goal is not to minimize scope, but to complete a high-quality research-style course project by using strong task decomposition, parallel execution across three members, and AI-assisted development.

The team has selected the following working assumptions:

- Target outcome: a solid high-scoring submission rather than a minimal pass
- Execution style: local-first development and validation
- Platform priority:
  - Primary comparison: Neo4j and a PostgreSQL closure-table baseline developed locally and kept compatible with later RDS-style deployment
  - Secondary comparison: JanusGraph as a meaningful but non-blocking enhancement
- Delivery principle: optimize for completed coursework, reproducibility, and credible comparative results
- Innovation strategy: keep locality-aware partitioning as a light extension if the main benchmark baseline stabilizes early

## 2. Project Objective

The project should produce a research artifact that answers the question:

How do different cloud-oriented graph storage approaches behave for multi-hop social graph queries under a unified benchmark protocol, and what practical guidance can be drawn for storage and partitioning decisions?

The project should be considered successful if it delivers all of the following:

- A reproducible repository structure suitable for the software artifact appendix
- Working data preparation and import flows for at least Neo4j and PostgreSQL closure-table modeling
- A shared benchmark runner and result format
- Report-ready comparative results for Neo4j vs PostgreSQL on common multi-hop workloads
- A verified JanusGraph path that reaches at least deployment plus basic query validation, with benchmark coverage if time allows
- Supporting materials for the final report and demo video

## 3. Recommended Delivery Model

The project will use a dual-track parallel execution model.

Track A focuses on getting the main comparison working end-to-end:

- SNAP dataset acquisition
- canonical graph conversion
- Neo4j import and query execution
- PostgreSQL closure-table import and query execution
- unified benchmark execution
- result aggregation for the report

Track B focuses on project depth and presentation strength:

- JanusGraph environment setup
- minimal import and query validation
- partial benchmark integration if feasible
- artifact documentation
- report figures, notes, appendix content, and demo support

This model is preferred over a purely research-driven or purely deliverable-driven start because it balances score potential with deadline safety. It lets the team make immediate progress on the two primary systems while still preserving a research-oriented third platform and structured documentation.

## 4. System Architecture

This repository should be treated as a research experiment workspace rather than a single software application. The implementation should be organized into five cooperating modules.

### 4.1 Data Pipeline

Purpose:

- download SNAP datasets
- normalize graph input into one canonical internal format
- generate backend-specific import assets

Core outputs:

- `nodes.csv`
- `edges.csv`
- dataset metadata such as node count, edge count, directedness, and generation parameters

Design rule:

All database backends should import from the same canonical source representation so that benchmark results remain comparable.

### 4.2 Database Adapters

Each backend should have an isolated adapter layer:

- `adapters/neo4j/`
- `adapters/rds/`
- `adapters/janusgraph/`

Each adapter is responsible for:

- environment notes
- schema or graph model setup
- import logic
- standardized query implementations

Each adapter should not own benchmark logic. It should only expose the operations needed by the benchmark runner.

### 4.3 Benchmark Runner

The benchmark runner should define:

- workload types
- warmup and measured rounds
- concurrency settings
- timeout settings
- output schema

The benchmark runner should call backend adapters through a unified interface so that the same logical workload can be executed against multiple systems with minimal drift.

### 4.4 Analysis and Reporting

This module should transform raw benchmark results into:

- summary tables
- latency statistics
- charts for the report
- concise experiment notes for the artifact appendix and demo

The purpose is to avoid a last-minute manual data-wrangling phase.

### 4.5 Docs and Artifact Support

This module should store:

- reproducibility instructions
- experiment logs
- report source notes
- artifact appendix drafts
- demo talking points

Documentation should evolve in parallel with code rather than being reconstructed at the end.

## 5. Repository Structure

The recommended initial repository structure is:

```text
datasets/                  dataset instructions, samples, transformed metadata
scripts/                   download, transform, import, benchmark, aggregate entrypoints
adapters/neo4j/            Neo4j setup, import, query implementations
adapters/rds/              PostgreSQL closure-table setup, import, query SQL
adapters/janusgraph/       JanusGraph setup and minimal validation flows
benchmarks/                workload definitions and benchmark configuration
results/                   raw outputs, summaries, chart-ready data
docs/                      artifact appendix drafts, experiment notes, demo materials
docs/superpowers/specs/    design and planning documents
```

This layout is intentionally optimized for three-person parallel work:

- one member can focus on Neo4j
- one member can focus on PostgreSQL
- one member can focus on benchmark orchestration, documentation, and JanusGraph support

It also supports clear artifact packaging because the project structure reflects the final deliverables from the beginning.

## 6. Data Flow and Experiment Protocol

To keep results comparable across systems, the project should follow one fixed data flow:

1. Acquire raw SNAP graph data
2. Convert it into a canonical internal representation
3. Generate backend-specific import artifacts from the canonical form
4. Execute shared workloads against each backend
5. Save benchmark outputs in a common result format
6. Aggregate results into report-ready summaries

### 6.1 Canonical Dataset Layer

The canonical layer should include:

- node identifiers
- edge pairs
- dataset metadata
- optional derived subsets for small and medium-scale experiments

All backend-specific transformations should be generated from this layer rather than re-parsing raw files independently.

### 6.2 Workload Set

The benchmark suite should standardize these five query classes:

- 1-hop neighbors
- 2-hop neighbors
- 3-hop neighbors
- common neighbors
- shortest path

For each workload, the benchmark configuration should define:

- input parameter form
- correctness check method
- timeout budget
- warmup count
- measured run count

To reduce backend mismatch, the preferred output contract is:

- neighbor count
- common-neighbor count
- path length or reachability result

Returning full result sets is optional for debugging, but reportable benchmark runs should prefer compact outputs that are easier to compare and validate.

### 6.3 Result Schema

Each benchmark output row should include, at minimum:

- `backend`
- `dataset`
- `query_type`
- `run_id`
- `warmup_count`
- `measured_count`
- `concurrency`
- `timeout_ms`
- `latency_ms`
- `success`
- `result_size`

If system metrics can be captured reliably, the team may also add:

- `cpu_percent`
- `memory_mb`
- `io_read_mb`
- `io_write_mb`

However, system metrics are secondary. The project should not block on them if they introduce too much execution complexity.

## 7. Scope Priorities

The comparison priority is:

1. Neo4j
2. PostgreSQL closure-table baseline
3. JanusGraph

The dataset priority is:

1. Facebook for smoke tests and correctness validation
2. Twitter for the main comparative benchmark
3. Pokec only if the main pipeline is already stable
4. LiveJournal only if resources and time clearly allow it

The project should explicitly avoid trying to maximize platform count and dataset scale at the expense of reliable results for the main comparison.

The locality-aware partitioning idea should be handled as an extension layer after the main benchmark pipeline is trustworthy. It is valuable for the final research narrative, but it should not block the first complete comparative results.

## 8. One-Week Execution Plan

The remaining schedule is:

- 2026-04-18 to 2026-04-19: repository skeleton, data normalization, benchmark interface, initial imports
- 2026-04-20 to 2026-04-21: stabilize Neo4j and PostgreSQL queries, produce first comparable benchmark outputs
- 2026-04-22: JanusGraph validation and partial integration, chart generation, interpretation notes
- 2026-04-23: fill experiment gaps, finalize appendix, prepare and rehearse demo
- 2026-04-24: final packaging and submission only

### 8.1 Suggested Team Split

Member A:

- Neo4j deployment and tuning
- query implementation
- benchmark participation for Neo4j

Member B:

- PostgreSQL closure-table schema and import
- SQL implementation for shared workloads
- benchmark participation for PostgreSQL

Member C:

- benchmark runner and result schema
- JanusGraph setup and minimum validation
- artifact appendix, experiment notes, report support, and demo structure

### 8.2 Coordination Rule

All members should work against shared benchmark definitions and shared dataset conventions. No backend should define its own incompatible workload semantics.

## 9. Risk Management and Fallback Rules

The team should adopt explicit fallback rules at the beginning of implementation.

### 9.1 JanusGraph Fallback

If JanusGraph has not reached stable import plus basic query validation by 2026-04-21, it should be formally downgraded to a secondary demonstration component rather than a full benchmark target.

### 9.2 Large-Dataset Fallback

If Pokec or larger datasets overwhelm local resources, the main report conclusions should remain based on Facebook and Twitter. Larger datasets may be discussed as exploratory extensions rather than required evidence.

### 9.3 Metrics Fallback

If machine-level monitoring becomes unreliable or expensive to integrate, the benchmark should prioritize:

- latency
- throughput
- success rate

Resource metrics should be treated as optional reinforcement, not a release blocker.

### 9.4 Workload Fallback

If shortest-path support creates major implementation drift across backends, it may be downgraded from a required mainline workload to an advanced optional workload, while the first four workload types remain mandatory.

## 10. Testing and Validation Strategy

The project should validate quality at four levels.

### 10.1 Data Validation

Verify:

- node and edge counts
- duplicate handling
- identifier mapping consistency
- dataset subset generation consistency

### 10.2 Query Correctness

On small datasets, verify that equivalent workloads produce consistent results across the supported backends. Exact result sets are useful during debugging, but compact correctness checks should be enough for benchmark runs.

### 10.3 Import Smoke Tests

Each backend should provide a fast test that proves:

- the service can start
- the schema or graph can be initialized
- a small dataset can be imported
- at least one query can run successfully

### 10.4 Benchmark Sanity Checks

The benchmark system should:

- separate warmup from measured rounds
- record timeouts and failures explicitly
- avoid silently mixing failed runs into summary statistics

## 11. Acceptance Criteria

### 11.1 Project Start Success

The startup phase is considered complete when:

- the repository skeleton exists
- a canonical data pipeline is defined
- Neo4j and PostgreSQL can import a small dataset and run most shared workloads
- the benchmark runner can output results in a common format

### 11.2 Coursework Success

The project is considered ready for course submission when:

- Neo4j and PostgreSQL produce reportable comparative benchmark results
- JanusGraph reaches at least setup plus minimum validation, with partial experiments if feasible
- the artifact appendix can reproduce the main experiment path
- the demo can show at least one complete end-to-end experiment flow

## 12. Out of Scope for the First Implementation Cycle

The following should not block the first execution cycle:

- full-scale locality-aware partition algorithm research implementation beyond a lightweight exploratory extension
- production-grade cloud deployment automation
- very large-scale dataset completion across every backend
- polished visualization beyond what is needed for the report and demo

The first implementation cycle should focus on a credible, reproducible, comparative experiment baseline that can support the final coursework submission.

## 13. Next Step

The next step after this design is to write an implementation plan that converts this architecture into concrete tasks, ownership, command entrypoints, and day-by-day milestones.
