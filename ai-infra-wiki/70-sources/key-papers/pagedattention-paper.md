---
title: PagedAttention Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/2309.06180
topic: inference
component: kv-cache
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, pagedattention, kv-cache, vllm]
---

# PagedAttention Paper

## Why It Matters

PagedAttention 论文是 KV cache 分页管理和高吞吐 LLM serving 的关键论文，是理解 paged KV、block table 与内存碎片控制的核心来源。

## Key Claims

- 论文提出通过分页式 KV 管理减少碎片和过度预留。
- block/page 管理让 continuous batching 与动态请求生命周期更容易落地。
- serving 吞吐和 KV 利用率的提升，很大程度来自内存管理而不只是算力提升。

## Limits Or Caveats

- 论文结论与具体实现密切相关，不等于所有 runtime 都有相同行为。
- 真实收益依赖 workload、prompt 分布、cache 命中和 kernel 路径。

## Links To Concepts

- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/batching-scheduling]]
- [[30-inference-systems/llm-serving-map]]

## Follow Up

- 后续补 block size、prefix cache 和 preemption 的实现差异说明。
