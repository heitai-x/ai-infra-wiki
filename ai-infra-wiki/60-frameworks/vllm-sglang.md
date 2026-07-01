---
title: vLLM SGLang
type: source
source_type: official_doc
source_url: https://docs.vllm.ai/en/stable/
topic: inference
component: vllm-sglang
level: intermediate
status: active
last_updated: 2026-06-13
last_checked: 2026-06-13
owner: local
reliability: high
tags: [vllm, sglang, serving, paged-attention]
---

# vLLM SGLang

## 为什么重要

vLLM 和 SGLang 是学习现代 LLM serving 的核心开源入口。它们暴露了 KV cache、paged memory、continuous batching、prefix cache、scheduler、parallelism 和 serving API 的实际工程问题。

## vLLM 学习重点

- PagedAttention / paged KV cache。
- Scheduler、continuous batching、preemption。
- Tensor parallel serving。
- Prefix caching。
- OpenAI-compatible server。
- Benchmark 参数与 metric。

## SGLang 学习重点

- Runtime scheduler。
- Radix/prefix cache。
- Speculative decoding、grammar/constrained decoding。
- Multi-node serving、PD/disaggregation 相关能力。
- 与 vLLM/TensorRT-LLM 的 benchmark 对比。

## 共同问题

- 如何估算 KV cache 容量。
- 如何设置 max model len、max num seqs、batch token 限制。
- 如何测 TTFT、TPOT、throughput。
- 如何处理长 prompt 和高并发混合 workload。
- 如何避免“只测吞吐、不看 SLO”的 benchmark 偏差。

## 官方来源

- vLLM stable docs: https://docs.vllm.ai/en/stable/
- vLLM latest docs for fast-moving changes: https://docs.vllm.ai/en/latest/
- vLLM GitHub: https://github.com/vllm-project/vllm
- SGLang docs: https://docs.sglang.ai/
- SGLang GitHub: https://github.com/sgl-project/sglang

## 相关页面

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[80-playbooks/serving-capacity-planning]]
- [[90-experiments/llm-serving-benchmark]]
