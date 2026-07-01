---
title: Prefix Cache Chunked Prefill Preemption
type: concept
topic: inference
component: serving-optimization
level: advanced
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [prefix-cache, chunked-prefill, preemption, scheduler]
source_refs: [70-sources/official-docs]
---

# Prefix Cache Chunked Prefill Preemption

## 一句话

高级 LLM serving 优化围绕 scheduler 和 KV cache 状态：prefix/radix cache 复用已有前缀，chunked prefill 把长 prompt 切成调度单元，preemption/swap 在 KV 紧张时保护 SLO。

## Prefix / Radix Cache

适合系统 prompt、few-shot prefix、agent 模板高度重复的 workload。命中后可以复用 prefix KV，降低 TTFT 和 prefill compute。

关键指标：

- prefix cache hit rate。
- saved prefill tokens。
- cache memory overhead。
- eviction rate。

## Chunked Prefill

长 prompt prefill 会阻塞 decode。chunked prefill 把 prompt 切块，让 scheduler 在 prefill 块和 decode iteration 之间交错。

收益：降低长 prompt 对在线 decode 的阻塞。代价：调度复杂、kernel launch/状态管理增加。

## Preemption / Swap

KV cache 不足时，runtime 需要选择：

- reject 新请求。
- preempt 低优先级请求。
- swap KV 到 CPU/host memory。
- 降低 batch 或 max context。

swap 能保留请求，但会增加 PCIe/CPU 内存路径延迟；preemption 需要公平性和用户体验策略。

## 验收问题

1. 开 prefix cache 后，重复 prompt 的 TTFT 是否下降？
2. 长 prompt 混合短 decode 时，chunked prefill 是否改善 p95 TPOT？
3. KV cache 压力下，runtime 是 reject、preempt 还是 swap？
4. 这些策略是否改变输出质量或请求公平性？

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/distserve-paper]]

## 相关页面

- [[30-inference-systems/batching-scheduling]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[90-experiments/vllm-sglang-benchmark-harness]]
