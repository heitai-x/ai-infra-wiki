---
title: Current Repository Gaps
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-09-22
owner: local
reliability: high
tags: [maintenance, design, gaps, progressive-loading]
---

# Current Repository Gaps

## 结论

当前仓库已经具备 AI Infra 学习 Wiki 的主体结构：概念页、source card、实验页、playbook、索引、BM25 检索和维护审计都已经存在。下一阶段的重点是把这些内容组织成一个可渐进加载、可被不同 Agent 复用、可从中断位置继续的学习底座。

当前缺口集中在项目协议和学习状态层，内容层本身继续保持 Markdown、YAML front matter 和原始证据分层。

## 现有基础

- `ai-infra-wiki/` 已按 index、roadmap、workflow、concept、source、playbook、experiment 分层。
- `raw-sources/` 提供不可变的原始资料边界。
- `scripts/` 已提供 front matter 解析、lint、SQLite FTS5/BM25 索引、搜索和可运行实验脚本。
- `01-roadmap/` 已提供 90 天课程和 competency matrix。
- `00-index/question-bank.md` 已提供主题化自测问题。
- 页面已使用 `topic`、`component`、`level`、`reliability` 等字段支持检索和学习路径组织。

这些基础适合继续增加轻量的项目协议，而不需要重构现有 Wiki。

## 当前固有不足

### 1. 内容有索引，缺少任务级加载包

现有 index 能帮助人查找页面，BM25 能帮助脚本搜索页面，但项目还没有用一个小型清单表达：

- 一个学习目标需要哪些页面；
- 页面应该按什么顺序加载；
- 哪些内容是核心，哪些内容是深入阅读；
- 该目标完成后需要提交什么证据。

这使渐进式加载主要依赖使用者自行判断。

### 2. 缺少与 Agent 无关的 Prompt Pack

Wiki 中已有协作规则和写作规范，但还没有独立的、可组合的任务 Prompt。学习、实验、ingest、审计和复盘需要共享相同的证据标准与输出结构。

项目需要提供任务 Prompt 文件，Prompt 只描述目标、输入、加载顺序和输出格式，不绑定某个 Agent 的 API 或记忆实现。

### 3. 工具已经存在，能力契约尚未集中描述

`scripts/` 中已经有搜索、索引、lint 和实验入口，但项目还没有一份简洁的工具清单说明每个入口的：

- 用途；
- 输入和输出；
- 是否写入文件；
- 运行前置条件；
- 验证方式。

不同 Agent 因此需要自行理解脚本约定。

### 4. 学习状态缺少可移植的 Checkpoint

当前有 `00-index/log.md`，它适合记录 Wiki 变更时间线；学习过程还需要记录当前目标、已加载页面、已完成练习、已有证据、未解决问题和下一步加载阶段。

这类状态应该保存成仓库中的人类可读 YAML，让不同 Agent 和人类都能继续同一个学习任务。

### 5. Checklist 还没有成为学习验收接口

问题库描述了应该会回答什么问题，competency matrix 描述了能力层级，实验页描述了实验目标。三者之间还缺少一个逐项验收清单，用来记录：

- 能否解释概念；
- 能否写出公式和 shape；
- 能否运行对应代码；
- 能否给出实验依据；
- 能否说明适用边界。

Checklist 可以把“读过页面”转化为“完成了可验证学习任务”。

### 6. 课程基础与代码练习之间还有连接空档

当前 backlog 已指出 Transformer architecture、Attention、MLP、RMSNorm、RoPE 等页面需要继续补充。当前 `softmax.py`、`MHA.py`、`GQA.py` 等学习代码很适合成为推理主线的入口，但还没有一个任务包把代码、概念页、KV Cache、batching 和 benchmark 串起来。

本轮先建立 `inference.mha-kv-cache` 学习包，后续再补齐模型结构页面。

### 7. 复现实验入口需要更清楚的环境说明

现有实验脚本和实验文档已经具备教学价值。项目根目录还需要集中说明 Python、PyTorch、CUDA、GPU 数量和 CPU fallback 等运行条件，帮助学生选择适合自己机器的路径。

本轮保持实验脚本轻量，不引入环境锁定、容器编排或生产级依赖管理。

### 8. 当前证据层仍处于教学样例阶段

当前 raw artifact note 已经建立了结构，但主要内容标记为 `local-simulated`，部分 note 中声明的 JSONL/YAML 原始输出仍待真实运行生成。概念页中的性能结论应继续依赖页面上的“本地证据”和“尚未本地验证的边界”来理解。

本轮实现会保留这个证据边界，不把模拟数据升级为真实 benchmark。

### 9. 维护记录需要跟随实际状态更新

当前仓库运行 lint 时发现 `00-index/raw-sources-index.md` 缺少入站 wikilink，而历史审计记录中保留了此前的 `wiki_lint=ok`。下一轮应补入口链接，并在操作日志中记录新的验证结果。

## 本轮保持的设计边界

- Wiki 继续使用 Markdown 和 YAML front matter。
- 渐进加载使用简单的 YAML bundle，不引入复杂图数据库或任务编排服务。
- Prompt 使用普通 Markdown，不绑定 Codex、Claude 或其他 Agent 的私有格式。
- 工具层只描述能力契约，已有 Python 脚本继续作为主要实现。
- Checkpoint 和 Checklist 使用人类可读 YAML，支持 Git diff 和手工修改。
- 当前检索继续使用 SQLite FTS5/BM25；向量索引和 rerank 保留为后续扩展。
- 当前不加入全量文件 hash、复杂缓存失效系统、远程状态服务或自动 Agent runtime。

## 缺口优先级

| 优先级 | 目标 | 交付结果 |
|---|---|---|
| P0 | 项目协议 | 两份设计文档、bundle、Prompt、工具清单、checkpoint/checklist 模板 |
| P1 | 渐进加载 | 一个可运行的 bundle loader，支持按阶段输出上下文 |
| P1 | 学习记录 | 一个主题 checklist 和一个可复制的 study checkpoint |
| P1 | 维护一致性 | 修复 orphan page，更新操作日志，lint 通过 |
| P2 | 课程深化 | 补 Attention/Transformer 页面和更多主题 bundle |
| P2 | 真实证据 | 用真实 GPU、serving 和 trace 输出替换教学样例 |
