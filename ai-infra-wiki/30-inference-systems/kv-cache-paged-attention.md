---
title: KV Cache Paged Attention
type: concept
topic: inference
component: kv-cache
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [kv-cache, paged-attention, memory, inference]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/key-papers/pagedattention-paper]
---

# KV Cache Paged Attention

## 一句话

KV cache 保存历史 token 的 key/value，避免每次 decode 重算整个上下文。Paged KV / PagedAttention 把 KV cache 管成页，减少碎片和过度预留，是现代 LLM serving 的核心机制之一。

## KV cache 公式

粗略估算：

```text
KV bytes = batch * seq_len * num_layers * 2 * kv_heads * head_dim * dtype_bytes
```

解释：

- `2` 代表 K 和 V。
- GQA/MQA 会让 `kv_heads < query_heads`，显存更省。
- batch 和 seq_len 是 serving 并发容量的主要乘数。
- 这个公式必须明确口径：单 GPU 容量估算应使用 per-rank 的 `kv_heads`、per-rank 可用显存和该 rank 实际持有的 KV；整个 TP group 容量估算才使用聚合显存和全局 KV 口径。
- 在 tensor parallel、pipeline parallel、KV offload 或 disaggregated serving 中，KV 是否按 rank 切分取决于 runtime 的 attention/KV 布局，不能直接把单卡公式套到全副本。

## 为什么需要 paging

朴素 KV 分配常按最大序列长度为每个请求预留连续空间：

- 短请求浪费大量空间。
- 请求长度动态增长，连续扩容困难。
- batch 中请求结束时间不同，容易碎片化。

Paged KV 把 KV cache 切成固定大小 block/page，请求只持有实际用到的 page。调度器通过 block table 把逻辑 token 位置映射到物理 KV page。

## 系统收益

- 降低 KV 内存浪费。
- 支持 continuous batching 中请求动态加入/退出。
- 支持 prefix cache、共享前缀、copy-on-write 等优化。
- 提高在长上下文和高并发场景下的可用 batch。

## 代价与边界

- attention kernel 需要支持分页索引。
- block size 影响碎片和 kernel 效率。
- prefix cache 命中率低时可能只增加管理成本。
- KV cache 不足时要选择 reject、preempt、swap 或降低并发。

## 观测点

- allocated blocks / free blocks。
- KV cache utilization。
- prefix cache hit rate。
- request preemption / eviction 次数。
- OOM 或 admission rejection 原因。

## 本地证据

- 暂无 `raw-sources/` 下的 block size / hit rate / OOM trace 样本。
- 章节中 KV cache 公式、paged attention 收益与代价属于对 vLLM 文档 + PagedAttention 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/inference/<runtime>-kv-<commit>.md`，含 block size 调参记录、prefix cache 命中率与 TTFT / TPOT 关系、rejection / preemption 次数。

## 尚未本地验证的边界

- KV cache 公式在 TP / PP / disaggregated serving 下口径不同，本页已在公式段说明，但并未用本机数据复现。
- “block size 影响碎片和 kernel 效率”是经验结论，block size 1k vs 8k 的实际差距需用本地 benchmark 验证。
- paged attention 的“前缀 cache 收益”与具体 workload 相关，不能用单一数字泛化。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/key-papers/pagedattention-paper]]

## 相关页面

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/batching-scheduling]]
- [[80-playbooks/serving-capacity-planning]]
- [[70-sources/key-papers/pagedattention-paper]]
