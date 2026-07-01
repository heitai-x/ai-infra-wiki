---
title: LLM Serving Benchmark
type: experiment
topic: inference
component: llm-serving
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [serving, benchmark, vllm, sglang]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# LLM Serving Benchmark

## Question

在同一模型、同一 GPU、同一 workload 下，serving runtime 参数如何影响 TTFT、TPOT、吞吐、KV cache 和拒绝率？

## Baseline

选择 vLLM 或 SGLang，先跑单 runtime baseline。后续再比较框架，避免变量过多。

## Variables

- max model len。
- max num seqs。
- max batched tokens。
- tensor parallel size。
- GPU memory utilization。
- prefix cache on/off。
- quantization。
- prompt/output length distribution。
- request concurrency / QPS。

## Metrics

- TTFT p50/p95/p99。
- TPOT p50/p95/p99。
- request throughput。
- prompt tokens/sec、generation tokens/sec。
- GPU memory and KV cache utilization。
- queue time、rejection、timeout。

## Procedure

1. 记录模型、commit、GPU、命令。
2. 预热。
3. 固定 workload 跑 3 次。
4. 每次只改变一个变量。
5. 保存 server log、benchmark raw JSON/CSV、GPU metrics。
6. 用 [[80-playbooks/benchmark-design]] 写结论。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/tensorrt-llm-docs]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/distserve-paper]]

## Related

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[80-playbooks/serving-capacity-planning]]
