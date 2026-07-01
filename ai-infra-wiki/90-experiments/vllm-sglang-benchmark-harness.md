---
title: vLLM SGLang Benchmark Harness
type: experiment
topic: inference
component: llm-serving
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [vllm, sglang, benchmark, openai-api]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/key-papers/pagedattention-paper, 70-sources/key-papers/distserve-paper]
---

# vLLM SGLang Benchmark Harness

## 目标

把 [[30-inference-systems/llm-serving-map]] 和 [[80-playbooks/serving-capacity-planning]] 变成可复现 benchmark：同一 OpenAI-compatible API，记录延迟、吞吐、错误率和 raw JSONL。

## 脚本

- 本地脚本：`scripts/experiments/llm_serving_benchmark.py`
- 样例 workload：`artifacts/sample-workloads/llm_prompts.jsonl`
- 输出 artifact：`artifacts/llm_serving_benchmark.jsonl`

## 前置

先启动一个 OpenAI-compatible server，例如 vLLM 或 SGLang。具体命令取决于模型和框架版本，必须记录到实验笔记中。

## 命令

```bash
python3 scripts/experiments/llm_serving_benchmark.py   --url http://127.0.0.1:8000/v1/chat/completions   --model <served-model-name>   --prompts artifacts/sample-workloads/llm_prompts.jsonl   --concurrency 4   --requests 32   --max-tokens 64   --output artifacts/llm_serving_benchmark.jsonl
```

## 输出指标

- `request_throughput_rps`
- `generation_tokens_per_s`
- `latency_ms_avg/p50/p95/p99`
- `ok/errors`
- raw per-request JSONL

当前脚本是轻量 harness，不替代专业 benchmark。它适合 Wiki 学习闭环和小规模回归；大规模压测仍应使用框架官方 benchmark 或专用压测工具，并按 [[80-playbooks/benchmark-design]] 记录公平性条件。

## 验收问题

1. 改变 concurrency 后，latency p95 和 generation tokens/s 如何变化？
2. prompt 长度变长时，TTFT 类指标是否上升？
3. max_tokens 变大时，decode 阶段是否成为主要耗时？
4. server log 中是否能看到 KV cache、queue、batching 相关指标？

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/distserve-paper]]

## 相关页面

- [[90-experiments/llm-serving-benchmark]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/batching-scheduling]]
