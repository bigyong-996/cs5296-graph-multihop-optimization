# Group 15 Project Proposal

**Subject:** Scalable Multi-Hop Query Optimization for Large-Scale Social Graphs on Cloud-Native Graph Databases

**Nature of Project:** Research

**Group Project (Group ID: 15)**

**Project Members:** [Name 1 (ID)], [Name 2 (ID)], [Name 3 (ID)]

---

## 1. Subject Summary

Multi-hop relationship queries (e.g., Friends-of-Friends, common connections within three degrees) are fundamental operations in social network analysis, yet they pose significant scalability challenges when the graph exceeds single-node memory limits. This project investigates cloud-native solutions for optimizing such queries by benchmarking distributed graph databases against traditional relational approaches. We aim to identify optimal storage architectures and partitioning strategies that minimize query latency while maximizing throughput for billion-scale social graphs.

Our research will compare Neo4j (deployed on EC2), JanusGraph with distributed backends, and Amazon RDS (using closure table patterns) to evaluate their performance characteristics under realistic social network workloads. The findings will provide actionable insights for practitioners selecting graph storage solutions in cloud environments.

**Relevant Website Links:**

- Neo4j: https://neo4j.com/
- JanusGraph: https://janusgraph.org/
- SNAP Datasets: https://snap.stanford.edu/data/

---

## 2. Dataset Acquisition

To ensure reproducibility and avoid legal concerns associated with web scraping, we will utilize publicly available social network datasets from the Stanford Network Analysis Project (SNAP):

| Dataset | Nodes | Edges | Description |
|---------|-------|-------|-------------|
| Facebook (ego-networks) | 4,039 | 88,234 | Facebook friend lists |
| Twitter (social circles) | 81,306 | 1,768,149 | Twitter follower graph |
| LiveJournal | 4,847,571 | 68,993,773 | Large-scale social network |
| Pokec | 1,632,803 | 30,622,564 | Slovak social network |

We will conduct experiments across multiple dataset scales to evaluate how each solution performs as the graph size increases. The largest dataset (LiveJournal, ~69M edges) will stress-test the distributed capabilities of each platform.

---

## 3. Project Methodology and Objectives

Our technical approach centers on deploying and benchmarking graph storage solutions within the AWS ecosystem. We will deploy Neo4j Community Edition on Amazon EC2 instances (t3.large or m5.large) to evaluate single-node performance, and JanusGraph with Cassandra backend to assess distributed query execution. As a baseline, we will implement a closure table schema in Amazon RDS (PostgreSQL) to compare native graph databases against relational alternatives.

The benchmarking framework will evaluate the following query patterns:

- **1-hop queries:** Direct friend retrieval
- **2-hop queries:** Friends-of-friends enumeration
- **3-hop queries:** Three-degree connection discovery
- **Common friends:** Identifying shared connections between two users
- **Shortest path:** Finding the minimum degree of separation

Performance will be quantified using query latency (p50, p95, p99), throughput (queries per second), and resource utilization (CPU, memory, I/O). We will also investigate the impact of different partitioning strategies (e.g., hash-based vs. relationship-type-based) on query performance.

To contribute novel insights beyond pure benchmarking, we propose to design and evaluate a **locality-aware partitioning heuristic** that co-locates densely connected user clusters, potentially reducing cross-partition traversals for multi-hop queries.

All source code, deployment scripts, and benchmarking results will be maintained in a public GitHub repository with a transparent commit history reflecting our collaborative development process.
