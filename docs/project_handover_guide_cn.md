# 项目交接与收尾指南

日期：2026-04-18

本文档的目标不是重复仓库里每个文件的内容，而是给当前团队一个“拿来就能接着干”的总览：

- 现在项目已经做到哪里
- 已完成内容分别保存在什么位置
- 接下来还建议做什么
- 另外两位同学如何最快熟悉这个项目
- 最终报告应该怎么整理
- Demo 应该怎么做
- 还有哪些容易遗漏但实际很重要的收尾点

---

## 1. 一句话判断当前项目状态

当前项目已经不是“只有骨架”的状态，而是已经进入：

- 主实验矩阵已完成
- 报告级结果已初步齐备
- Artifact 结构已基本具备
- 剩余重点主要是整理报告、讲清结论、完成 demo

如果用更直白的话说：

**代码、数据管线、两组主实验、主要图表、运行文档都已经有了；现在最重要的已经不是继续搭系统，而是把现有结果整理成最终可交付材料。**

---

## 2. 现在已经做了什么

### 2.1 代码与工程底座

已经完成：

- Python 包 `graph_bench`
- 数据准备脚本
- `Neo4j / PostgreSQL / JanusGraph` adapter
- benchmark runner
- 结果聚合脚本
- 出图脚本
- smoke test
- 轻量分区策略实验

对应代码位置：

- 核心包：
  - [src/graph_bench](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/src/graph_bench)
- 入口脚本：
  - [scripts](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts)
- 容器环境：
  - [infra/docker-compose.yml](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/infra/docker-compose.yml)

### 2.2 小样本验证

已经完成：

- `facebook_tiny` 数据生成
- `Neo4j / PostgreSQL / JanusGraph` 的 tiny 导入
- tiny smoke 验证
- tiny benchmark

主要文件：

- 数据：
  - [datasets/derived/facebook_tiny](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/datasets/derived/facebook_tiny)
- workload：
  - [benchmarks/facebook_tiny.json](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/benchmarks/facebook_tiny.json)
- tiny raw results：
  - [results/raw/neo4j-facebook-tiny.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/neo4j-facebook-tiny.jsonl)
  - [results/raw/postgres-facebook-tiny.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/postgres-facebook-tiny.jsonl)
  - [results/raw/janusgraph-facebook-tiny.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/janusgraph-facebook-tiny.jsonl)
- tiny summary：
  - [results/summary/neo4j-facebook-tiny.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/neo4j-facebook-tiny.csv)
  - [results/summary/postgres-facebook-tiny.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/postgres-facebook-tiny.csv)
  - [results/summary/janusgraph-facebook-tiny.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/janusgraph-facebook-tiny.csv)

### 2.3 Facebook 主实验

已经完成：

- 下载真实 `SNAP Facebook` 数据
- 生成 `facebook_full` canonical 数据
- 生成真实 workload
- 导入 `Neo4j`
- 导入 `PostgreSQL`
- 跑完整正式 benchmark
- 汇总 summary
- 生成图表

主要文件：

- 原始数据：
  - [datasets/raw/facebook_combined.txt.gz](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/datasets/raw/facebook_combined.txt.gz)
  - [datasets/raw/facebook_combined.txt](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/datasets/raw/facebook_combined.txt)
- canonical 数据：
  - [datasets/derived/facebook_full](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/datasets/derived/facebook_full)
- workload：
  - [benchmarks/facebook_full.json](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/benchmarks/facebook_full.json)
- raw results：
  - [results/raw/neo4j-facebook-full.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/neo4j-facebook-full.jsonl)
  - [results/raw/postgres-facebook-full.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/postgres-facebook-full.jsonl)
- summary：
  - [results/summary/neo4j-facebook-full.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/neo4j-facebook-full.csv)
  - [results/summary/postgres-facebook-full.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/postgres-facebook-full.csv)
  - [results/summary/facebook-full-comparison.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-comparison.csv)
  - [results/summary/facebook-full-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-p50-latency.png)

### 2.4 Twitter 主实验

已经完成：

- 下载真实 `SNAP Twitter` 数据
- 生成 `twitter_top10000` canonical 数据
- 根据真实节点重生成 workload
- 导入 `Neo4j`
- 导入 `PostgreSQL`
- 跑完整正式 benchmark
- 汇总 summary
- 生成图表

主要文件：

- workload：
  - [benchmarks/twitter_top10000.json](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/benchmarks/twitter_top10000.json)
- raw results：
  - [results/raw/neo4j-twitter-top10000.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/neo4j-twitter-top10000.jsonl)
  - [results/raw/postgres-twitter-top10000.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/postgres-twitter-top10000.jsonl)
- summary：
  - [results/summary/neo4j-twitter-top10000.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/neo4j-twitter-top10000.csv)
  - [results/summary/postgres-twitter-top10000.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/postgres-twitter-top10000.csv)
  - [results/summary/twitter-top10000-comparison.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-comparison.csv)
  - [results/summary/twitter-top10000-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-p50-latency.png)

### 2.5 JanusGraph 增强路径

已经完成：

- tiny benchmark
- `facebook_full` full-data smoke validation
- `facebook_full_probe10` 输入文件准备

但没有完成：

- `facebook_full` 的完整 JanusGraph benchmark
- `twitter_top10000` 的 JanusGraph benchmark

当前定位：

- JanusGraph 是增强项
- 不进入主实验矩阵

相关文件：

- tiny raw / summary：
  - [results/raw/janusgraph-facebook-tiny.jsonl](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/raw/janusgraph-facebook-tiny.jsonl)
  - [results/summary/janusgraph-facebook-tiny.csv](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/janusgraph-facebook-tiny.csv)
- probe 输入：
  - [benchmarks/facebook_full_probe10.json](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/benchmarks/facebook_full_probe10.json)

### 2.6 文档与交付支撑

目前已有的关键文档：

- 运行手册：
  - [docs/runbook.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/runbook.md)
- 实验结论笔记：
  - [docs/experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)
- Artifact 附录草稿：
  - [docs/artifact_appendix.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/artifact_appendix.md)
- Demo 讲解提纲：
  - [docs/demo_script.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/demo_script.md)
- 中文状态总结：
  - [docs/current_status_cn.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/current_status_cn.md)
- 报告写作脚手架：
  - [docs/report_scaffold_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/report_scaffold_notes.md)

---

## 3. 当前最重要的结论是什么

### Facebook 结果

`facebook_full` 上：

- `PostgreSQL + closure_3` 明显优于 `Neo4j`
- 特别是 `neighbors` 查询差距很大

### Twitter 结果

`twitter_top10000` 上：

- `Neo4j` 在 `neighbors` 和 `common_neighbors` 上明显优于 `PostgreSQL`
- `PostgreSQL` 在 `shortest_path` 上仍然更强

### 这意味着什么

这不是一个“谁永远更快”的结果，而是一个更像研究项目的结论：

- 后端优劣与数据集结构有关
- 也与查询模式有关
- `PostgreSQL + closure_3` 的优势主要来自预计算
- `Neo4j` 的优势主要来自在线图遍历在某些数据形态下更合适

### 报告里必须写明的 caveat

这一点非常重要，不能遗漏：

- 当前对比不是纯数据库引擎对引擎
- 而是 `PostgreSQL + closure_3` 对比 `Neo4j` 在线遍历

这个 caveat 已经整理在：

- [docs/experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)

---

## 4. 现在还建议做什么

按收益优先级，最建议继续做的是：

### 第一优先级：写最终报告

因为主实验结果已经齐了，继续折腾系统收益越来越低。  
最值当的是把现有材料转成正式报告。

建议直接围绕这几个文件写：

- [docs/experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)
- [docs/report_scaffold_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/report_scaffold_notes.md)
- [results/summary/facebook-full-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-p50-latency.png)
- [results/summary/twitter-top10000-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-p50-latency.png)

### 第二优先级：整理 Artifact Appendix

这一块已经有草稿，但还应该在最终报告成稿时再统一润一遍。

重点不是再加新内容，而是保证：

- 文件名真实
- 命令真实
- 仓库路径真实
- 与最终 report 中叙述完全一致

### 第三优先级：录 demo / 准备 demo

目前 demo 的最佳叙事已经比较清楚：

- 先讲研究问题
- 再讲 benchmark pipeline
- 然后展示 Facebook 结果
- 再展示 Twitter 结果
- 最后讲 JanusGraph 作为增强项

### 不太建议继续深挖的方向

当前不建议作为主线继续投入：

- 继续追 JanusGraph full benchmark
- 继续冲 full Twitter
- 继续做更大的 SNAP 图压力测试

原因很简单：

- 它们会吃掉大量时间
- 对最终交付收益不一定高
- 反而可能让报告和 demo 来不及收尾

---

## 5. 另外两个人拿到项目后怎么快速熟悉

建议让另外两位同学按照下面顺序熟悉，而不是一上来就看全部代码。

### 第一步：先看这四个文档

按顺序看：

1. [README.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/README.md)
2. [docs/runbook.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/runbook.md)
3. [docs/experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)
4. [docs/project_handover_guide_cn.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/project_handover_guide_cn.md)

只看完这四份，基本就能知道：

- 项目在干什么
- 主实验是什么
- 结果是什么
- 下一步做什么

### 第二步：只看最关键的脚本，不要先看全部源码

推荐顺序：

1. [scripts/prepare_dataset.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/prepare_dataset.py)
2. [scripts/load_neo4j.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/load_neo4j.py)
3. [scripts/load_postgres.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/load_postgres.py)
4. [scripts/run_benchmark.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/run_benchmark.py)
5. [scripts/aggregate_results.py](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/scripts/aggregate_results.py)

这五个脚本就是主实验流程。

### 第三步：只需要知道三类数据位置

另外两个人最需要记住的是：

- 数据在哪：
  - `datasets/raw/`
  - `datasets/derived/`
- workload 在哪：
  - `benchmarks/`
- 结果在哪：
  - `results/raw/`
  - `results/summary/`

### 第四步：跑一遍最短验证链路

建议他们不要一上来就重跑 Facebook/Twitter 全实验。  
最好的熟悉方式是：

1. 启动 Docker
2. 跑 `facebook_tiny`
3. 跑 `smoke_test_core_backends.py`
4. 看 summary 文件

这样能最快建立“这个项目到底怎么跑”的心理模型。

---

## 6. 团队分工现在最合理的方式

如果三个人现在并行收尾，我建议这样拆：

### 成员 A：报告主笔

负责：

- Introduction
- Method
- Experimental setup
- Results
- Conclusion

主要参考：

- [docs/experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)
- [docs/report_scaffold_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/report_scaffold_notes.md)

### 成员 B：Artifact 与文档收尾

负责：

- README 最终检查
- runbook 最终检查
- artifact appendix 最终整理
- 引用与附录

主要参考：

- [docs/runbook.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/runbook.md)
- [docs/artifact_appendix.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/artifact_appendix.md)

### 成员 C：Demo 与最终核对

负责：

- demo 讲稿
- 图表展示顺序
- 命令复现检查
- 最终 PDF/视频提交前检查

主要参考：

- [docs/demo_script.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/demo_script.md)
- [results/summary](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary)

---

## 7. 报告怎么做

### 7.1 最适合的报告主线

你们最终报告最推荐的故事线是：

1. 社交图多跳查询为什么重要
2. 我们为什么比较图数据库与关系数据库方案
3. 我们如何构建可复现 benchmark artifact
4. `facebook_full` 上为什么 `PostgreSQL + closure_3` 更强
5. `twitter_top10000` 上为什么 `Neo4j` 在邻居类查询上更强
6. JanusGraph 为什么保留为增强项而不是主矩阵
7. 我们从结果里得到什么系统层面的结论

这条线是现在仓库最能支撑的，不要讲成：

- “我们做了一个通用图数据库终极评测平台”
- 或者“JanusGraph 也是完整主实验之一”

那样会和现有证据不匹配。

### 7.2 报告写作时直接可用的材料

请重点使用：

- [docs/report_scaffold_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/report_scaffold_notes.md)
- [docs/experiment_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/experiment_notes.md)

其中：

- `report_scaffold_notes.md` 提供章节结构和写作要点
- `experiment_notes.md` 提供事实、数字、claim 和 caveat

### 7.3 报告里一定要包含的图

最推荐至少放这两张：

- [facebook-full-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/facebook-full-p50-latency.png)
- [twitter-top10000-p50-latency.png](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/results/summary/twitter-top10000-p50-latency.png)

再加一个表格：

- 数据集规模表

这样已经足够组成一版强的结果部分。

### 7.4 报告里必须写清楚的句子

必须明确写：

- `PostgreSQL` 路线使用的是 `closure_3` 预计算
- `Neo4j` 路线使用的是在线图遍历
- JanusGraph 不是主实验矩阵的一部分

这三点不写清楚，老师很可能会质疑实验公平性或完整性。

---

## 8. Demo 怎么做

### 8.1 推荐 demo 主线

最佳演示顺序：

1. 研究问题
2. 本地 benchmark pipeline
3. tiny smoke
4. Facebook 结果
5. Twitter 结果
6. JanusGraph 增强路径
7. 结论

这已经整理在：

- [docs/demo_script.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/demo_script.md)

### 8.2 Demo 不要做什么

不建议在 demo 里：

- 临场重跑大规模 Twitter 全流程
- 临场追 JanusGraph benchmark
- 临场做任何不稳定操作

推荐方式是：

- 现场展示 runbook 命令
- 展示已经跑好的结果文件和图表
- 最多演示 tiny smoke 或一个很轻的命令

### 8.3 Demo 的核心 message

Demo 里真正要让老师记住的不是你们“跑了多少命令”，而是：

- 你们做了可复现 artifact
- 你们比较了两种不同系统路线
- 两个数据集给出了不同优势模式
- 这说明后端选择和 workload / graph structure 强相关

---

## 9. 其他容易遗漏但很重要的地方

### 9.1 数据与 git

当前要特别注意：

- `twitter_combined` 原始数据和 `twitter_top10000` 派生数据体积比较大
- 现在它们已经被 `.gitignore` 排除了，避免提交过重

所以团队成员不要误以为：

- “为什么 Twitter 原始数据不在 git 里”

这是有意为之，不是丢文件。

### 9.2 容器里一次只装一个数据集

这点很重要：

- 当前本地 `Neo4j / PostgreSQL` 容器一次只对应一个当前导入的数据集
- 所以你在跑 `facebook_full` smoke 前，要先导入 `facebook_full`
- 在跑 `twitter_top10000` smoke 前，要先导入 `twitter_top10000`

这个点如果不提醒，别人很容易以为 benchmark 结果不一致是 bug。

### 9.3 不要再把 JanusGraph 扩成主线

现在最危险的误操作是：

- 团队有人觉得“JanusGraph 还没跑完整，所以要继续补”

我不建议这样做。  
当前最优策略是：

- 主矩阵已经够写报告
- JanusGraph 现在的价值是“增强项 + full-data smoke validation”
- 不要让它再次吞掉报告和 demo 的时间

### 9.4 报告一定要用自己的话写

课程说明里明确说：

- 不要用 LLM 直接生成最终 report

所以你们现在最安全的方式是：

- 用 [docs/report_scaffold_notes.md](/Users/qingynag/development/projects/study/cs5296-graph-multihop-optimization/docs/report_scaffold_notes.md) 做写作脚手架
- 再由你们自己成文

### 9.5 交付前的最后检查

最终提交前建议再做一次：

1. `python3 -m pytest -q`
2. tiny smoke
3. 检查 summary 文件是否都在
4. 检查图是否都在
5. 检查 report 中的文件名、命令名是否与仓库一致

---

## 10. 最后给团队的建议

如果从“完成作业”而不是“继续做工程”的角度看，当前项目最合理的下一步是：

1. 立刻写报告正文
2. 同时整理 artifact appendix
3. 再准备 demo
4. 只做非常小的修补，不再开新主线

当前仓库已经足够支撑：

- 一份有实验内容的 final report
- 一份可复现的 software artifact
- 一段结构清楚的 demo

所以从现在开始，最重要的不是“再做更多”，而是“把已经做出来的东西讲清楚、组织清楚、提交清楚”。
