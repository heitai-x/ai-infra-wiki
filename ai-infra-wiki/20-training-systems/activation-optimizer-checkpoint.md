---
title: Activation Optimizer Checkpoint
type: concept
topic: training
component: memory
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [activation-checkpointing, optimizer, checkpoint, memory]
source_refs: [70-sources/official-docs/pytorch-distributed-docs, 70-sources/official-docs/deepspeed-docs, 70-sources/key-papers/zero-paper, 70-sources/key-papers/data-pipeline-papers]
---

# Activation Optimizer Checkpoint

## 一句话

训练显存主要被参数、梯度、optimizer state、activation 吃掉。Activation checkpointing 用重算换 activation 显存；ZeRO/FSDP/distributed optimizer 切 optimizer state；distributed checkpoint 让大规模训练可恢复。

## Activation checkpointing

普通 backward 需要 forward 中保存的 activation。checkpointing 只保存部分边界 activation，backward 时重新计算中间 activation。

收益：

- activation 显存显著下降。
- 可以提高 batch size 或 seq len。

代价：

- backward 增加重算 FLOPs。
- checkpoint 粒度过细会增加开销。
- 与 dropout/RNG、custom kernel、pipeline 调度需要仔细处理。

## Optimizer state

训练显存账本中，参数、梯度和 optimizer state 是不同类别：

```text
parameters + gradients + optimizer_states
```

Adam 类 optimizer state 通常包含一阶矩和二阶矩：

```text
exp_avg + exp_avg_sq
```

在混合精度训练中还可能有 FP32 master params。大模型下 optimizer state 常常与参数同阶甚至更大，因此 ZeRO-1/FSDP distributed optimizer 的收益很高。

## Distributed checkpoint

大规模训练 checkpoint 不只是保存模型权重，还包括：

- model shard。
- optimizer shard。
- scheduler state。
- RNG state。
- dataloader position。
- parallelism metadata。
- framework/version/config。

关键问题：

- sharded state 如何映射到恢复时的新 parallelism。
- checkpoint 写入是否造成训练停顿。
- partial failure 时如何保证一致性。
- 保存频率如何平衡恢复点目标和 IO 成本。

## 观测点

- activation memory peak。
- recompute overhead。
- optimizer step time。
- checkpoint write/read throughput。
- resume 后 loss 是否连续。

## 本地证据

- 暂无 `raw-sources/` 下的 activation checkpoint 显存 / step time 折衷、checkpoint 写入吞吐、optimizer 状态大小复现样本。
- 章节中 activation checkpoint 收益 / 代价、optimizer state 账本、distributed checkpoint 关键问题属于对 PyTorch Distributed / DeepSpeed 文档 + ZeRO 论文 + 数据 pipeline 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/ckpt-actopt-<commit>.md`，含开 / 关 activation checkpoint 前后显存峰值与 step time，以及一次 sharded checkpoint 的写入吞吐。

## 尚未本地验证的边界

- “activation 显存显著下降” 的具体倍数依赖 layer / seq len / micro-batch。
- distributed checkpoint 写入是否造成训练停顿，依赖 IO 子系统与实现，本页未引用本机数据。
- resume 后 loss 是否连续受 RNG state、dataset shard、parallelism metadata 等多因素影响，本页未给出复现脚本。

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/deepspeed-docs]]
- [[70-sources/key-papers/zero-paper]]
- [[70-sources/key-papers/data-pipeline-papers]]

## 相关页面

- [[20-training-systems/ddp-fsdp-zero]]
- [[80-playbooks/fsdp-zero-oom-triage]]
- [[20-training-systems/data-pipeline-fault-tolerance]]
