---
title: Current Repository Gaps
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-09-23
owner: local
reliability: high
tags: [maintenance, design, gaps, progressive-loading]
---

# Current Repository Gaps

## 结论

当前仓库已经具备 AI Infra 学习 Wiki 的主体结构：概念页、source card、实验页、playbook、索引、BM25 检索和维护审计都已经存在。下一阶段的重点是把这些内容组织成一个可渐进加载、可被不同 Agent 复用、可从中断位置继续的学习底座。

当前项目协议已经覆盖首批主题，剩余工作集中在课程内容深度、真实证据和运行环境说明，内容层继续保持 Markdown、YAML front matter 和原始证据分层。

## 本轮实现后的状态

- 已加入五个 progressive-loading bundle，覆盖推理、分布式训练、NCCL、serving 和 Wiki/RAG。
- 已加入学习 Prompt、实验 Prompt、checkpoint Prompt 和工具能力清单。
- 已加入五个主题 Checklist、共享 checkpoint 模板、checkpoint 记录脚本和学习状态汇总脚本。
- loader 已支持单阶段加载和 `--through` 连续阶段加载。
- Wiki lint、SQLite 索引构建、索引一致性检查和跨平台路径归一化已经通过验证。

因此，原先集中在协议层的结构缺口已经转化为可运行的项目协议。当前需要继续补充的是知识深度、真实运行证据和环境覆盖。

## 现有基础

- `ai-infra-wiki/` 已按 index、roadmap、workflow、concept、source、playbook、experiment 分层。
- `raw-sources/` 提供不可变的原始资料边界。
- `scripts/` 已提供 front matter 解析、lint、SQLite FTS5/BM25 索引、搜索和可运行实验脚本。
- `01-roadmap/` 已提供 90 天课程和 competency matrix。
- `00-index/question-bank.md` 已提供主题化自测问题。
- 页面已使用 `topic`、`component`、`level`、`reliability` 等字段支持检索和学习路径组织。

这些基础适合继续增加轻量的项目协议，而不需要重构现有 Wiki。

## 当前固有不足与完成状态

### 1. 任务级加载包已形成首批主题

现有 index 和 BM25 继续负责查找页面，`packs/` 已经用 bundle 表达：

- 一个学习目标需要哪些页面；
- 页面按照什么阶段加载；
- 哪些内容属于核心、实践和深入阅读；
- 目标完成后使用哪个 Checklist 和 checkpoint。

当前已落地 `inference.mha-kv-cache`、`training.ddp-fsdp`、`training.nccl-performance`、`serving.capacity-planning` 和 `rag.wiki-retrieval` 五个主题包。

### 2. Agent-agnostic Prompt Pack 已形成

`prompts/` 已提供学习、实验和 checkpoint 记录的通用 Prompt。Prompt 直接描述目标、输入、加载顺序、证据标准和输出格式，Agent 通过自己的工具适配执行。

### 3. 工具能力契约已集中描述

`tools/manifest.yml` 已登记搜索、索引、lint、bundle 加载、学习检查、checkpoint 记录和实验入口，并说明：

- 用途；
- 输入和输出；
- 是否写入文件；
- 运行前置条件；
- 验证方式。

不同 Agent 可以按照同一份能力清单映射本地 CLI、MCP 或其他工具接口。

### 4. 学习状态已具备可移植的 Checkpoint

`checkpoints/template.yml` 保存学习目标、已加载页面、完成项、证据、开放问题和下一步阶段；`scripts/record_checkpoint.py` 可以创建或更新 checkpoint。

学习状态使用人类可读 YAML，让不同 Agent 和人类继续同一个学习任务。

### 5. Checklist 已成为学习验收接口

五个主题 Checklist 把 question bank、competency matrix 和实验页连接成逐项验收标准，用来记录：

- 能否解释概念；
- 能否写出公式和 shape；
- 能否运行对应代码；
- 能否给出实验依据；
- 能否说明适用边界。

Checklist 将“读过页面”转化为“完成了可验证学习任务”。

### 6. 课程基础与代码练习之间还有连接空档

当前 backlog 已指出 Transformer architecture、Attention、MLP、RMSNorm、RoPE 等页面需要继续补充。当前 `softmax.py`、`MHA.py`、`GQA.py` 等学习代码很适合成为推理主线的入口，但还没有一个任务包把代码、概念页、KV Cache、batching 和 benchmark 串起来。

当前主题包已经把代码入口、KV Cache、batching 和 benchmark 连接起来。剩余内容是补充 Attention、MLP、RMSNorm、RoPE 等模型结构页面，让代码练习拥有更完整的理论前置。

### 7. 复现实验入口需要更清楚的环境说明

现有实验脚本和实验文档已经具备教学价值。项目根目录还需要集中说明 Python、PyTorch、CUDA、GPU 数量和 CPU fallback 等运行条件，帮助学生选择适合自己机器的路径。

当前仍需要集中说明 Python、PyTorch、CUDA、GPU 数量和 CPU fallback 等运行条件。本项目继续使用学习仓库适合的环境说明，不引入环境锁定、容器编排或生产级依赖管理。

### 8. 当前证据层仍处于教学样例阶段

当前 raw artifact note 已经建立了结构，但主要内容标记为 `local-simulated`，部分 note 中声明的 JSONL/YAML 原始输出仍待真实运行生成。概念页中的性能结论应继续依赖页面上的“本地证据”和“尚未本地验证的边界”来理解。

项目继续保留这个证据边界，真实运行后以新版本 artifact 更新教学样例。

### 9. 维护记录需要跟随实际状态更新

`00-index/raw-sources-index.md` 的入站 wikilink 已补齐，操作日志已记录当前实现和验证结果。历史审计保留历史状态，后续每轮更新继续追加新的验证记录。

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
| P1 | 渐进加载 | 五个可运行的主题 bundle，支持单阶段和连续阶段输出 |
| P1 | 学习记录 | 五个主题 checklist、共享 checkpoint 模板和记录脚本 |
| P1 | 维护一致性 | 修复 orphan page、更新操作日志、lint 和索引检查通过 |
| P2 | 课程深化 | 补 Attention/Transformer 页面和更多主题练习 |
| P2 | 真实证据 | 用真实 GPU、serving 和 trace 输出替换教学样例 |
