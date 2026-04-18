# Local-First Graph Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible local-first benchmark pipeline that compares Neo4j and PostgreSQL on multi-hop graph workloads, adds a minimum JanusGraph validation path, and produces artifact-ready outputs for the course submission.

**Architecture:** The implementation centers on one Python package, `graph_bench`, that owns canonical dataset preparation, backend adapters, workload generation, benchmark execution, result aggregation, and a lightweight partitioning extension. Local Docker services provide Neo4j, PostgreSQL, Cassandra, and JanusGraph, while small deterministic tests and smoke scripts keep the pipeline verifiable from the first commit onward.

**Tech Stack:** Python 3.12, pytest, Docker Compose, Neo4j, PostgreSQL 16, JanusGraph, Cassandra, pandas, matplotlib, neo4j Python driver, psycopg 3, gremlinpython

---

## Scope Note

This plan stays as a single implementation plan because every subsystem feeds the same benchmark artifact. Neo4j, PostgreSQL, JanusGraph, data preparation, benchmarking, aggregation, and documentation all share one canonical dataset format and one workload contract. They are not independent products.

## Assumptions Locked In

- The canonical graph representation is directed, but undirected source datasets are symmetrized during preparation.
- The PostgreSQL baseline uses a bounded closure table capped at depth `3`, because the benchmarked multi-hop workloads stop at `3` hops.
- The formal local benchmark datasets are:
  - `facebook_full`
  - `twitter_top10000`
- The benchmarked workload contract is:
  - `1-hop neighbors`
  - `2-hop neighbors`
  - `3-hop neighbors`
  - `common neighbors`
  - `shortest path up to 3`
- The lightweight research extension compares `hash` partitioning vs `locality-aware` partitioning on the canonical graph, not on a distributed graph database cluster.

## File Structure Map

### Project and Environment

- `pyproject.toml`
  - Python package metadata and dependencies
- `.env.example`
  - Local service connection defaults
- `infra/docker-compose.yml`
  - Local containers for Neo4j, PostgreSQL, Cassandra, and JanusGraph
- `README.md`
  - Quickstart and run order

### Python Package

- `src/graph_bench/__init__.py`
  - Package version
- `src/graph_bench/models.py`
  - Shared dataclasses for datasets, workload cases, and benchmark results
- `src/graph_bench/config.py`
  - Environment-backed settings loader
- `src/graph_bench/canonical.py`
  - Raw SNAP parsing, symmetrization, and top-degree induced sampling
- `src/graph_bench/closure.py`
  - Bounded closure generation up to depth 3
- `src/graph_bench/workloads.py`
  - Deterministic workload case generation
- `src/graph_bench/results.py`
  - Result serialization helpers
- `src/graph_bench/benchmark_runner.py`
  - Warmup, measured runs, and JSONL emission
- `src/graph_bench/partitioning.py`
  - Hash and locality-aware partitioning heuristics
- `src/graph_bench/adapters/base.py`
  - Shared backend protocol
- `src/graph_bench/adapters/neo4j_adapter.py`
  - Neo4j query adapter
- `src/graph_bench/adapters/postgres_adapter.py`
  - PostgreSQL query adapter
- `src/graph_bench/adapters/janusgraph_adapter.py`
  - JanusGraph query adapter

### Scripts

- `scripts/prepare_dataset.py`
  - Raw SNAP to canonical CSV/JSON export
- `scripts/load_neo4j.py`
  - Canonical CSV import into Neo4j
- `scripts/load_postgres.py`
  - Canonical CSV and bounded closure import into PostgreSQL
- `scripts/load_janusgraph.py`
  - Canonical CSV import into JanusGraph
- `scripts/run_benchmark.py`
  - Execute a workload file against one backend
- `scripts/aggregate_results.py`
  - JSONL to summary CSV table
- `scripts/plot_results.py`
  - Summary CSV to PNG chart
- `scripts/smoke_test_core_backends.py`
  - Quick Neo4j and PostgreSQL verification
- `scripts/smoke_test_janusgraph.py`
  - Quick JanusGraph verification
- `scripts/evaluate_partitioning.py`
  - Hash vs locality-aware edge-cut evaluation

### Tests

- `tests/test_package_smoke.py`
- `tests/test_canonical_dataset.py`
- `tests/test_config.py`
- `tests/test_closure.py`
- `tests/test_prepare_dataset_script.py`
- `tests/test_benchmark_runner.py`
- `tests/test_aggregate_results.py`
- `tests/test_smoke_script.py`
- `tests/test_docs_smoke.py`
- `tests/test_partitioning.py`
- `tests/adapters/test_neo4j_adapter.py`
- `tests/adapters/test_postgres_adapter.py`
- `tests/adapters/test_janusgraph_adapter.py`
- `tests/fixtures/raw/facebook_tiny.txt`

### Docs

- `docs/runbook.md`
- `docs/artifact_appendix.md`
- `docs/demo_script.md`

## Task 1: Bootstrap the Python Workspace

**Files:**
- Create: `pyproject.toml`
- Create: `src/graph_bench/__init__.py`
- Create: `tests/test_package_smoke.py`

- [ ] **Step 1: Write the failing package smoke test**

```python
# tests/test_package_smoke.py
from graph_bench import __version__


def test_package_exposes_version() -> None:
    assert __version__ == "0.1.0"
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m pytest tests/test_package_smoke.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench'`

- [ ] **Step 3: Add package metadata and the package entrypoint**

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "graph-bench"
version = "0.1.0"
description = "Local-first graph benchmark toolkit for CS5296"
requires-python = ">=3.12"
dependencies = [
  "neo4j>=5.20",
  "psycopg[binary]>=3.1",
  "gremlinpython>=3.7",
  "pandas>=2.2",
  "matplotlib>=3.9",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.2",
]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
markers = [
  "integration: requires local containers",
]

[tool.setuptools.packages.find]
where = ["src"]
```

```python
# src/graph_bench/__init__.py
__version__ = "0.1.0"
```

- [ ] **Step 4: Run the smoke test again**

Run: `python -m pytest tests/test_package_smoke.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the bootstrap**

```bash
git add pyproject.toml src/graph_bench/__init__.py tests/test_package_smoke.py
git commit -m "chore: bootstrap graph benchmark package"
```

## Task 2: Build the Canonical Dataset Pipeline

**Files:**
- Create: `src/graph_bench/models.py`
- Create: `src/graph_bench/canonical.py`
- Create: `tests/fixtures/raw/facebook_tiny.txt`
- Create: `tests/test_canonical_dataset.py`

- [ ] **Step 1: Write a failing canonical dataset test and fixture**

```text
# tests/fixtures/raw/facebook_tiny.txt
1 2
2 3
3 1
3 4
```

```python
# tests/test_canonical_dataset.py
from pathlib import Path

from graph_bench.canonical import read_edge_list, top_degree_subgraph


def test_read_edge_list_symmetrizes_undirected_graph() -> None:
    dataset = read_edge_list(
        Path("tests/fixtures/raw/facebook_tiny.txt"),
        dataset_name="facebook_tiny",
        directed=False,
        symmetrize=True,
    )

    assert dataset.metadata.dataset_name == "facebook_tiny"
    assert dataset.metadata.node_count == 4
    assert (1, 2) in dataset.edges
    assert (2, 1) in dataset.edges
    assert (4, 3) in dataset.edges


def test_top_degree_subgraph_keeps_highest_degree_nodes() -> None:
    dataset = read_edge_list(
        Path("tests/fixtures/raw/facebook_tiny.txt"),
        dataset_name="facebook_tiny",
        directed=False,
        symmetrize=True,
    )

    sampled = top_degree_subgraph(dataset, max_nodes=3, sampled_name="facebook_top3")

    assert sampled.metadata.dataset_name == "facebook_top3"
    assert sampled.nodes == {1, 2, 3}
    assert (3, 4) not in sampled.edges
```

- [ ] **Step 2: Run the dataset tests to verify they fail**

Run: `python -m pytest tests/test_canonical_dataset.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.canonical'`

- [ ] **Step 3: Implement the shared dataset models and canonical parsing**

```python
# src/graph_bench/models.py
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class GraphMetadata:
    dataset_name: str
    directed: bool
    node_count: int
    edge_count: int

    def to_json(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")


@dataclass(frozen=True)
class GraphDataset:
    metadata: GraphMetadata
    nodes: set[int]
    edges: set[tuple[int, int]]
```

```python
# src/graph_bench/canonical.py
from __future__ import annotations

from collections import Counter
from pathlib import Path
import csv

from graph_bench.models import GraphDataset, GraphMetadata


def read_edge_list(
    path: Path,
    *,
    dataset_name: str,
    directed: bool,
    symmetrize: bool,
) -> GraphDataset:
    nodes: set[int] = set()
    edges: set[tuple[int, int]] = set()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        left_text, right_text = line.split()
        left, right = int(left_text), int(right_text)
        nodes.update({left, right})
        edges.add((left, right))
        if symmetrize and left != right:
            edges.add((right, left))

    metadata = GraphMetadata(
        dataset_name=dataset_name,
        directed=directed and not symmetrize,
        node_count=len(nodes),
        edge_count=len(edges),
    )
    return GraphDataset(metadata=metadata, nodes=nodes, edges=edges)


def top_degree_subgraph(
    dataset: GraphDataset,
    *,
    max_nodes: int,
    sampled_name: str,
) -> GraphDataset:
    degrees: Counter[int] = Counter()
    for left, right in dataset.edges:
        degrees[left] += 1
        degrees[right] += 1

    chosen_nodes = {
        node_id
        for node_id, _ in sorted(
            degrees.items(),
            key=lambda item: (-item[1], item[0]),
        )[:max_nodes]
    }
    sampled_edges = {
        (left, right)
        for left, right in dataset.edges
        if left in chosen_nodes and right in chosen_nodes
    }
    metadata = GraphMetadata(
        dataset_name=sampled_name,
        directed=dataset.metadata.directed,
        node_count=len(chosen_nodes),
        edge_count=len(sampled_edges),
    )
    return GraphDataset(metadata=metadata, nodes=chosen_nodes, edges=sampled_edges)


def write_canonical_dataset(dataset: GraphDataset, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "nodes.csv").open("w", encoding="utf-8", newline="") as node_file:
        writer = csv.writer(node_file)
        writer.writerow(["node_id"])
        for node_id in sorted(dataset.nodes):
            writer.writerow([node_id])

    with (output_dir / "edges.csv").open("w", encoding="utf-8", newline="") as edge_file:
        writer = csv.writer(edge_file)
        writer.writerow(["src", "dst"])
        for src, dst in sorted(dataset.edges):
            writer.writerow([src, dst])

    dataset.metadata.to_json(output_dir / "metadata.json")
```

- [ ] **Step 4: Run the dataset tests again**

Run: `python -m pytest tests/test_canonical_dataset.py -q`
Expected: PASS with `2 passed`

- [ ] **Step 5: Commit the canonical dataset layer**

```bash
git add src/graph_bench/models.py src/graph_bench/canonical.py tests/fixtures/raw/facebook_tiny.txt tests/test_canonical_dataset.py
git commit -m "feat: add canonical dataset preparation layer"
```

## Task 3: Add Local Configuration and Docker Services

**Files:**
- Create: `.env.example`
- Create: `infra/docker-compose.yml`
- Create: `src/graph_bench/config.py`
- Create: `tests/test_config.py`

- [ ] **Step 1: Write a failing config test**

```python
# tests/test_config.py
from graph_bench.config import load_settings


def test_load_settings_uses_local_defaults() -> None:
    settings = load_settings()

    assert settings.neo4j_uri == "bolt://localhost:7687"
    assert settings.postgres_dsn == "postgresql://postgres:postgres@localhost:5432/graphbench"
    assert settings.janusgraph_url == "ws://localhost:8182/gremlin"
```

- [ ] **Step 2: Run the config test to verify it fails**

Run: `python -m pytest tests/test_config.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.config'`

- [ ] **Step 3: Implement settings loading and local container definitions**

```python
# src/graph_bench/config.py
from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    postgres_dsn: str
    janusgraph_url: str


def load_settings() -> Settings:
    return Settings(
        neo4j_uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_user=os.getenv("NEO4J_USER", "neo4j"),
        neo4j_password=os.getenv("NEO4J_PASSWORD", "password"),
        postgres_dsn=os.getenv(
            "POSTGRES_DSN",
            "postgresql://postgres:postgres@localhost:5432/graphbench",
        ),
        janusgraph_url=os.getenv("JANUSGRAPH_URL", "ws://localhost:8182/gremlin"),
    )
```

```dotenv
# .env.example
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
POSTGRES_DSN=postgresql://postgres:postgres@localhost:5432/graphbench
JANUSGRAPH_URL=ws://localhost:8182/gremlin
```

```yaml
# infra/docker-compose.yml
services:
  neo4j:
    image: neo4j:5.20
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/password
    volumes:
      - neo4j-data:/data

  postgres:
    image: postgres:16
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: graphbench
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres-data:/var/lib/postgresql/data

  cassandra:
    image: cassandra:4.1
    profiles: ["janusgraph"]
    ports:
      - "9042:9042"
    volumes:
      - cassandra-data:/var/lib/cassandra

  janusgraph:
    image: janusgraph/janusgraph:1.0.0
    profiles: ["janusgraph"]
    depends_on:
      - cassandra
    ports:
      - "8182:8182"
    environment:
      JANUS_PROPS_TEMPLATE: cql-es
      storage.backend: cql
      storage.hostname: cassandra

volumes:
  neo4j-data:
  postgres-data:
  cassandra-data:
```

- [ ] **Step 4: Run the config test and validate the compose file**

Run: `python -m pytest tests/test_config.py -q`
Expected: PASS with `1 passed`

Run: `docker compose -f infra/docker-compose.yml config > /tmp/graph-bench-compose.txt`
Expected: command exits `0` and `/tmp/graph-bench-compose.txt` contains `neo4j`, `postgres`, `cassandra`, and `janusgraph`

- [ ] **Step 5: Commit the local environment setup**

```bash
git add .env.example infra/docker-compose.yml src/graph_bench/config.py tests/test_config.py
git commit -m "chore: add local service configuration"
```

## Task 4: Implement Bounded Closure Generation

**Files:**
- Create: `src/graph_bench/closure.py`
- Create: `tests/test_closure.py`

- [ ] **Step 1: Write a failing bounded closure test**

```python
# tests/test_closure.py
from graph_bench.closure import build_bounded_closure
from graph_bench.models import GraphDataset, GraphMetadata


def test_build_bounded_closure_stops_at_depth_three() -> None:
    dataset = GraphDataset(
        metadata=GraphMetadata(
            dataset_name="chain",
            directed=False,
            node_count=5,
            edge_count=8,
        ),
        nodes={1, 2, 3, 4, 5},
        edges={
            (1, 2), (2, 1),
            (2, 3), (3, 2),
            (3, 4), (4, 3),
            (4, 5), (5, 4),
        },
    )

    rows = build_bounded_closure(dataset, max_depth=3)

    assert (1, 4, 3) in rows
    assert (1, 5, 4) not in rows
```

- [ ] **Step 2: Run the closure test to verify it fails**

Run: `python -m pytest tests/test_closure.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.closure'`

- [ ] **Step 3: Implement bounded breadth-first closure generation**

```python
# src/graph_bench/closure.py
from __future__ import annotations

from collections import deque

from graph_bench.models import GraphDataset


def build_bounded_closure(
    dataset: GraphDataset,
    *,
    max_depth: int,
) -> set[tuple[int, int, int]]:
    adjacency: dict[int, set[int]] = {node_id: set() for node_id in dataset.nodes}
    for src, dst in dataset.edges:
        adjacency.setdefault(src, set()).add(dst)

    closure_rows: set[tuple[int, int, int]] = set()
    for source in sorted(dataset.nodes):
        queue = deque([(source, 0)])
        seen_depth: dict[int, int] = {source: 0}
        while queue:
            current, depth = queue.popleft()
            if depth == max_depth:
                continue
            for neighbor in sorted(adjacency.get(current, set())):
                next_depth = depth + 1
                if neighbor not in seen_depth or next_depth < seen_depth[neighbor]:
                    seen_depth[neighbor] = next_depth
                    queue.append((neighbor, next_depth))
                    if neighbor != source:
                        closure_rows.add((source, neighbor, next_depth))
    return closure_rows
```

- [ ] **Step 4: Run the closure test again**

Run: `python -m pytest tests/test_closure.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the closure builder**

```bash
git add src/graph_bench/closure.py tests/test_closure.py
git commit -m "feat: add bounded closure generation"
```

## Task 5: Implement the Neo4j Query Adapter

**Files:**
- Create: `src/graph_bench/adapters/base.py`
- Create: `src/graph_bench/adapters/neo4j_adapter.py`
- Create: `tests/adapters/test_neo4j_adapter.py`

- [ ] **Step 1: Write a failing Neo4j adapter test**

```python
# tests/adapters/test_neo4j_adapter.py
from graph_bench.adapters.neo4j_adapter import Neo4jAdapter


class FakeResult:
    def __init__(self, value):
        self._value = value

    def single(self):
        return {"value": self._value}


class FakeSession:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def run(self, query, **params):
        self.calls.append((query, params))
        return FakeResult(self.values.pop(0))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeDriver:
    def __init__(self, values):
        self.session_obj = FakeSession(values)

    def session(self):
        return self.session_obj


def test_neighbor_count_uses_bounded_relationship_length() -> None:
    driver = FakeDriver([5])
    adapter = Neo4jAdapter(driver)

    result = adapter.neighbor_count(node_id=1, hops=2)

    assert result == 5
    query, params = driver.session_obj.calls[0]
    assert "*1..2" in query
    assert params == {"node_id": 1}
```

- [ ] **Step 2: Run the Neo4j adapter test to verify it fails**

Run: `python -m pytest tests/adapters/test_neo4j_adapter.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.adapters.neo4j_adapter'`

- [ ] **Step 3: Implement the shared backend protocol and the Neo4j adapter**

```python
# src/graph_bench/adapters/base.py
from __future__ import annotations

from typing import Protocol


class GraphBackend(Protocol):
    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        ...

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        ...

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        ...
```

```python
# src/graph_bench/adapters/neo4j_adapter.py
from __future__ import annotations


class Neo4jAdapter:
    def __init__(self, driver) -> None:
        self._driver = driver

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        if hops not in {1, 2, 3}:
            raise ValueError("hops must be 1, 2, or 3")
        query = (
            f"MATCH (start:User {{id: $node_id}})-[:LINK*1..{hops}]-(target:User) "
            "WHERE target.id <> $node_id "
            "RETURN count(DISTINCT target) AS value"
        )
        with self._driver.session() as session:
            return int(session.run(query, node_id=node_id).single()["value"])

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        query = (
            "MATCH (left:User {id: $left_id})-[:LINK]-(common:User)-[:LINK]-(right:User {id: $right_id}) "
            "WHERE common.id <> $left_id AND common.id <> $right_id "
            "RETURN count(DISTINCT common) AS value"
        )
        with self._driver.session() as session:
            return int(session.run(query, left_id=left_id, right_id=right_id).single()["value"])

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        query = (
            "MATCH (left:User {id: $left_id}), (right:User {id: $right_id}) "
            "OPTIONAL MATCH p = shortestPath((left)-[:LINK*..3]-(right)) "
            "RETURN CASE WHEN p IS NULL THEN NULL ELSE length(p) END AS value"
        )
        with self._driver.session() as session:
            return session.run(query, left_id=left_id, right_id=right_id).single()["value"]
```

- [ ] **Step 4: Run the Neo4j adapter test again**

Run: `python -m pytest tests/adapters/test_neo4j_adapter.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the Neo4j adapter**

```bash
git add src/graph_bench/adapters/base.py src/graph_bench/adapters/neo4j_adapter.py tests/adapters/test_neo4j_adapter.py
git commit -m "feat: add neo4j benchmark adapter"
```

## Task 6: Implement the PostgreSQL Query Adapter

**Files:**
- Create: `src/graph_bench/adapters/postgres_adapter.py`
- Create: `tests/adapters/test_postgres_adapter.py`

- [ ] **Step 1: Write a failing PostgreSQL adapter test**

```python
# tests/adapters/test_postgres_adapter.py
from graph_bench.adapters.postgres_adapter import PostgresAdapter


class FakeCursor:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def execute(self, query, params):
        self.calls.append((query, params))

    def fetchone(self):
        return {"value": self.values.pop(0)}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self, values):
        self.cursor_obj = FakeCursor(values)

    def cursor(self, row_factory=None):
        return self.cursor_obj


def test_neighbor_count_reads_from_bounded_closure_table() -> None:
    connection = FakeConnection([7])
    adapter = PostgresAdapter(connection)

    result = adapter.neighbor_count(node_id=11, hops=3)

    assert result == 7
    query, params = connection.cursor_obj.calls[0]
    assert "closure_3" in query
    assert params == {"node_id": 11, "max_depth": 3}
```

- [ ] **Step 2: Run the PostgreSQL adapter test to verify it fails**

Run: `python -m pytest tests/adapters/test_postgres_adapter.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.adapters.postgres_adapter'`

- [ ] **Step 3: Implement the PostgreSQL adapter against `closure_3`**

```python
# src/graph_bench/adapters/postgres_adapter.py
from __future__ import annotations


class PostgresAdapter:
    def __init__(self, connection) -> None:
        self._connection = connection

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        query = (
            "SELECT COUNT(DISTINCT dst) AS value "
            "FROM closure_3 "
            "WHERE src = %(node_id)s AND depth <= %(max_depth)s"
        )
        with self._connection.cursor(row_factory=dict) as cursor:
            cursor.execute(query, {"node_id": node_id, "max_depth": hops})
            return int(cursor.fetchone()["value"])

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        query = (
            "SELECT COUNT(*) AS value "
            "FROM ("
            "  SELECT dst FROM closure_3 WHERE src = %(left_id)s AND depth = 1 "
            "  INTERSECT "
            "  SELECT dst FROM closure_3 WHERE src = %(right_id)s AND depth = 1"
            ") AS common_neighbors"
        )
        with self._connection.cursor(row_factory=dict) as cursor:
            cursor.execute(query, {"left_id": left_id, "right_id": right_id})
            return int(cursor.fetchone()["value"])

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        query = (
            "SELECT MIN(depth) AS value "
            "FROM closure_3 "
            "WHERE src = %(left_id)s AND dst = %(right_id)s"
        )
        with self._connection.cursor(row_factory=dict) as cursor:
            cursor.execute(query, {"left_id": left_id, "right_id": right_id})
            return cursor.fetchone()["value"]
```

- [ ] **Step 4: Run the PostgreSQL adapter test again**

Run: `python -m pytest tests/adapters/test_postgres_adapter.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the PostgreSQL adapter**

```bash
git add src/graph_bench/adapters/postgres_adapter.py tests/adapters/test_postgres_adapter.py
git commit -m "feat: add postgres benchmark adapter"
```

## Task 7: Add Dataset Preparation and Backend Load Scripts

**Files:**
- Create: `scripts/prepare_dataset.py`
- Create: `scripts/load_neo4j.py`
- Create: `scripts/load_postgres.py`
- Create: `tests/test_prepare_dataset_script.py`

- [ ] **Step 1: Write a failing script-level test for dataset preparation**

```python
# tests/test_prepare_dataset_script.py
from pathlib import Path
import subprocess
import sys


def test_prepare_dataset_writes_closure_file(tmp_path: Path) -> None:
    output_dir = tmp_path / "facebook_tiny"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/prepare_dataset.py",
            "--input",
            "tests/fixtures/raw/facebook_tiny.txt",
            "--dataset-name",
            "facebook_tiny",
            "--symmetrize",
            "--output-dir",
            str(output_dir),
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert (output_dir / "nodes.csv").exists()
    assert (output_dir / "edges.csv").exists()
    assert (output_dir / "metadata.json").exists()
    assert (output_dir / "closure_3.csv").exists()
```

- [ ] **Step 2: Run the script-level test to verify it fails before the script exists**

Run: `python -m pytest tests/test_prepare_dataset_script.py -q`
Expected: FAIL because `scripts/prepare_dataset.py` does not exist yet and the subprocess returns a non-zero exit code

- [ ] **Step 3: Implement the dataset preparation and load scripts**

```python
# scripts/prepare_dataset.py
from __future__ import annotations

import argparse
from pathlib import Path

from graph_bench.canonical import read_edge_list, top_degree_subgraph, write_canonical_dataset
from graph_bench.closure import build_bounded_closure


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--symmetrize", action="store_true")
    parser.add_argument("--max-nodes", type=int)
    args = parser.parse_args()

    dataset = read_edge_list(
        Path(args.input),
        dataset_name=args.dataset_name,
        directed=not args.symmetrize,
        symmetrize=args.symmetrize,
    )
    if args.max_nodes:
        dataset = top_degree_subgraph(
            dataset,
            max_nodes=args.max_nodes,
            sampled_name=f"{args.dataset_name}_top{args.max_nodes}",
        )

    output_dir = Path(args.output_dir)
    write_canonical_dataset(dataset, output_dir)
    closure_rows = build_bounded_closure(dataset, max_depth=3)
    with (output_dir / "closure_3.csv").open("w", encoding="utf-8") as handle:
        handle.write("src,dst,depth\n")
        for src, dst, depth in sorted(closure_rows):
            handle.write(f"{src},{dst},{depth}\n")


if __name__ == "__main__":
    main()
```

```python
# scripts/load_neo4j.py
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from neo4j import GraphDatabase

from graph_bench.config import load_settings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    args = parser.parse_args()

    settings = load_settings()
    dataset_dir = Path(args.dataset_dir)
    driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )

    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        session.run("CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE")
        with (dataset_dir / "nodes.csv").open(encoding="utf-8") as node_file:
            for row in csv.DictReader(node_file):
                session.run("MERGE (:User {id: $node_id})", node_id=int(row["node_id"]))
        with (dataset_dir / "edges.csv").open(encoding="utf-8") as edge_file:
            for row in csv.DictReader(edge_file):
                session.run(
                    "MATCH (src:User {id: $src}), (dst:User {id: $dst}) "
                    "MERGE (src)-[:LINK]->(dst)",
                    src=int(row["src"]),
                    dst=int(row["dst"]),
                )


if __name__ == "__main__":
    main()
```

```python
# scripts/load_postgres.py
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import psycopg

from graph_bench.config import load_settings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    args = parser.parse_args()

    settings = load_settings()
    dataset_dir = Path(args.dataset_dir)
    with psycopg.connect(settings.postgres_dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS closure_3")
            cursor.execute("DROP TABLE IF EXISTS edges")
            cursor.execute("DROP TABLE IF EXISTS users")
            cursor.execute("CREATE TABLE users (node_id BIGINT PRIMARY KEY)")
            cursor.execute("CREATE TABLE edges (src BIGINT NOT NULL, dst BIGINT NOT NULL, PRIMARY KEY (src, dst))")
            cursor.execute("CREATE TABLE closure_3 (src BIGINT NOT NULL, dst BIGINT NOT NULL, depth INT NOT NULL, PRIMARY KEY (src, dst))")
            with (dataset_dir / "nodes.csv").open(encoding='utf-8') as node_file:
                for row in csv.DictReader(node_file):
                    cursor.execute("INSERT INTO users (node_id) VALUES (%s)", (int(row["node_id"]),))
            with (dataset_dir / "edges.csv").open(encoding='utf-8') as edge_file:
                for row in csv.DictReader(edge_file):
                    cursor.execute("INSERT INTO edges (src, dst) VALUES (%s, %s)", (int(row["src"]), int(row["dst"])))
            with (dataset_dir / "closure_3.csv").open(encoding='utf-8') as closure_file:
                for row in csv.DictReader(closure_file):
                    cursor.execute(
                        "INSERT INTO closure_3 (src, dst, depth) VALUES (%s, %s, %s)",
                        (int(row["src"]), int(row["dst"]), int(row["depth"])),
                    )
        connection.commit()


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the script-level test and then exercise the data-prep script directly**

Run: `python -m pytest tests/test_prepare_dataset_script.py -q`
Expected: PASS with `1 passed`

Run: `python scripts/prepare_dataset.py --input tests/fixtures/raw/facebook_tiny.txt --dataset-name facebook_tiny --symmetrize --output-dir datasets/derived/facebook_tiny`
Expected: `datasets/derived/facebook_tiny/` contains `nodes.csv`, `edges.csv`, `metadata.json`, and `closure_3.csv`

- [ ] **Step 5: Commit the preparation and import scripts**

```bash
git add scripts/prepare_dataset.py scripts/load_neo4j.py scripts/load_postgres.py tests/test_prepare_dataset_script.py
git commit -m "feat: add canonical export and core load scripts"
```

## Task 8: Implement the Benchmark Runner and Workload Generator

**Files:**
- Create: `src/graph_bench/workloads.py`
- Create: `src/graph_bench/results.py`
- Create: `src/graph_bench/benchmark_runner.py`
- Create: `scripts/run_benchmark.py`
- Create: `tests/test_benchmark_runner.py`

- [ ] **Step 1: Write a failing benchmark runner test**

```python
# tests/test_benchmark_runner.py
import json
from pathlib import Path

from graph_bench.benchmark_runner import run_benchmark
from graph_bench.workloads import WorkloadCase


class FakeBackend:
    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        return node_id + hops

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        return left_id + right_id

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        return 2


def test_run_benchmark_emits_only_measured_rows(tmp_path: Path) -> None:
    output_path = tmp_path / "results.jsonl"
    workloads = [
        WorkloadCase(query_type="neighbors", node_id=1, hops=1),
        WorkloadCase(query_type="shortest_path", left_id=1, right_id=3, hops=3),
    ]

    run_benchmark(
        backend_name="fake",
        dataset_name="tiny",
        backend=FakeBackend(),
        workloads=workloads,
        warmup_count=1,
        measured_count=2,
        output_path=output_path,
    )

    rows = [json.loads(line) for line in output_path.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 4
    assert {row["query_type"] for row in rows} == {"neighbors", "shortest_path"}
```

- [ ] **Step 2: Run the benchmark runner test to verify it fails**

Run: `python -m pytest tests/test_benchmark_runner.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.benchmark_runner'`

- [ ] **Step 3: Implement workloads, result serialization, the benchmark runner, and the Neo4j/PostgreSQL benchmark CLI**

```python
# src/graph_bench/workloads.py
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import random


@dataclass(frozen=True)
class WorkloadCase:
    query_type: str
    node_id: int | None = None
    left_id: int | None = None
    right_id: int | None = None
    hops: int = 1


def generate_workloads(nodes: list[int], *, per_type: int) -> list[WorkloadCase]:
    rng = random.Random(5296)
    ordered = sorted(nodes)
    pairs = list(zip(ordered[::2], ordered[1::2]))
    workloads: list[WorkloadCase] = []
    for hops in (1, 2, 3):
        for node_id in rng.sample(ordered, k=min(per_type, len(ordered))):
            workloads.append(WorkloadCase(query_type="neighbors", node_id=node_id, hops=hops))
    for left_id, right_id in pairs[:per_type]:
        workloads.append(WorkloadCase(query_type="common_neighbors", left_id=left_id, right_id=right_id))
        workloads.append(WorkloadCase(query_type="shortest_path", left_id=left_id, right_id=right_id, hops=3))
    return workloads


def write_workloads(workloads: list[WorkloadCase], output_path: Path) -> None:
    output_path.write_text(
        json.dumps([asdict(workload) for workload in workloads], indent=2),
        encoding="utf-8",
    )
```

```python
# src/graph_bench/results.py
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class BenchmarkRow:
    backend: str
    dataset: str
    query_type: str
    run_id: int
    latency_ms: float
    success: bool
    result_size: int | None


def append_rows(rows: list[BenchmarkRow], output_path: Path) -> None:
    with output_path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(asdict(row)) + "\n")
```

```python
# src/graph_bench/benchmark_runner.py
from __future__ import annotations

from pathlib import Path
from time import perf_counter

from graph_bench.results import BenchmarkRow, append_rows
from graph_bench.workloads import WorkloadCase


def _execute_case(backend, workload: WorkloadCase) -> int | None:
    if workload.query_type == "neighbors":
        return backend.neighbor_count(node_id=workload.node_id, hops=workload.hops)
    if workload.query_type == "common_neighbors":
        return backend.common_neighbor_count(left_id=workload.left_id, right_id=workload.right_id)
    if workload.query_type == "shortest_path":
        return backend.shortest_path_up_to_3(left_id=workload.left_id, right_id=workload.right_id)
    raise ValueError(f"unsupported query type: {workload.query_type}")


def run_benchmark(
    *,
    backend_name: str,
    dataset_name: str,
    backend,
    workloads: list[WorkloadCase],
    warmup_count: int,
    measured_count: int,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("", encoding="utf-8")

    for workload in workloads:
        for _ in range(warmup_count):
            _execute_case(backend, workload)

        measured_rows: list[BenchmarkRow] = []
        for run_id in range(measured_count):
            start = perf_counter()
            result = _execute_case(backend, workload)
            latency_ms = round((perf_counter() - start) * 1000, 3)
            measured_rows.append(
                BenchmarkRow(
                    backend=backend_name,
                    dataset=dataset_name,
                    query_type=workload.query_type,
                    run_id=run_id,
                    latency_ms=latency_ms,
                    success=True,
                    result_size=result,
                )
            )
        append_rows(measured_rows, output_path)
```

```python
# scripts/run_benchmark.py
from __future__ import annotations

import argparse
import json
from pathlib import Path

import psycopg
from neo4j import GraphDatabase

from graph_bench.benchmark_runner import run_benchmark
from graph_bench.config import load_settings
from graph_bench.adapters.neo4j_adapter import Neo4jAdapter
from graph_bench.adapters.postgres_adapter import PostgresAdapter
from graph_bench.workloads import WorkloadCase


def _load_workloads(path: Path) -> list[WorkloadCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [WorkloadCase(**row) for row in payload]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", required=True, choices=["neo4j", "postgres"])
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--workload-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--warmup-count", type=int, default=2)
    parser.add_argument("--measured-count", type=int, default=5)
    args = parser.parse_args()

    settings = load_settings()
    workloads = _load_workloads(Path(args.workload_file))

    if args.backend == "neo4j":
        driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
        backend = Neo4jAdapter(driver)
    else:
        backend = PostgresAdapter(psycopg.connect(settings.postgres_dsn))

    run_benchmark(
        backend_name=args.backend,
        dataset_name=args.dataset_name,
        backend=backend,
        workloads=workloads,
        warmup_count=args.warmup_count,
        measured_count=args.measured_count,
        output_path=Path(args.output),
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the benchmark runner test again**

Run: `python -m pytest tests/test_benchmark_runner.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the benchmark runner**

```bash
git add src/graph_bench/workloads.py src/graph_bench/results.py src/graph_bench/benchmark_runner.py scripts/run_benchmark.py tests/test_benchmark_runner.py
git commit -m "feat: add shared benchmark runner"
```

## Task 9: Add the JanusGraph Adapter

**Files:**
- Create: `src/graph_bench/adapters/janusgraph_adapter.py`
- Create: `tests/adapters/test_janusgraph_adapter.py`
- Create: `scripts/load_janusgraph.py`
- Create: `scripts/smoke_test_janusgraph.py`
- Modify: `scripts/run_benchmark.py`

- [ ] **Step 1: Write a failing JanusGraph adapter test**

```python
# tests/adapters/test_janusgraph_adapter.py
from graph_bench.adapters.janusgraph_adapter import JanusGraphAdapter


class FakeResponse:
    def __init__(self, value):
        self._value = value

    def all(self):
        return [self._value]


class FakeClient:
    def __init__(self, values):
        self.values = list(values)
        self.calls = []

    def submit(self, query, bindings=None):
        self.calls.append((query, bindings))
        value = self.values.pop(0)
        return FakeResponse(value)


def test_neighbor_count_uses_repeat_both_times_hops() -> None:
    client = FakeClient([5])
    adapter = JanusGraphAdapter(client)

    result = adapter.neighbor_count(node_id=9, hops=2)

    assert result == 5
    query, bindings = client.calls[0]
    assert "repeat(both('link')).times(hops)" in query
    assert bindings == {"node_id": 9, "hops": 2}
```

- [ ] **Step 2: Run the JanusGraph adapter test to verify it fails**

Run: `python -m pytest tests/adapters/test_janusgraph_adapter.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.adapters.janusgraph_adapter'`

- [ ] **Step 3: Implement the JanusGraph adapter, smoke scripts, and benchmark CLI integration**

```python
# src/graph_bench/adapters/janusgraph_adapter.py
from __future__ import annotations


class JanusGraphAdapter:
    def __init__(self, client) -> None:
        self._client = client

    def _submit_scalar(self, query: str, bindings: dict[str, int]) -> int | None:
        rows = self._client.submit(query, bindings=bindings).all()
        if not rows:
            return None
        return rows[0]

    def neighbor_count(self, *, node_id: int, hops: int) -> int:
        query = (
            "g.V().has('user','id',node_id)"
            ".repeat(both('link')).times(hops)"
            ".dedup()"
            ".where(values('id').is(neq(node_id)))"
            ".count().next()"
        )
        return int(self._submit_scalar(query, {"node_id": node_id, "hops": hops}))

    def common_neighbor_count(self, *, left_id: int, right_id: int) -> int:
        query = (
            "g.V().has('user','id',left_id).both('link').aggregate('left_neighbors')"
            ".V().has('user','id',right_id).both('link').where(within('left_neighbors')).dedup().count().next()"
        )
        return int(self._submit_scalar(query, {"left_id": left_id, "right_id": right_id}))

    def shortest_path_up_to_3(self, *, left_id: int, right_id: int) -> int | None:
        query = (
            "g.V().has('user','id',left_id)"
            ".repeat(both('link').simplePath()).times(3)"
            ".emit()"
            ".has('id', right_id)"
            ".path().limit(1).count(local).next() - 1"
        )
        return self._submit_scalar(query, {"left_id": left_id, "right_id": right_id})
```

```python
# scripts/load_janusgraph.py
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from gremlin_python.driver.client import Client

from graph_bench.config import load_settings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset-dir", required=True)
    args = parser.parse_args()

    client = Client(load_settings().janusgraph_url, "g")
    dataset_dir = Path(args.dataset_dir)
    client.submit("g.V().drop().iterate()").all()

    with (dataset_dir / "nodes.csv").open(encoding="utf-8") as node_file:
        for row in csv.DictReader(node_file):
            client.submit("g.addV('user').property('id', node_id).iterate()", {"node_id": int(row["node_id"])}).all()

    with (dataset_dir / "edges.csv").open(encoding="utf-8") as edge_file:
        for row in csv.DictReader(edge_file):
            client.submit(
                "g.V().has('user','id',src).as('src').V().has('user','id',dst).addE('link').from('src').iterate()",
                {"src": int(row["src"]), "dst": int(row["dst"])},
            ).all()


if __name__ == "__main__":
    main()
```

```python
# scripts/run_benchmark.py
from __future__ import annotations

import argparse
import json
from pathlib import Path

import psycopg
from neo4j import GraphDatabase
from gremlin_python.driver.client import Client

from graph_bench.benchmark_runner import run_benchmark
from graph_bench.config import load_settings
from graph_bench.adapters.neo4j_adapter import Neo4jAdapter
from graph_bench.adapters.postgres_adapter import PostgresAdapter
from graph_bench.adapters.janusgraph_adapter import JanusGraphAdapter
from graph_bench.workloads import WorkloadCase


def _load_workloads(path: Path) -> list[WorkloadCase]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [WorkloadCase(**row) for row in payload]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", required=True, choices=["neo4j", "postgres", "janusgraph"])
    parser.add_argument("--dataset-name", required=True)
    parser.add_argument("--workload-file", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--warmup-count", type=int, default=2)
    parser.add_argument("--measured-count", type=int, default=5)
    args = parser.parse_args()

    settings = load_settings()
    workloads = _load_workloads(Path(args.workload_file))

    if args.backend == "neo4j":
        driver = GraphDatabase.driver(settings.neo4j_uri, auth=(settings.neo4j_user, settings.neo4j_password))
        backend = Neo4jAdapter(driver)
    elif args.backend == "postgres":
        backend = PostgresAdapter(psycopg.connect(settings.postgres_dsn))
    else:
        backend = JanusGraphAdapter(Client(settings.janusgraph_url, "g"))

    run_benchmark(
        backend_name=args.backend,
        dataset_name=args.dataset_name,
        backend=backend,
        workloads=workloads,
        warmup_count=args.warmup_count,
        measured_count=args.measured_count,
        output_path=Path(args.output),
    )


if __name__ == "__main__":
    main()
```

```python
# scripts/smoke_test_janusgraph.py
from __future__ import annotations

from gremlin_python.driver.client import Client

from graph_bench.adapters.janusgraph_adapter import JanusGraphAdapter
from graph_bench.config import load_settings


def main() -> None:
    client = Client(load_settings().janusgraph_url, "g")
    adapter = JanusGraphAdapter(client)
    print({"neighbors_1hop": adapter.neighbor_count(node_id=1, hops=1)})


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the JanusGraph adapter test again**

Run: `python -m pytest tests/adapters/test_janusgraph_adapter.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the JanusGraph adapter path**

```bash
git add src/graph_bench/adapters/janusgraph_adapter.py tests/adapters/test_janusgraph_adapter.py scripts/load_janusgraph.py scripts/smoke_test_janusgraph.py scripts/run_benchmark.py
git commit -m "feat: add janusgraph validation adapter"
```

## Task 10: Add Core Backend Smoke Scripts and End-to-End Commands

**Files:**
- Create: `scripts/smoke_test_core_backends.py`
- Create: `tests/test_smoke_script.py`

- [ ] **Step 1: Write a failing smoke-script test**

```python
# tests/test_smoke_script.py
from pathlib import Path


def test_core_smoke_script_uses_both_primary_adapters() -> None:
    contents = Path("scripts/smoke_test_core_backends.py").read_text(encoding="utf-8")

    assert "Neo4jAdapter" in contents
    assert "PostgresAdapter" in contents
```

- [ ] **Step 2: Run the smoke-script test to verify it fails**

Run: `python -m pytest tests/test_smoke_script.py -q`
Expected: FAIL with `FileNotFoundError` for `scripts/smoke_test_core_backends.py`

- [ ] **Step 3: Implement the core backend smoke script**

```python
# scripts/smoke_test_core_backends.py
from __future__ import annotations

import psycopg
from neo4j import GraphDatabase

from graph_bench.adapters.neo4j_adapter import Neo4jAdapter
from graph_bench.adapters.postgres_adapter import PostgresAdapter
from graph_bench.config import load_settings


def main() -> None:
    settings = load_settings()

    neo4j_driver = GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_user, settings.neo4j_password),
    )
    postgres_connection = psycopg.connect(settings.postgres_dsn)

    neo4j_adapter = Neo4jAdapter(neo4j_driver)
    postgres_adapter = PostgresAdapter(postgres_connection)

    print(
        {
            "neo4j_neighbors_1hop": neo4j_adapter.neighbor_count(node_id=1, hops=1),
            "postgres_neighbors_1hop": postgres_adapter.neighbor_count(node_id=1, hops=1),
            "neo4j_common_neighbors": neo4j_adapter.common_neighbor_count(left_id=1, right_id=2),
            "postgres_common_neighbors": postgres_adapter.common_neighbor_count(left_id=1, right_id=2),
        }
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the smoke-script test and then execute the smoke path**

Run: `python -m pytest tests/test_smoke_script.py -q`
Expected: PASS with `1 passed`

Run: `docker compose -f infra/docker-compose.yml up -d neo4j postgres`
Expected: both containers report `healthy` or `running`

Run: `python scripts/prepare_dataset.py --input tests/fixtures/raw/facebook_tiny.txt --dataset-name facebook_tiny --symmetrize --output-dir datasets/derived/facebook_tiny`
Expected: dataset files are written

Run: `python scripts/load_neo4j.py --dataset-dir datasets/derived/facebook_tiny`
Expected: command exits `0`

Run: `python scripts/load_postgres.py --dataset-dir datasets/derived/facebook_tiny`
Expected: command exits `0`

Run: `python scripts/smoke_test_core_backends.py`
Expected: printed dictionary contains equal counts for Neo4j and PostgreSQL on the tiny dataset

- [ ] **Step 5: Commit the smoke script**

```bash
git add scripts/smoke_test_core_backends.py tests/test_smoke_script.py
git commit -m "feat: add core backend smoke validation"
```

## Task 11: Add Result Aggregation and Chart Generation

**Files:**
- Create: `scripts/aggregate_results.py`
- Create: `scripts/plot_results.py`
- Create: `tests/test_aggregate_results.py`

- [ ] **Step 1: Write a failing aggregation test**

```python
# tests/test_aggregate_results.py
from pathlib import Path

from graph_bench.results import BenchmarkRow
from scripts.aggregate_results import aggregate_jsonl


def test_aggregate_jsonl_produces_summary_table(tmp_path: Path) -> None:
    input_path = tmp_path / "raw.jsonl"
    input_path.write_text(
        "\n".join(
            [
                '{"backend":"neo4j","dataset":"tiny","query_type":"neighbors","run_id":0,"latency_ms":1.0,"success":true,"result_size":2}',
                '{"backend":"neo4j","dataset":"tiny","query_type":"neighbors","run_id":1,"latency_ms":3.0,"success":true,"result_size":2}',
            ]
        ),
        encoding="utf-8",
    )

    summary = aggregate_jsonl(input_path)

    assert summary.loc[0, "backend"] == "neo4j"
    assert summary.loc[0, "p50_latency_ms"] == 2.0
```

- [ ] **Step 2: Run the aggregation test to verify it fails**

Run: `python -m pytest tests/test_aggregate_results.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.aggregate_results'`

- [ ] **Step 3: Implement aggregation and chart scripts**

```python
# scripts/aggregate_results.py
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

    aggregate_jsonl(Path(args.input)).to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
```

```python
# scripts/plot_results.py
from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    pivot = frame.pivot(index="query_type", columns="backend", values="p50_latency_ms")
    pivot.plot(kind="bar", ylabel="p50 latency (ms)", rot=0)
    plt.tight_layout()
    plt.savefig(args.output, dpi=200)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the aggregation test again**

Run: `python -m pytest tests/test_aggregate_results.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the aggregation layer**

```bash
git add scripts/aggregate_results.py scripts/plot_results.py tests/test_aggregate_results.py
git commit -m "feat: add result aggregation and plotting"
```

## Task 12: Document the Reproducible Workflow

**Files:**
- Create: `docs/runbook.md`
- Create: `docs/artifact_appendix.md`
- Create: `docs/demo_script.md`
- Create: `tests/test_docs_smoke.py`
- Modify: `README.md`

- [ ] **Step 1: Write a failing docs smoke test**

```python
# tests/test_docs_smoke.py
from pathlib import Path


def test_runbook_mentions_core_commands() -> None:
    runbook = Path("docs/runbook.md").read_text(encoding="utf-8")
    appendix = Path("docs/artifact_appendix.md").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "scripts/prepare_dataset.py" in runbook
    assert "scripts/run_benchmark.py" in appendix
    assert "docker compose -f infra/docker-compose.yml up -d neo4j postgres" in readme
```

- [ ] **Step 2: Run the docs smoke test to verify it fails**

Run: `python -m pytest tests/test_docs_smoke.py -q`
Expected: FAIL with `FileNotFoundError` for `docs/runbook.md`

- [ ] **Step 3: Write the runbook, appendix draft, demo script, and README quickstart**

```markdown
# docs/runbook.md
# Runbook

## Core local startup

1. `docker compose -f infra/docker-compose.yml up -d neo4j postgres`
2. `python scripts/prepare_dataset.py --input tests/fixtures/raw/facebook_tiny.txt --dataset-name facebook_tiny --symmetrize --output-dir datasets/derived/facebook_tiny`
3. `python scripts/load_neo4j.py --dataset-dir datasets/derived/facebook_tiny`
4. `python scripts/load_postgres.py --dataset-dir datasets/derived/facebook_tiny`
5. `python scripts/smoke_test_core_backends.py`

## Benchmark path

1. Generate the real dataset directory under `datasets/derived/`
2. Write workload JSON under `benchmarks/`
3. Run `python scripts/run_benchmark.py --backend neo4j --dataset-name facebook_full --workload-file benchmarks/facebook.json --output results/raw/neo4j-facebook.jsonl`
4. Run `python scripts/run_benchmark.py --backend postgres --dataset-name facebook_full --workload-file benchmarks/facebook.json --output results/raw/postgres-facebook.jsonl`
5. Run `python scripts/aggregate_results.py --input results/raw/neo4j-facebook.jsonl --output results/summary/neo4j-facebook.csv`
```

```markdown
# docs/artifact_appendix.md
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

1. `python -m pytest tests/test_package_smoke.py tests/test_canonical_dataset.py tests/test_closure.py tests/adapters/test_neo4j_adapter.py tests/adapters/test_postgres_adapter.py tests/test_benchmark_runner.py -q`
2. `python scripts/smoke_test_core_backends.py`
3. `python scripts/run_benchmark.py --backend neo4j --dataset-name facebook_full --workload-file benchmarks/facebook.json --output results/raw/neo4j-facebook.jsonl`
```

```markdown
# docs/demo_script.md
# Demo Script

1. Introduce the research question in one sentence.
2. Show `infra/docker-compose.yml` and explain the local-first setup.
3. Run the tiny dataset smoke flow.
4. Show one benchmark command for Neo4j and one for PostgreSQL.
5. Open the summary CSV and latency chart.
6. Close with the JanusGraph validation path and the partitioning extension.
```

```markdown
# README.md
## Quickstart

1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -e ".[dev]"`
3. `docker compose -f infra/docker-compose.yml up -d neo4j postgres`
4. `python scripts/prepare_dataset.py --input tests/fixtures/raw/facebook_tiny.txt --dataset-name facebook_tiny --symmetrize --output-dir datasets/derived/facebook_tiny`
5. `python scripts/load_neo4j.py --dataset-dir datasets/derived/facebook_tiny`
6. `python scripts/load_postgres.py --dataset-dir datasets/derived/facebook_tiny`
7. `python scripts/smoke_test_core_backends.py`
```

- [ ] **Step 4: Run the docs smoke test again**

Run: `python -m pytest tests/test_docs_smoke.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the docs and quickstart**

```bash
git add docs/runbook.md docs/artifact_appendix.md docs/demo_script.md README.md tests/test_docs_smoke.py
git commit -m "docs: add runbook appendix and demo script"
```

## Task 13: Add the Lightweight Partitioning Extension

**Files:**
- Create: `src/graph_bench/partitioning.py`
- Create: `tests/test_partitioning.py`
- Create: `scripts/evaluate_partitioning.py`

- [ ] **Step 1: Write a failing partitioning test**

```python
# tests/test_partitioning.py
from graph_bench.models import GraphDataset, GraphMetadata
from graph_bench.partitioning import edge_cut_ratio, hash_partition, locality_aware_partition


def test_locality_aware_partition_reduces_edge_cut_on_clustered_graph() -> None:
    dataset = GraphDataset(
        metadata=GraphMetadata(dataset_name="clustered", directed=False, node_count=6, edge_count=14),
        nodes={1, 2, 3, 4, 5, 6},
        edges={
            (1, 2), (2, 1), (2, 3), (3, 2), (1, 3), (3, 1),
            (4, 5), (5, 4), (5, 6), (6, 5), (4, 6), (6, 4),
            (3, 4), (4, 3),
        },
    )

    hash_assignments = hash_partition(dataset, partition_count=2)
    locality_assignments = locality_aware_partition(dataset, partition_count=2)

    assert edge_cut_ratio(dataset, locality_assignments) < edge_cut_ratio(dataset, hash_assignments)
```

- [ ] **Step 2: Run the partitioning test to verify it fails**

Run: `python -m pytest tests/test_partitioning.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'graph_bench.partitioning'`

- [ ] **Step 3: Implement the partitioning heuristics and evaluator**

```python
# src/graph_bench/partitioning.py
from __future__ import annotations

from collections import Counter, defaultdict

from graph_bench.models import GraphDataset


def hash_partition(dataset: GraphDataset, *, partition_count: int) -> dict[int, int]:
    return {node_id: node_id % partition_count for node_id in sorted(dataset.nodes)}


def locality_aware_partition(dataset: GraphDataset, *, partition_count: int) -> dict[int, int]:
    adjacency: dict[int, set[int]] = defaultdict(set)
    degree: Counter[int] = Counter()
    for src, dst in dataset.edges:
        adjacency[src].add(dst)
        degree[src] += 1

    seeds = [node_id for node_id, _ in degree.most_common(partition_count)]
    assignments: dict[int, int] = {seed: index for index, seed in enumerate(seeds)}
    frontier = list(seeds)

    while frontier:
        current = frontier.pop(0)
        current_partition = assignments[current]
        for neighbor in sorted(adjacency[current]):
            if neighbor in assignments:
                continue
            assignments[neighbor] = current_partition
            frontier.append(neighbor)

    unassigned = [node_id for node_id in sorted(dataset.nodes) if node_id not in assignments]
    for index, node_id in enumerate(unassigned):
        assignments[node_id] = index % partition_count

    return assignments


def edge_cut_ratio(dataset: GraphDataset, assignments: dict[int, int]) -> float:
    crossing = 0
    for src, dst in dataset.edges:
        if assignments[src] != assignments[dst]:
            crossing += 1
    return round(crossing / max(1, len(dataset.edges)), 4)
```

```python
# scripts/evaluate_partitioning.py
from __future__ import annotations

import argparse
from pathlib import Path

from graph_bench.canonical import read_edge_list
from graph_bench.partitioning import edge_cut_ratio, hash_partition, locality_aware_partition


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--partitions", type=int, default=4)
    args = parser.parse_args()

    dataset = read_edge_list(
        Path(args.input),
        dataset_name="partition_eval",
        directed=False,
        symmetrize=True,
    )
    hash_assignments = hash_partition(dataset, partition_count=args.partitions)
    locality_assignments = locality_aware_partition(dataset, partition_count=args.partitions)
    print(
        {
            "hash_edge_cut": edge_cut_ratio(dataset, hash_assignments),
            "locality_edge_cut": edge_cut_ratio(dataset, locality_assignments),
        }
    )


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the partitioning test again**

Run: `python -m pytest tests/test_partitioning.py -q`
Expected: PASS with `1 passed`

- [ ] **Step 5: Commit the partitioning extension**

```bash
git add src/graph_bench/partitioning.py tests/test_partitioning.py scripts/evaluate_partitioning.py
git commit -m "feat: add lightweight partitioning evaluation"
```

## Task 14: Run the First Full Validation Sweep

**Files:**
- Modify: `benchmarks/` by adding workload JSON files generated from `src/graph_bench/workloads.py`
- Modify: `results/raw/` and `results/summary/` by generating first-pass outputs

- [ ] **Step 1: Generate workload files for the tiny and primary datasets**

```python
# one-off Python command
from pathlib import Path
import json

from graph_bench.workloads import generate_workloads, write_workloads

write_workloads(generate_workloads([1, 2, 3, 4], per_type=2), Path("benchmarks/facebook_tiny.json"))
write_workloads(generate_workloads(list(range(1, 10001)), per_type=25), Path("benchmarks/twitter_top10000.json"))
```

- [ ] **Step 2: Run the core test suite**

Run: `python -m pytest tests/test_package_smoke.py tests/test_canonical_dataset.py tests/test_config.py tests/test_closure.py tests/adapters/test_neo4j_adapter.py tests/adapters/test_postgres_adapter.py tests/adapters/test_janusgraph_adapter.py tests/test_benchmark_runner.py tests/test_aggregate_results.py tests/test_docs_smoke.py tests/test_partitioning.py -q`
Expected: PASS with all listed tests green

- [ ] **Step 3: Run the tiny end-to-end benchmark smoke**

Run: `python scripts/run_benchmark.py --backend neo4j --dataset-name facebook_tiny --workload-file benchmarks/facebook_tiny.json --output results/raw/neo4j-facebook-tiny.jsonl`
Expected: command exits `0` and writes JSONL rows

Run: `python scripts/run_benchmark.py --backend postgres --dataset-name facebook_tiny --workload-file benchmarks/facebook_tiny.json --output results/raw/postgres-facebook-tiny.jsonl`
Expected: command exits `0` and writes JSONL rows

Run: `python scripts/aggregate_results.py --input results/raw/neo4j-facebook-tiny.jsonl --output results/summary/neo4j-facebook-tiny.csv`
Expected: summary CSV exists with `p50_latency_ms`

- [ ] **Step 4: Commit the validated baseline**

```bash
git add benchmarks results
git commit -m "test: capture first validated benchmark baseline"
```

## Execution Order for the Team

Use this order to parallelize without stepping on each other:

1. One engineer executes Tasks 1 through 4.
2. Engineer A takes Tasks 5 and 10.
3. Engineer B takes Tasks 6 and 7.
4. Engineer C takes Tasks 8, 9, 11, and 12.
5. After Tasks 5 through 12 are merged, one engineer executes Task 14.
6. Only after Task 14 is green should anyone execute Task 13 for the lightweight partitioning extension.

## Self-Review

- Spec coverage:
  - Repository skeleton and local-first workflow: Tasks 1, 3, 12
  - Canonical data pipeline: Tasks 2, 4, 7
  - Neo4j and PostgreSQL primary comparison path: Tasks 5, 6, 10, 14
  - JanusGraph minimum validation path: Task 9
  - Benchmark runner and unified result format: Task 8
  - Reporting and artifact support: Tasks 11 and 12
  - Lightweight innovation extension: Task 13
- Placeholder scan:
  - No unresolved markers or postponed work notes remain in the plan.
- Type consistency:
  - All backends expose `neighbor_count`, `common_neighbor_count`, and `shortest_path_up_to_3`.
  - The bounded closure table is named `closure_3` everywhere.
  - Dataset preparation writes `nodes.csv`, `edges.csv`, `metadata.json`, and `closure_3.csv`.
