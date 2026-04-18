# CS5296 · 云原生图数据库的大规模社交网络多跳查询优化

本仓库为 **香港城市大学（CityU）CS5296 Cloud Computing** 小组研究项目代码与文档的协作空间。课程要求、评分与交付节奏以课程材料为准；**内部执行清单与阶段划分**见 [`docs/docx/markdown/action_guide_cn.md`](docs/docx/markdown/action_guide_cn.md)。

**远程仓库**：[bigyong-996/cs5296-graph-multihop-optimization](https://github.com/bigyong-996/cs5296-graph-multihop-optimization)

---

## 项目概览

| 项目 | 说明 |
|------|------|
| **类型** | Research（最高 25 分） |
| **团队** | 3 人 |
| **预算** | $150（每人约 $50 AWS Academy 额度） |

### 核心研究问题

在社交网络中，多跳关系查询（如「好友的好友」、三度人脉、共同好友）十分常见。当图规模超过单机内存时，如何选择合适的存储与分区策略，以优化查询性能？

### 技术路线（对比）

| 方案 | 技术栈 | 优势 | 劣势 |
|------|--------|------|------|
| Neo4j | EC2 自建 | 原生图查询、Cypher 易用 | 单机扩展性有限 |
| JanusGraph | EC2 + Cassandra | 分布式、可水平扩展 | 配置复杂 |
| RDS（闭包表） | PostgreSQL | SQL 熟悉、成本较低 | 多跳查询性能相对弱 |

**创新方向**：*locality-aware* 分区——将高连接度用户聚簇，减少跨分区查询。

---

## 数据与评估

- **数据**：斯坦福 [SNAP](https://snap.stanford.edu/data/) 公开数据集（Facebook / Twitter / Pokec / LiveJournal 等，按实验阶段选用）。
- **指标**：查询延迟（p50 / p95 / p99）、吞吐量（QPS）、资源消耗（CPU / 内存 / 磁盘 I/O）。

---

## 阶段路线图（摘要）

详细勾选清单见行动指南。

1. **环境 & 数据**：SNAP 数据、EC2 上 Neo4j、导入与基础查询验证。  
2. **基准框架**：多类查询模式（1/2/3-hop、共同好友、最短路径等）、自动化压测与指标记录。  
3. **对比实验**：JanusGraph（可选）、RDS 闭包表、同数据集对比。  
4. **分区研究**：Hash 分区 vs locality-aware 分区。  
5. **交付**：终稿报告、Artifact、Demo 视频（截止以课程通知为准）。

---

## 仓库结构（当前）

```text
src/graph_bench/         # 数据准备、adapter、benchmark 与 partitioning 代码
scripts/                 # 数据导入、benchmark、聚合与 smoke scripts
infra/                   # 本地 Docker Compose 环境
datasets/derived/        # 小规模样例数据与导出格式
docs/docx/               # 课程 PDF、proposal 与参考材料
docs/docx/markdown/      # 中英说明、小组 proposal、行动指南等
docs/superpowers/        # 设计文档与 implementation plan
```

---

## 当前实验状态

- `facebook_full` 已完成 `Neo4j + PostgreSQL` 正式 benchmark
- `twitter_top10000` 已完成 `Neo4j + PostgreSQL` 正式 benchmark
- `JanusGraph` 保留 tiny benchmark 和增强验证路径，但不进入主对比矩阵
- 结构化结论、可写入报告的 claim 和 caveat 见 [docs/experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)

---

## Quickstart

1. `python3 -m venv .venv && source .venv/bin/activate`
2. `python3 -m pip install -e ".[dev]"`
3. `docker compose -f infra/docker-compose.yml up -d neo4j postgres`
4. `python3 scripts/prepare_dataset.py --input tests/fixtures/raw/facebook_tiny.txt --dataset-name facebook_tiny --symmetrize --output-dir datasets/derived/facebook_tiny`
5. `python3 scripts/load_neo4j.py --dataset-dir datasets/derived/facebook_tiny`
6. `python3 scripts/load_postgres.py --dataset-dir datasets/derived/facebook_tiny`
7. `python3 scripts/smoke_test_core_backends.py`

本仓库当前以本地优先的方式开发与验证，再按需要映射到云上实验环境。

---

## 主实验结果入口

主实验结果固定为两条：

- `facebook_full` on `Neo4j + PostgreSQL`
- `twitter_top10000` on `Neo4j + PostgreSQL`

对应产物：

- [results/summary/facebook-full-comparison.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-comparison.csv)
- [results/summary/facebook-full-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-p50-latency.png)
- [results/summary/twitter-top10000-comparison.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-comparison.csv)
- [results/summary/twitter-top10000-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-p50-latency.png)

---

## 文档索引

| 文档 | 说明 |
|------|------|
| [行动指南（中文）](docs/docx/markdown/action_guide_cn.md) | 阶段任务、交付物、预算与风险 |
| [小组 Proposal（Markdown）](docs/docx/markdown/group15_proposal.md) | 小组选题与方案摘要 |
| [本地运行手册](docs/runbook.md) | 本地开发、导入与 benchmark 命令 |
| [实验说明笔记](docs/experiment_notes.md) | 数据规模、结果结论、报告可用 claim 与 caveat |
| [Artifact Appendix 草稿](docs/artifact_appendix.md) | 复现实验与仓库入口说明 |
| [Demo Script](docs/demo_script.md) | Demo 视频讲解提纲 |

---

## 许可与声明

课程作业材料仅供课程与学习使用；数据集使用需遵守 SNAP 与各数据集的许可与引用要求。
