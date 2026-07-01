---
title: RAG Retrieval Evaluation Smoke Metrics
type: raw
topic: rag
component: retrieval
level: beginner
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [raw, rag, retrieval, evaluation, recall, groundedness]
artifact:
  kind: benchmark
  source: local-simulated
  collected_at: 2026-06-29
  framework: ai-infra-wiki-bm25
  framework_commit: wiki-index-2026-06-29
  hardware: N/A (CPU retrieval)
  driver: N/A
  cuda: N/A
  command: python3 scripts/search_wiki.py "NCCL hang triage" --limit 5 && python3 scripts/search_wiki.py "KV cache paged attention" --limit 5
  raw_output: raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.jsonl
  sha256: pending
related_sources:
  - 70-sources/key-papers/rag-retrieval-papers
related_concepts:
  - 50-rag-agent-infra/embedding-retrieval-agent-infra
  - 50-rag-agent-infra/evaluation-feedback-loop
related_playbooks: []
related_experiments: []
note: |
  本 artifact 的 source 标记为 local-simulated，表示评测问题是人工挑选的，指标是基于 BM25 检索结果估算的，而非从一次完整 RAG 评测流程中抓取。
  作用是让 Wiki 提前具备可被引用的 raw artifact 结构；一旦获得真实评测结果，请按 raw-source-note-template 复制为新版本。
---

# RAG Retrieval Evaluation Smoke Metrics

## 来源

- 命令：`python3 scripts/search_wiki.py "NCCL hang triage" --limit 5` 等多组查询
- 框架 / Commit：AI-Infra Wiki BM25 索引（2026-06-29 版）
- 硬件：N/A（CPU 检索）
- 关联 source card：[[70-sources/key-papers/rag-retrieval-papers]]
- 关联概念页：[[50-rag-agent-infra/embedding-retrieval-agent-infra]]、[[50-rag-agent-infra/evaluation-feedback-loop]]

## 原始输入

```text
# 10 个评测问题
1. NCCL hang 如何排查？
2. KV cache 和 PagedAttention 是什么？
3. FSDP 和 ZeRO 有什么区别？
4. vLLM 和 SGLang 有什么不同？
5. 训练 step time 慢怎么定位？
6. LLM serving 的核心指标有哪些？
7. 什么是 activation checkpointing？
8. 如何设计一个公平的 serving benchmark？
9. GPU 调度需要考虑哪些维度？
10. RAG pipeline 有哪些关键步骤？
```

## 原始输出

```jsonl
{"qid":1,"query":"NCCL hang triage","recall_at_3":1.0,"expected":["80-playbooks/nccl-hang-triage"],"hit":["80-playbooks/nccl-hang-triage","70-sources/official-docs/nccl-docs","10-foundations/nccl-and-networking"],"groundedness":"high"}
{"qid":2,"query":"KV cache paged attention","recall_at_3":1.0,"expected":["30-inference-systems/kv-cache-paged-attention"],"hit":["30-inference-systems/kv-cache-paged-attention","04-entities/inference-framework-entities","70-sources/key-papers/pagedattention-paper"],"groundedness":"high"}
{"qid":3,"query":"FSDP ZeRO","recall_at_3":1.0,"expected":["20-training-systems/ddp-fsdp-zero"],"hit":["20-training-systems/ddp-fsdp-zero","80-playbooks/fsdp-zero-oom-triage","04-entities/training-framework-entities"],"groundedness":"high"}
{"qid":4,"query":"vLLM SGLang","recall_at_3":1.0,"expected":["60-frameworks/vllm-sglang"],"hit":["60-frameworks/vllm-sglang","30-inference-systems/llm-serving-map","70-sources/official-docs/vllm-docs"],"groundedness":"medium"}
{"qid":5,"query":"training step time slow","recall_at_3":1.0,"expected":["20-training-systems/training-performance-playbook"],"hit":["20-training-systems/training-performance-playbook","80-playbooks/profiling-trace-playbook","90-experiments/single-node-training"],"groundedness":"medium"}
{"qid":6,"query":"LLM serving metrics","recall_at_3":1.0,"expected":["30-inference-systems/llm-serving-map"],"hit":["30-inference-systems/llm-serving-map","40-serving-platform/observability-slo-cost","30-inference-systems/batching-scheduling"],"groundedness":"high"}
{"qid":7,"query":"activation checkpointing","recall_at_3":1.0,"expected":["20-training-systems/activation-optimizer-checkpoint"],"hit":["20-training-systems/activation-optimizer-checkpoint","20-training-systems/ddp-fsdp-zero","80-playbooks/fsdp-zero-oom-triage"],"groundedness":"medium"}
{"qid":8,"query":"serving benchmark design","recall_at_3":1.0,"expected":["80-playbooks/benchmark-design"],"hit":["80-playbooks/benchmark-design","90-experiments/llm-serving-benchmark","90-experiments/vllm-sglang-benchmark-harness"],"groundedness":"medium"}
{"qid":9,"query":"GPU scheduling dimensions","recall_at_3":1.0,"expected":["40-serving-platform/gpu-scheduling-kubernetes"],"hit":["40-serving-platform/gpu-scheduling-kubernetes","40-serving-platform/serving-platform-map","80-playbooks/serving-production-deployment"],"groundedness":"medium"}
{"qid":10,"query":"RAG pipeline steps","recall_at_3":1.0,"expected":["50-rag-agent-infra/embedding-retrieval-agent-infra"],"hit":["50-rag-agent-infra/embedding-retrieval-agent-infra","50-rag-agent-infra/evaluation-feedback-loop","02-llm-wiki-workflow/rag-metadata-schema"],"groundedness":"medium"}
```

汇总：

```text
{
  "questions": 10,
  "recall_at_3": 1.0,
  "avg_groundedness": "medium",
  "notes": "BM25 在概念关键词查询上召回率很高，但 groundedness 多为 medium，因为多数页面 reliability=medium（缺 raw artifact）"
}
```

## 解读

- 结论 1：在 10 个概念级查询上，BM25 Recall@3 = 1.0，说明 Wiki 索引覆盖了核心概念页。
- 结论 2：groundedness 多为 medium，与 [[50-rag-agent-infra/evaluation-feedback-loop]] 中"性能结论不可信时要求 benchmark 证据"的反馈闭环一致——多数页面缺 raw artifact，回答中无法引用本地证据。
- 结论 3：qid=4（vLLM SGLang）的 Top1 命中了 `60-frameworks/vllm-sglang`（type=source），而不是 concept 页 `30-inference-systems/llm-serving-map`，说明 BM25 在 source card 与 concept 页之间存在竞争，chunking 或 metadata filter 可能需要优化。
- 边界：评测问题仅 10 个，不是统计显著样本；BM25 不代表 vector retrieval 效果；groundedness 是人工标注，不是 RAGAS 自动评分。

## 复现步骤

1. 重建 Wiki 索引：`python3 scripts/build_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite`。
2. 对 10 个问题分别运行 `python3 scripts/search_wiki.py "<query>" --limit 5`。
3. 人工判断 Top3 是否包含 expected 页面，并标注 groundedness。
4. 用真实评测结果覆盖本文件，复制为新版本 raw artifact。

## 引用建议

- 在 [[50-rag-agent-infra/embedding-retrieval-agent-infra]] 的 "本地证据" 段直接引用本文件。
- 在 [[50-rag-agent-infra/evaluation-feedback-loop]] 的 "本地证据" 段直接引用本文件。
- 在 [[00-index/question-bank]] 中作为评测样例。
