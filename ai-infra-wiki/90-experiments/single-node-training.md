---
title: Single Node Training
type: experiment
topic: training
component: ddp-fsdp
level: beginner
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [training, ddp, fsdp, experiment]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# Single Node Training

## Question

DDP 和 FSDP 在单机多卡上的显存、step time 和通信有什么差异？

## Setup

建议选择一个小模型，保证 DDP 和 FSDP 都能跑通。硬件至少 2 GPU，更好是 8 GPU。

## Variables

- Strategy：DDP、FSDP full shard。
- Batch：micro batch 与 global batch。
- Seq len。
- Activation checkpoint：on/off。
- Precision：bf16/fp16/fp32。

## Metrics

- step time p50/p95。
- max allocated/reserved GPU memory。
- NCCL all-reduce/all-gather/reduce-scatter 时间。
- samples/sec 或 tokens/sec。
- loss 是否一致。

## Expected Learnings

- DDP 简单但状态复制多。
- FSDP 降低常驻显存，但引入 all-gather/reduce-scatter。
- Activation checkpoint 能降 activation 显存，但 step time 增加。
- profiler 比最终吞吐更能解释差异来源。

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/pytorch-profiler-docs]]
- [[70-sources/key-papers/zero-paper]]

## Related

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/training-performance-playbook]]
- [[80-playbooks/fsdp-zero-oom-triage]]
