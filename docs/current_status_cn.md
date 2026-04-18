# 项目当前状态与下一步实验计划

日期：2026-04-18

## 1. 当前进度判断

当前项目已经不再是“只有文档”或“只有骨架”的状态，而是进入了：

- 实验底座已完成
- 小样本 smoke test 已完成
- 第一轮真实 `SNAP Facebook` 正式实验已完成
- `Twitter` 扩展实验、`JanusGraph` 正式对比、报告整合还未完成

也就是说，现在仓库已经具备“能跑真实实验并产出第一版结果”的能力，而不只是一个 scaffold。

## 2. 已完成内容

目前已经完成的部分如下：

- 代码与脚本
  - `graph_bench` Python 包已建立
  - 数据准备、数据导入、benchmark、聚合、绘图、smoke test、partitioning 脚本都已可用
- 本地数据库环境
  - `Neo4j`
  - `PostgreSQL`
  - `JanusGraph`
  - `Cassandra`
- 小样本验证
  - `facebook_tiny` 已跑通 `Neo4j / PostgreSQL / JanusGraph`
  - tiny benchmark 结果已写入 `results/raw/` 和 `results/summary/`
- 真实数据准备
  - 已下载 `SNAP Facebook` 原始数据：
    - `datasets/raw/facebook_combined.txt.gz`
    - `datasets/raw/facebook_combined.txt`
  - 已生成 canonical 数据目录：
    - `datasets/derived/facebook_full/`
- 第一轮正式 benchmark
  - 已完成 `facebook_full` 在 `Neo4j` 与 `PostgreSQL` 上的导入
  - 已完成正式 workload 生成：
    - `benchmarks/facebook_full.json`
  - 已完成正式 benchmark 原始结果：
    - `results/raw/neo4j-facebook-full.jsonl`
    - `results/raw/postgres-facebook-full.jsonl`
  - 已完成结果聚合与图表：
    - `results/summary/neo4j-facebook-full.csv`
    - `results/summary/postgres-facebook-full.csv`
    - `results/summary/facebook-full-comparison.csv`
    - `results/summary/facebook-full-p50-latency.png`

## 3. 当前数据规模

这次正式实验使用的是 `SNAP Facebook Combined` 数据，转换后得到：

- 节点数：`4039`
- 边数：`176468`
- `closure_3.csv` 行数：约 `6874455`

说明：

- `edges.csv` 是对原图做了对称化后的有向边表示
- `closure_3.csv` 是预计算的 3-hop 可达闭包，主要服务于 `PostgreSQL` 查询

## 4. 第一轮正式实验结果

当前已得到的聚合结果如下。

### Neo4j

- `common_neighbors`
  - `p50 = 0.513 ms`
  - `p95 = 0.999 ms`
- `neighbors`
  - `p50 = 2.059 ms`
  - `p95 = 17.063 ms`
- `shortest_path`
  - `p50 = 0.550 ms`
  - `p95 = 0.929 ms`

### PostgreSQL

- `common_neighbors`
  - `p50 = 0.332 ms`
  - `p95 = 0.744 ms`
- `neighbors`
  - `p50 = 0.295 ms`
  - `p95 = 0.416 ms`
- `shortest_path`
  - `p50 = 0.174 ms`
  - `p95 = 0.306 ms`

### 初步结论

- 在当前实现下，`PostgreSQL` 明显快于 `Neo4j`
- 差距最大的查询类型是 `neighbors`
- `common_neighbors` 和 `shortest_path` 两边都很快，但 `PostgreSQL` 仍然更低延迟

## 5. 结果解释时必须说明的 caveat

这轮结果可以写进阶段汇报，但在正式报告里必须解释下面这一点：

- `PostgreSQL` 查询当前依赖 `closure_3` 预计算表
- `Neo4j` 查询当前是在图上做在线多跳展开

因此，这一轮对比更准确地说是在比较：

- `关系数据库 + 预计算闭包`
- `图数据库 + 在线遍历`

而不是一个完全 apples-to-apples 的纯引擎基准。  
这并不影响本轮结果有效，但在报告中要写清楚，否则容易被老师问。

## 6. 本轮推进中已经解决的关键技术问题

在这轮真实实验里，已经修掉了几个会卡住项目的点：

- `PostgreSQL` 导入优化
  - 原始逐行插入在 `facebook_full` 上太慢
  - 现在改成了 `COPY` 批量导入
- `Neo4j` 多跳查询优化
  - 原来的 `*1..3` 可变长度路径在真实图上会非常慢
  - 现在改成了更稳定的分层展开写法
- `JanusGraph` 本地资源控制
  - 已将默认过大的 JVM heap 调低到适合本地开发的级别

## 7. 现在还没完成什么

虽然已经不是“只有骨架”，但距离作业完整交付还差几块关键内容：

- 还没有跑 `Twitter` 的正式实验
- 还没有决定 `JanusGraph` 是做“最小验证”还是“补正式 benchmark”
- 还没有把当前结果整理成课程报告正文
- 还没有制作最终展示材料和讲解逻辑

## 8. 接下来最合理的顺序

当前建议的下一步不是继续改底座，而是继续推进实验与交付：

1. 基于这轮 `facebook_full` 结果，先写第一版报告结论草稿
2. 决定 `Twitter` 要不要作为第二个正式数据集
3. 决定 `JanusGraph` 是只保留 smoke validation，还是补一轮正式 benchmark
4. 补报告中的方法、实验设置、结果分析、局限性
5. 最后整理 demo 和 artifact 说明

## 9. 当前最稳妥的任务拆分建议

如果三个人并行推进，当前阶段比较稳的拆分方式是：

- 一个人负责报告正文
  - 背景
  - 方法
  - 实验设置
  - 当前 `facebook_full` 结果整理
- 一个人负责扩展实验
  - `Twitter`
  - workload 调整
  - 更多图表
- 一个人负责系统与 artifact
  - `JanusGraph`
  - runbook
  - demo script
  - artifact appendix

## 10. 结论

当前项目的准确状态是：

- 已完成：实验平台、真实 Facebook 数据准备、第一轮正式 benchmark、第一版图表
- 未完成：扩展数据集、完整对比矩阵、报告整合、最终演示

所以当前最重要的工作重点已经很清楚：

从“搭系统”切换到“补实验结论与完成作业交付”。
