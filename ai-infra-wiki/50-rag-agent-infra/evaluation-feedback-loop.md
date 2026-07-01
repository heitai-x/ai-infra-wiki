---
title: Evaluation Feedback Loop
type: concept
topic: rag
component: evaluation
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [evaluation, feedback, rag, llmops]
sources: [../raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.md]
source_refs: [70-sources/key-papers/rag-retrieval-papers, 70-sources/official-docs/slo-observability-docs]
---

# Evaluation Feedback Loop

## 一句话

AI Infra Wiki/RAG 必须被评测，否则它只是资料集合。评测问题应覆盖概念、API、排障、性能、学习路线五类场景。

## 离线评测

使用 [[00-index/question-bank]] 构造 50-100 个问题：

- 答案是否引用正确页面。
- 是否区分官方事实、论文结论和本地经验。
- 是否给出可执行下一步。
- 是否拒绝无证据的性能断言。
- 是否能定位到 source card。

## 在线反馈

记录用户每次追问：

- 找不到资料：补 index 或概念页。
- 回答过泛：补 playbook 或实验。
- 引用不准：改 chunking 或 metadata。
- API 过期：更新 source card 状态。
- 性能结论不可信：要求 benchmark 证据。

## Wiki 更新闭环

```text
question -> retrieval miss or weak answer
  -> identify missing source/concept/playbook
  -> ingest/update note
  -> update index/question bank
  -> rerun eval
```

## 指标

- Recall@k：相关页面是否被召回。
- Citation accuracy：引用是否支持回答。
- Answer groundedness：是否有无来源断言。
- Task success：用户是否能完成实验/排障。
- Freshness：source last_checked 是否过期。

## 本地证据

- 已落地 raw artifact：`raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.md`（10 个概念级查询的 Recall@3 + groundedness 评测）。
- 指标为 local-simulated，结构真实可用；升级到 `reliability: high` 是因为现在同时具备：RAG / evaluation 论文 + SRE 观测文献 + 本地 raw artifact。
- 进一步提升可信度的条件：用真实在线反馈日志 + 更大评测集覆盖，并复制为新版本 raw artifact。

## 尚未本地验证的边界

- “50-100 个问题”是经验规模，不是经过统计显著性检验的样本量。
- Recall@k / Citation accuracy / groundedness 的口径依赖评测框架，本页未引用具体实现。
- 在线反馈“找不到资料 / 回答过泛 / 引用不准 / API 过期 / 性能结论不可信”是分类启发，不等于实际线上分布。

## 来源

- [[70-sources/key-papers/rag-retrieval-papers]]
- [[70-sources/official-docs/slo-observability-docs]]

## 相关页面

- [[02-llm-wiki-workflow/lint-and-maintenance]]
- [[00-index/question-bank]]
- [[02-llm-wiki-workflow/rag-metadata-schema]]
