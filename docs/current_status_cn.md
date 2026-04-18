# 项目当前状态与下一步实验计划

日期：2026-04-18

## 1. 当前项目进度

当前仓库已经不再是“只有文档”的状态，而是进入了“实验底座已经搭好、真实数据实验尚未开始”的阶段。

已经完成的部分如下：

- 本地代码骨架已完成
  - 已有 Python 包 `graph_bench`
  - 已有数据准备、benchmark、聚合、绘图、smoke test 等脚本
- 本地数据库环境已完成
  - `Neo4j`
  - `PostgreSQL`
  - `JanusGraph`
  - `Cassandra`
- 小样本验证已完成
  - tiny 图数据已经成功导入 `Neo4j`、`PostgreSQL`、`JanusGraph`
  - 三套后端都能跑基础查询
  - tiny benchmark 结果已经写入 `results/raw/` 与 `results/summary/`
- 本地运行文档已完成
  - [README](README.md)
  - [runbook](runbook.md)
  - [artifact appendix draft](artifact_appendix.md)
  - [demo script](demo_script.md)

## 2. 当前阶段的准确判断

如果对照课程行动指南，当前状态可以理解为：

- 第一阶段“环境搭建与数据准备”：已完成大部分
- 第二阶段“基准测试框架”：基本完成
- 第三阶段“对比实验”：刚开始
- 第四阶段“分区策略研究”：只有轻量实现，尚未形成正式实验结果
- 第五阶段“报告与演示”：只有支撑文档，尚未进入最终交付整理

因此，当前最重要的工作重点已经不是继续搭骨架，而是切换到“真实 SNAP 数据实验”。

## 3. 现在还缺什么

当前还没有真正完成的核心内容是：

- 下载并整理真实 SNAP 图数据
- 用真实数据跑第一轮正式 benchmark
- 生成能写进报告的第一版结果图表
- 写出第一版结论
- 再决定 `Twitter` 和 `JanusGraph` 要做到多深

需要特别说明的是：

- 现在仓库中的 `facebook_tiny` 只用于本地 smoke test
- 它不能作为课程报告中的正式实验数据
- 正式实验必须切换到真实 SNAP 数据集

## 4. 接下来最该做的事情

下一阶段的建议顺序如下：

1. 下载 SNAP Facebook 数据到 `datasets/raw/`
2. 使用 `scripts/prepare_dataset.py` 转换成 canonical 格式
3. 导入 `Neo4j` 和 `PostgreSQL`
4. 跑第一轮正式 benchmark
5. 生成第一版 summary 和图表
6. 根据第一轮结果决定：
   - 是否继续上 `Twitter`
   - `JanusGraph` 做到“最小验证”还是“补一部分 benchmark”

## 5. 第一轮正式实验建议范围

为了控制时间和风险，第一轮正式实验建议先只做：

- 数据集：`Facebook`
- 主对比后端：
  - `Neo4j`
  - `PostgreSQL`
- 查询类型：
  - `1-hop neighbors`
  - `2-hop neighbors`
  - `3-hop neighbors`
  - `common neighbors`
  - `shortest path up to 3`

原因：

- 这是当前最稳、最容易先产出报告材料的路径
- 一旦这条主线有结果，后续不管是补 `Twitter` 还是补 `JanusGraph`，都属于增强，而不是救火

## 6. 建议的第一轮产出物

完成第一轮正式实验后，仓库中应该至少新增这些内容：

- `datasets/raw/` 下的原始 SNAP 文件
- `datasets/derived/` 下的正式 canonical 导出目录
- `results/raw/` 下的正式 benchmark 原始结果
- `results/summary/` 下的聚合 CSV
- 如有需要，再补：
  - `results/plots/` 下的图表 PNG
  - 报告结论草稿

## 7. 当前推荐执行命令

下面是第一轮正式实验的建议执行链路：

```bash
# 1. 下载 SNAP Facebook 数据到 datasets/raw/
# 2. 假设下载文件路径为 datasets/raw/facebook_combined.txt

python3 scripts/prepare_dataset.py \
  --input datasets/raw/facebook_combined.txt \
  --dataset-name facebook_full \
  --symmetrize \
  --output-dir datasets/derived/facebook_full

python3 scripts/load_neo4j.py \
  --dataset-dir datasets/derived/facebook_full

python3 scripts/load_postgres.py \
  --dataset-dir datasets/derived/facebook_full

python3 scripts/run_benchmark.py \
  --backend neo4j \
  --dataset-name facebook_full \
  --workload-file benchmarks/facebook_tiny.json \
  --output results/raw/neo4j-facebook-full.jsonl

python3 scripts/run_benchmark.py \
  --backend postgres \
  --dataset-name facebook_full \
  --workload-file benchmarks/facebook_tiny.json \
  --output results/raw/postgres-facebook-full.jsonl

python3 scripts/aggregate_results.py \
  --input results/raw/neo4j-facebook-full.jsonl \
  --output results/summary/neo4j-facebook-full.csv

python3 scripts/aggregate_results.py \
  --input results/raw/postgres-facebook-full.jsonl \
  --output results/summary/postgres-facebook-full.csv
```

## 8. 一个重要提醒

正式实验开始前，最好不要直接复用现在仓库里的占位 workload 文件作为最终实验输入。更稳妥的做法是：

- 先完成真实数据导入
- 再根据真实图中的节点 ID 范围生成新的 workload 文件

这样可以避免 benchmark 输入和真实数据不匹配。

## 9. 结论

当前阶段的正确判断是：

- 已完成：实验基础设施与本地小样本验证
- 尚未完成：真实数据实验、正式结果、报告结论与最终交付

因此，当前项目的主任务已经明确：

从“骨架建设”切换到“第一轮真实 SNAP Facebook 实验”。
