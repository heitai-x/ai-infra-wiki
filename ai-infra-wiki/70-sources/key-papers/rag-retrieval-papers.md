---
title: RAG And Retrieval Papers
type: source
source_type: paper
source_url: https://arxiv.org/abs/2005.11401
topic: rag
component: retrieval
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [paper, rag, retrieval, rerank, agent]
---

# RAG And Retrieval Papers

## Why It Matters

`50-rag-agent-infra/embedding-retrieval-agent-infra` 与 `50-rag-agent-infra/evaluation-feedback-loop` 的 pipeline 设计、chunking、hybrid search、rerank、agent runtime 和评测指标，都需要追溯到 RAG 原始论文、retrieel evaluation 论文和 agent runtime 论文，避免把工程经验当成算法结论。

## Key Claims

- RAG 论文给出 retrieve-then-generate 的标准形式和 retrieve / generate 解耦的动机。
- 后续工作讨论 hybrid search（BM25 + dense）、rerank、citation、groundedness 的评估方法。
- Agent 论文讨论 tool calling、planning、memory、state management 和安全边界。
- RAGAS / TruLens / Arethusa 等评测框架定义 groundedness、context relevance、answer relevance 指标。
- 评测论文给出 Recall@k、Citation accuracy、Task success 等指标的口径。

## Limits Or Caveats

- 论文结论与今天的 embedding 模型、reranker、LLM 和 agent runtime 差异较大。
- 评测指标在不同数据集和语言上表现不同，不能照搬数字。
- 引用时需要明确是 RAG / rerank / agent / evaluation 中的哪一个。

## Links To Concepts

- [[50-rag-agent-infra/embedding-retrieval-agent-infra]]
- [[50-rag-agent-infra/evaluation-feedback-loop]]
- [[02-llm-wiki-workflow/rag-metadata-schema]]

## Follow Up

- 后续按 RAG / rerank / agent / RAGAS 分别建独立 source card。
- 后续补真实评测集到 `raw-sources/rag/`。
