# CS5296 · 云原生图数据库的大规模社交网络多跳查询优化

本仓库为 **HKU CS5296 Cloud Computing** 小组研究项目代码与文档的协作空间。课程要求、评分与交付节奏以课程材料为准；**内部执行清单与阶段划分**见 [`docs/docx/markdown/action_guide_cn.md`](docs/docx/markdown/action_guide_cn.md)。

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
docs/docx/              # 课程 PDF、proposal 与参考材料
docs/docx/markdown/ # 中英说明、小组 proposal、行动指南等
```

后续开发可在仓库根目录增加 `src/`、`scripts/`、`infra/` 等目录，并在本 README 中补充运行方式与环境变量说明。

---

## 本地开发（占位）

环境与依赖将随代码落地更新。一般流程预期为：

1. 克隆本仓库并创建 Python/工具虚拟环境（若项目采用脚本与自动化测试）。  
2. 按 `docs/docx/markdown/action_guide_cn.md` 中的阶段推进实验与记录。  
3. 大规模实验前优先用小数据集验证，控制 AWS 费用。

---

## 文档索引

| 文档 | 说明 |
|------|------|
| [行动指南（中文）](docs/docx/markdown/action_guide_cn.md) | 阶段任务、交付物、预算与风险 |
| [小组 Proposal（Markdown）](docs/docx/markdown/group15_proposal.md) | 小组选题与方案摘要 |

---

## 许可与声明

课程作业材料仅供课程与学习使用；数据集使用需遵守 SNAP 与各数据集的许可与引用要求。
