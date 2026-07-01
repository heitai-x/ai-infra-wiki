---
title: Embedding Retrieval Agent Infra
type: concept
topic: rag
component: retrieval
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [rag, embedding, retrieval, agent]
sources: [../raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.md]
source_refs: [70-sources/key-papers/rag-retrieval-papers, 70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs]
---

# Embedding Retrieval Agent Infra

## 一句话

RAG/Agent Infra 解决的是“模型如何使用外部知识、工具和反馈”。它和模型 serving 相连，但不是同一个系统层次。

## RAG pipeline

```text
documents -> parsing -> chunking -> metadata -> embeddings/index
query -> rewrite -> hybrid retrieval -> rerank -> context assembly -> generation -> citation/eval
```

## Chunking

AI Infra Wiki 的 chunking 应保留：

- front matter。
- 标题层级。
- source URL 和 last_checked。
- 表格表头。
- 命令和配置完整块。
- 概念页之间的 wikilinks。

## Hybrid search

- BM25/keyword：适合 `NCCL_DEBUG`、`--tensor-parallel-size`、错误码、函数名。
- Vector：适合“为什么 decode memory-bound”这类语义问题。
- Metadata filter：限定 topic/component/reliability/status。
- Reranker：解决召回太多时的排序。

## Agent runtime

Agent runtime 在 RAG 之上增加：

- tool calling。
- 多步计划。
- 状态管理。
- memory 更新。
- 安全边界和权限。
- 任务审计。

对 AI Infra 来说，agent 可以执行 benchmark、读 profiler、跑 lint、更新 Wiki，但必须保留证据和命令。

## 本地证据

- 已落地 raw artifact：`raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.md`（10 个概念级查询的 Recall@3 + groundedness 评测）。
- 指标为 local-simulated，结构真实可用；升级到 `reliability: high` 是因为现在同时具备：RAG 论文 + 本地 raw artifact。
- 进一步提升可信度的条件：用 RAGAS / TruLens 自动评分 + 更大评测集覆盖，并复制为新版本 raw artifact。

## 尚未本地验证的边界

- “BM25 适合错误码、函数名；vector 适合语义问题” 是经验判断，本页未引用本机 A/B 数据。
- chunking 规则（保留 front matter / 标题 / source URL）是 Wiki 自身约定，不等于通用 RAG 最佳实践。
- agent runtime 安全边界和权限是策略方向，没有具体实现或审计日志样本。

## 来源

- [[70-sources/key-papers/rag-retrieval-papers]]
- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]

## 相关页面

- [[02-llm-wiki-workflow/architecture]]
- [[02-llm-wiki-workflow/rag-metadata-schema]]
- [[50-rag-agent-infra/evaluation-feedback-loop]]
