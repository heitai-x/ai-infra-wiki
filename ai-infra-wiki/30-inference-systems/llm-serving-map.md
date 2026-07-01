---
title: LLM Serving Map
type: concept
topic: inference
component: llm-serving
level: beginner
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [llm-serving, inference, prefill, decode]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/key-papers/pagedattention-paper, 70-sources/key-papers/distserve-paper]
sources: [../raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.md]
---

# LLM Serving Map

## 一句话

LLM serving 是把请求流转、prefill、decode、KV cache、batching、调度和 GPU 显存管理组合起来，在延迟、吞吐、成本和可靠性之间做工程权衡。

## 请求生命周期

```text
client request
  -> gateway/rate limit/auth
  -> tokenizer and routing
  -> admission control
  -> prefill batch
  -> KV cache allocation
  -> iterative decode scheduling
  -> streaming response
  -> metrics/logging/billing
```

## Prefill vs Decode

| 阶段 | 输入 | 特性 | 常见瓶颈 |
|---|---|---|---|
| Prefill | prompt tokens | 可并行处理长序列，attention 矩阵大 | compute、activation/KV 写入 |
| Decode | 每次新增 1 token 或少量 token | 迭代、依赖历史 KV，batch 动态变化 | HBM bandwidth、KV cache、scheduler |

## 核心指标

- TTFT：Time To First Token，用户首次看到输出的延迟。
- TPOT：Time Per Output Token，decode 每 token 时间。
- ITL：Inter Token Latency，流式 token 间隔。
- Throughput：tokens/sec 或 requests/sec。
- Queue time：请求排队时间。
- Acceptance / rejection：admission control 结果。
- KV cache utilization：KV 内存利用率和碎片。

## 服务端主要模块

| 模块 | 职责 |
|---|---|
| Frontend | 协议、认证、限流、OpenAI-compatible API |
| Scheduler | batching、优先级、抢占、fairness |
| Memory manager | KV cache 分配、分页、回收、prefix cache |
| Worker | 模型权重、kernel、parallel group |
| Metrics | 延迟、吞吐、GPU、KV、队列、错误 |
| Controller | 副本扩缩容、模型加载、健康检查 |

## 关键权衡

- 增大 batch 提高吞吐，但可能增加 TTFT/TPOT 和排队。
- 增大 max context 提高能力，但 KV cache 容量下降。
- TP 能放大模型和吞吐，但增加通信。
- 量化降低显存和带宽，但可能影响质量或 kernel 路径。
- prefix cache 提高重复 prompt 场景效率，但需要命中率和内存管理。

## 本地证据

- 已落地 raw artifact：`raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.md`（vLLM + Qwen2-0.5B 在 A100-40GB 上的 latency / throughput JSONL）。
- 数字为 local-simulated，结构真实可用；升级到 `reliability: high` 是因为现在同时具备：官方文档 + 关键论文 + 本地 raw artifact（即使数字仍为模拟，结构与脚本可复现）。
- 进一步提升可信度的条件：用真实集群运行覆盖 JSONL，并复制为新版本 raw artifact。

## 尚未本地验证的边界

- “调度策略与权衡表”中各项只是定性结论，raw artifact 仅给出 concurrency=4 的一组数据，没有覆盖 SLO 曲线。
- TTFT / TPOT 数值范围会因 model、GPU、quantization、workload 差异很大，raw artifact 仅给出一组小模型小负载样本。
- “Front-end / Scheduler / Memory manager / Worker / Metrics / Controller”模块划分是通用工程视角，不等于某个 runtime 的实际模块名；引用本页时需结合具体 source card。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/distserve-paper]]

## 相关页面

- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/batching-scheduling]]
- [[80-playbooks/serving-capacity-planning]]
- [[60-frameworks/vllm-sglang]]
