# 项目当前状态与下一步收尾建议

日期：2026-04-18

## 1. 当前完成度判断

当前项目已经从“实验底座完成”推进到了“主实验矩阵已完成”的阶段。

现在的准确状态是：

- `facebook_full` 主实验已完成
- `twitter_top10000` 主实验已完成
- `JanusGraph` 保留为增强项，不进入主对比矩阵
- 报告正文、最终 demo 讲稿、最终 artifact 整理还没完全写完

所以当前项目已经不是“只有骨架”，而是已经具备了两组真正可以写进报告的正式结果。

## 2. 已完成的核心内容

### 工程与脚本

- `graph_bench` 包已具备数据准备、backend adapter、benchmark、聚合、绘图和 smoke test
- `Neo4j / PostgreSQL / JanusGraph / Cassandra` 本地容器链路已建立
- `smoke_test_core_backends.py` 和 `smoke_test_janusgraph.py` 已支持参数化节点输入
- `aggregate_results.py` 已补充 `p99_latency_ms`

### 正式数据集

- `facebook_full`
  - 原始数据已下载
  - canonical 数据已生成
  - 正式 workload 已生成
  - `Neo4j + PostgreSQL` benchmark 已完成
- `twitter_top10000`
  - 原始 `twitter_combined` 已下载
  - `top10000` canonical 数据已生成
  - 真实 workload 已重生成
  - `Neo4j + PostgreSQL` benchmark 已完成

### 结果文件

已落地的主结果包括：

- `results/summary/facebook-full-comparison.csv`
- `results/summary/facebook-full-p50-latency.png`
- `results/summary/twitter-top10000-comparison.csv`
- `results/summary/twitter-top10000-p50-latency.png`
- `docs/experiment_notes.md`

## 3. 当前正式实验结论

### Facebook

在 `facebook_full` 上：

- `PostgreSQL` 明显快于 `Neo4j`
- 尤其是 `neighbors` 查询差距更明显
- `shortest_path` 也仍然是 `PostgreSQL` 更快

### Twitter

在 `twitter_top10000` 上：

- `Neo4j` 在 `neighbors` 和 `common_neighbors` 上明显反超 `PostgreSQL`
- `PostgreSQL` 在 `shortest_path` 上仍然最快

也就是说，当前项目已经不是只有一组结论，而是已经出现了“不同数据规模/结构下，优势后端会发生变化”的研究结果，这一点对报告非常有价值。

## 4. 结果解释时必须写明的 caveat

报告里一定要明确写：

- 当前 `PostgreSQL` 路线使用的是 `closure_3` 预计算表
- 当前 `Neo4j` 路线使用的是在线多跳遍历

所以这不是纯粹的“数据库引擎对引擎”对比，而是：

- `PostgreSQL + closure_3`
- versus `Neo4j` online traversal

这个 caveat 已经整理进 [experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)。

## 5. JanusGraph 当前定位

JanusGraph 现在的正确定位是：

- 保留 tiny benchmark 和增强验证路径
- 已完成 `facebook_full` 的 full-data smoke validation
- 不进入主对比矩阵

原因不是“完全跑不通”，而是：

- full benchmark 路径出现了不稳定因素
- 清理和重导过程存在 Gremlin timeout
- 继续强行把它塞进主实验矩阵，收益不如继续完成报告与交付

所以当前最合理的写法是：

- 主矩阵：`facebook_full + twitter_top10000` on `Neo4j + PostgreSQL`
- 次要增强：`JanusGraph` tiny path + `facebook_full` full-data smoke validation

## 6. 现在还缺什么

离最终交付最近的缺口主要不在代码，而在材料整理：

- 把 `docs/experiment_notes.md` 写进最终报告正文
- 把现有图表嵌入报告并补文字解释
- 整理 Artifact Appendix 最终版本
- 录制或准备 Demo 视频

## 7. 当前最推荐的收尾顺序

1. 以 `docs/experiment_notes.md` 为基础写报告实验部分
2. 把 `facebook_full` 和 `twitter_top10000` 两张图放进报告
3. 在报告中明确写出 `PostgreSQL + closure_3` 的 caveat
4. 将 JanusGraph 写成增强项，而不是主结论来源
5. 按 `docs/demo_script.md` 整理最终 demo

## 8. 一句话结论

当前项目的最好表述是：

主实验已经完成，剩下的主要是把结果整理成“能交、能讲、能 defend”的最终材料。
