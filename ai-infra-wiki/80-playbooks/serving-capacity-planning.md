---
title: Serving Capacity Planning
type: playbook
topic: inference
component: capacity-planning
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [serving, capacity, kv-cache, slo]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/official-docs/tensorrt-llm-docs, 70-sources/key-papers/pagedattention-paper, 70-sources/key-papers/distserve-paper, 70-sources/key-papers/flashattention-papers]
---

# Serving Capacity Planning

## 目标

在给定模型、GPU、precision、context length、SLO 和 workload 下，估算需要多少 GPU、副本、KV cache 和并发上限。

## 输入

- 模型：参数量、layers、hidden、heads、kv_heads、head_dim。
- Precision：weights dtype、KV dtype、quantization。
- GPU：型号、显存、互联、数量。
- Workload：prompt length 分布、output length 分布、QPS、并发。
- SLO：TTFT、TPOT、端到端 latency、拒绝率。
- Runtime：vLLM/SGLang/TensorRT-LLM 参数。

## 显存估算

单 GPU / 单 rank 口径：

```text
available_for_kv_per_rank = gpu_memory_per_rank
  - model_weights_per_rank
  - runtime_workspace_per_rank
  - cuda_graph_pools_per_rank
  - fragmentation_margin_per_rank
```

```text
kv_per_token_per_rank = layers_held_by_rank * 2 * kv_heads_held_by_rank * head_dim * dtype_bytes
max_tokens_in_kv_per_rank = available_for_kv_per_rank / kv_per_token_per_rank
```

全副本口径必须把 TP/PP/DP 的 rank 布局展开后再聚合，不能把全局 `kv_heads` 和单卡可用显存混用。

并发上限粗略：

```text
max_concurrency ~= min_rank(max_tokens_in_kv_per_rank) / average_total_sequence_length
```

## 性能估算

- Prefill 容量看 prompt tokens/sec。
- Decode 容量看 generation tokens/sec 和 TPOT。
- 混合 workload 下分开测 prefill-heavy、decode-heavy、真实分布。
- capacity 不能只按平均长度，要看 p95/p99 长度。

## 运行时参数检查

- max model len。
- max num seqs。
- max batched tokens。
- tensor parallel size。
- GPU memory utilization。
- enable prefix cache / chunked prefill。
- quantization / KV dtype。

## 输出模板

```text
model:
gpu:
runtime:
SLO:
expected workload:
capacity estimate:
  max concurrent seqs:
  max total tokens in KV:
  expected TTFT:
  expected TPOT:
risks:
  long-context tail:
  KV fragmentation:
  prefill spikes:
next benchmark:
```

## 本地证据

- 暂无 `raw-sources/` 下专门针对 capacity planning 的显存估算 vs 实测对照样本。
- 章节中显存估算公式、性能估算、运行时参数检查属于对 vLLM / SGLang / TensorRT-LLM 文档 + PagedAttention / DistServe / FlashAttention 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/serving/capacity-<model>-<gpu>.md`，含显存估算 vs 实测、KV cache 容量、并发上限。

## 尚未本地验证的边界

- 显存估算公式中的 `runtime_workspace`、`cuda_graph_pools`、`fragmentation_margin` 依赖 runtime 版本，本页未引用本机数字。
- “并发上限粗略”公式仅用平均长度，真实场景需要 p95/p99 长度分布。
- 性能估算“prefill 看 prompt tokens/sec、decode 看 generation tokens/sec”是方向性结论，没有本机数字。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/tensorrt-llm-docs]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/distserve-paper]]
- [[70-sources/key-papers/flashattention-papers]]

## 相关页面

- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/batching-scheduling]]
- [[40-serving-platform/observability-slo-cost]]
