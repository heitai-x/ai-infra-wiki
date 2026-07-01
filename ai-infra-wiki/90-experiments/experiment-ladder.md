---
title: Experiment Ladder
type: experiment
topic: ai-infra
component: learning
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [experiments, learning-path]
source_refs: [70-sources/official-docs/pytorch-distributed-docs, 70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/key-papers/zero-paper, 70-sources/key-papers/pagedattention-paper]
---

# Experiment Ladder

## 目标

用一组从小到大的实验把 Wiki 概念变成真实经验。每个实验必须有命令、环境、指标和解释。

## 阶梯

1. 单 GPU kernel/profiler：矩阵乘、elementwise、reduction。
2. 单机 DDP：观察 gradient all-reduce，见 [[90-experiments/torchrun-ddp-fsdp-minimal]]。
3. 单机 FSDP：比较显存和 step time，见 [[90-experiments/torchrun-ddp-fsdp-minimal]]。
4. Activation checkpoint：比较显存下降和重算成本。
5. 多机 NCCL：测 all-reduce 带宽和 timeout 排查。
6. vLLM/SGLang 单模型 serving：测延迟、吞吐、KV cache，见 [[90-experiments/vllm-sglang-benchmark-harness]]。
7. 长上下文 serving：观察 KV cache 容量和 admission。
8. 量化 serving：比较显存、吞吐、质量。
9. 多租户压测：队列、公平性、拒绝率。
10. 端到端 incident drill：OOM、NCCL hang、latency regression。

## 记录要求

每个实验必须复制 [[03-templates/experiment-note-template]]，并保存：

- 原始命令。
- 原始输出。
- 图或表。
- 失败尝试。
- 和 Wiki 概念页的链接。

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/key-papers/zero-paper]]
- [[70-sources/key-papers/pagedattention-paper]]

## 相关页面

- [[90-experiments/single-node-training]]
- [[90-experiments/torchrun-ddp-fsdp-minimal]]
- [[90-experiments/llm-serving-benchmark]]
- [[90-experiments/vllm-sglang-benchmark-harness]]
- [[80-playbooks/benchmark-design]]
