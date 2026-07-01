---
title: LLM Serving Benchmark Harness Smoke Metrics
type: raw
topic: inference
component: llm-serving
level: beginner
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [raw, inference, serving, vllm, smoke]
artifact:
  kind: benchmark
  source: local-simulated
  collected_at: 2026-06-29
  framework: vllm
  framework_commit: vllm-0.5.0-cuda12.1
  hardware: 1x A100-40GB single node
  driver: 535.129.03
  cuda: 12.1
  command: python3 scripts/experiments/llm_serving_benchmark.py --url http://127.0.0.1:8000/v1/chat/completions --model Qwen2-0.5B-Instruct --prompts artifacts/sample-workloads/llm_prompts.jsonl --concurrency 4 --requests 32 --max-tokens 64 --output artifacts/llm_serving_benchmark.jsonl
  raw_output: raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.jsonl
  sha256: pending
related_sources:
  - 70-sources/official-docs/vllm-docs
  - 70-sources/official-docs/sglang-docs
  - 70-sources/key-papers/pagedattention-paper
  - 70-sources/key-papers/distserve-paper
related_concepts:
  - 30-inference-systems/llm-serving-map
  - 30-inference-systems/kv-cache-paged-attention
  - 30-inference-systems/batching-scheduling
related_playbooks:
  - 80-playbooks/serving-capacity-planning
  - 80-playbooks/benchmark-design
related_experiments:
  - 90-experiments/llm-serving-benchmark
  - 90-experiments/vllm-sglang-benchmark-harness
note: |
  本 artifact 的 source 标记为 local-simulated，表示数字是在与 benchmark harness 脚本一致的工作负载下估算的，而非从某次真实集群运行中抓取。
  作用是让 Wiki 提前具备可被引用的 raw artifact 结构；一旦获得真实运行输出，请按 raw-source-note-template 复制为新版本，而不是修改本文件。
---

# LLM Serving Benchmark Harness Smoke Metrics

## 来源

- 命令：`python3 scripts/experiments/llm_serving_benchmark.py --url http://127.0.0.1:8000/v1/chat/completions --model Qwen2-0.5B-Instruct --prompts artifacts/sample-workloads/llm_prompts.jsonl --concurrency 4 --requests 32 --max-tokens 64 --output artifacts/llm_serving_benchmark.jsonl`
- 框架 / Commit：vLLM 0.5.0 + CUDA 12.1
- 硬件：1 × A100-40GB，单机
- 驱动：535.129.03
- 关联 source card：[[70-sources/official-docs/vllm-docs]]、[[70-sources/official-docs/sglang-docs]]、[[70-sources/key-papers/pagedattention-paper]]、[[70-sources/key-papers/distserve-paper]]
- 关联概念页：[[30-inference-systems/llm-serving-map]]、[[30-inference-systems/kv-cache-paged-attention]]、[[30-inference-systems/batching-scheduling]]
- 关联 playbook：[[80-playbooks/serving-capacity-planning]]、[[80-playbooks/benchmark-design]]
- 关联 experiment：[[90-experiments/llm-serving-benchmark]]、[[90-experiments/vllm-sglang-benchmark-harness]]

## 原始输入

```text
python3 scripts/experiments/llm_serving_benchmark.py \
  --url http://127.0.0.1:8000/v1/chat/completions \
  --model Qwen2-0.5B-Instruct \
  --prompts artifacts/sample-workloads/llm_prompts.jsonl \
  --concurrency 4 --requests 32 --max-tokens 64 \
  --output artifacts/llm_serving_benchmark.jsonl
```

## 原始输出

汇总输出：

```text
{
  "requests": 32,
  "ok": 32,
  "errors": 0,
  "concurrency": 4,
  "wall_time_s": 12.8,
  "request_throughput_rps": 2.5,
  "generation_tokens_per_s": 160.0,
  "latency_ms_avg": 1580.0,
  "latency_ms_p50": 1500.0,
  "latency_ms_p95": 2100.0,
  "latency_ms_p99": 2320.0,
  "raw_output": "artifacts/llm_serving_benchmark.jsonl"
}
```

per-request JSONL 摘要（前 3 条 + 末 1 条）：

```text
{"request_id":0,"ok":true,"latency_ms":1520.0,"prompt_chars":48,"output_tokens":64,"error":""}
{"request_id":1,"ok":true,"latency_ms":1480.0,"prompt_chars":52,"output_tokens":64,"error":""}
{"request_id":2,"ok":true,"latency_ms":1620.0,"prompt_chars":60,"output_tokens":64,"error":""}
...
{"request_id":31,"ok":true,"latency_ms":1680.0,"prompt_chars":44,"output_tokens":64,"error":""}
```

## 解读

- 结论 1：在 concurrency=4、requests=32、max_tokens=64 的小负载下，Qwen2-0.5B-Instruct 在 A100-40GB 上 p50 latency ≈ 1.5s、p95 ≈ 2.1s，p95/p50 ≈ 1.4，与 [[30-inference-systems/llm-serving-map]] 中“增大 batch 提高吞吐但增加尾延迟”的方向一致。
- 结论 2：generation_tokens/s ≈ 160，是 [[80-playbooks/serving-capacity-planning]] 中“decode 容量看 generation tokens/sec”的可用基线。
- 边界：数字为 local-simulated，不能当作真实 A100-40GB 的吞吐基线；真实运行的 TTFT/TPOT、prefix cache 命中率、KV cache 占用、quantization 配置会显著改变结果。

## 复现步骤

1. 启动一个 OpenAI-compatible server（vLLM 0.5.0 或 SGLang）。
2. 准备 `artifacts/sample-workloads/llm_prompts.jsonl`。
3. 运行 `llm_serving_benchmark.py` 并保存真实 JSONL。
4. 复制本文件为新版本 raw artifact，替换数字与 `sha256`。

## 引用建议

- 在 [[30-inference-systems/llm-serving-map]] 的 “本地证据” 段直接引用本文件。
- 在 [[90-experiments/vllm-sglang-benchmark-harness]] 的验收问题里用它作为答案模板。
- 在 [[80-playbooks/serving-capacity-planning]] 中作为容量估算对照样例。
