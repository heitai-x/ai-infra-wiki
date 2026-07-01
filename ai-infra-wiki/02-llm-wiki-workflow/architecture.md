---
title: LLM Wiki Architecture
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [llm-wiki, architecture, obsidian, rag]
---

# LLM Wiki Architecture

本 Wiki 采用 Karpathy 风格的 LLM Wiki 思路：让 AI 代理维护本地 Markdown 知识库，把原始资料、研究过程、实验结果和排障经验结构化成可检索的长期记忆。

## 三层对齐

标准 `llm_wiki` 的核心是三层：

1. Raw sources：仓库根目录 `raw-sources/`，作为不可变证据层。
2. Wiki：`ai-infra-wiki/`，保存 agent 维护的结构化 Markdown。
3. Schema：`AGENTS.md`、`.ai-wiki.yml` 与 `02-llm-wiki-workflow/`，定义构建规则和维护流程。

## Wiki 内部分层

1. Index：`00-index/`，提供主题入口、概念索引、source 索引、问题库。
2. Entities：`04-entities/`，记录框架、硬件、平台组件等对象页。
3. Concepts：`10-*` 到 `50-*`，记录稳定概念、系统模型和学习路径。
4. Sources：`70-sources/`，记录官方文档、论文、代码、内部资料的摘要和可信度。
5. Practice：`80-playbooks/` 与 `90-experiments/`，记录排障流程和可复现实验。

## 工作流

详细 ingestion 规范见 [[02-llm-wiki-workflow/ingest-workflow]]。

```text
Raw input
  -> Ingest: 提取事实、术语、命令、图、限制、来源
  -> Structure: 放入 Concepts / Sources / Playbooks / Experiments
  -> Index: 更新 topic、concept、source、question 索引
  -> Log: 记录到 [[00-index/log]]
  -> Link: 添加双向链接和 prerequisite / next links
  -> Lint: 检查 front matter、死链、来源、更新时间
  -> Audit: 更新 [[99-maintenance/content-coverage-audit]]
  -> Eval: 用 question bank 测 Wiki/RAG 是否能回答
```

## 设计取舍

- Markdown 优先：便于 Git diff、AI 读写、Obsidian 双链和 RAG ingestion。
- source card 优先于长篇复制：保留摘要、关键机制、引用位置和可信度，不复制全文。
- 细粒度概念页：便于 chunking 和增量维护。
- 每个性能结论必须绑定证据：硬件、模型、框架版本、命令、指标、原始输出。
- lint/index 只读取受控输入：忽略 `.ipynb_checkpoints` 等临时目录，避免构建被编辑器垃圾文件污染。

## RAG 检索策略

推荐 hybrid search：

- keyword/BM25：召回术语、参数名、错误码、命令。
- vector：召回语义相近的概念和解释。
- metadata filter：按 topic、component、source_type、level、reliability 过滤。
- reranker：对多个候选笔记重新排序。

当前 v1 已落地 [[02-llm-wiki-workflow/local-indexing]]：SQLite FTS5/BM25 本地检索。向量索引和 rerank 是后续扩展。

回答策略：

1. 先检索 Index，再检索 Concepts，再检索 Sources/Playbooks。
2. 对 API 或命令问题优先引用官方文档。
3. 对机制问题优先引用概念页和论文 source card。
4. 对性能问题优先引用实验、benchmark、trace 或 playbook。
