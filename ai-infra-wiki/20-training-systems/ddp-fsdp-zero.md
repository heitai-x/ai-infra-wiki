---
title: DDP FSDP ZeRO
type: concept
topic: training
component: data-parallel
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [ddp, fsdp, zero, sharding]
source_refs: [70-sources/official-docs/pytorch-distributed-docs, 70-sources/official-docs/deepspeed-docs, 70-sources/key-papers/zero-paper]
sources: [../raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.md]
---

# DDP FSDP ZeRO

## 一句话

DDP 复制模型并同步梯度；ZeRO 按 stage 切分 optimizer state、梯度和参数，FSDP/ZeRO-3 才切分参数。切分越彻底，每卡常驻显存越低，但 all-gather/reduce-scatter 等通信和调度复杂度越高。

## DDP

每个 rank 有完整模型副本：

```text
forward/backward local
  -> gradient buckets all-reduce
  -> every rank has same averaged gradients
  -> optimizer update locally
```

优点：简单、稳定、通信模式清晰。缺点：参数、梯度、optimizer state 都完整复制，显存随模型规模迅速受限。

## ZeRO 分级

| 策略 | 切分 optimizer | 切分 gradients | 切分 parameters | 主要收益 |
|---|---|---|---|---|
| ZeRO-1 | 是 | 否 | 否 | optimizer state 显存下降 |
| ZeRO-2 | 是 | 是 | 否 | 再降低 gradient 显存 |
| ZeRO-3 | 是 | 是 | 是 | 参数也切分，最大显存收益 |

## FSDP

FSDP 通常把 module 参数 flatten/shard。计算某个 module 前 all-gather 需要的参数，forward/backward 后释放或 reshard；梯度通过 reduce-scatter 回到 shard。

典型时序：

```text
all-gather params for layer/block
  -> compute forward/backward
  -> reduce-scatter gradients
  -> optimizer update local shard
```

## 显存账本

DDP 每卡近似：

```text
params + gradients + optimizer_states + activations
```

ZeRO-3/FSDP 每卡近似：

```text
(params + gradients + optimizer_states) / data_parallel_size
+ all_gathered_working_set
+ activations
+ buffers
```

实际显存还受 prefetch、bucket、fragmentation、activation checkpoint、mixed precision 影响。

## 性能权衡

- shard 越彻底，常驻显存越低，但通信越频繁。
- module wrapping 粒度影响 all-gather 工作集和 overlap。
- prefetch 能隐藏通信，但也会提高峰值显存。
- activation checkpoint 与 FSDP 常组合使用，但会增加重算。

## 观测点

- GPU memory peak。
- all-gather / reduce-scatter 时间。
- backward compute 与 communication overlap。
- step time p50/p99。
- OOM 发生在 forward、backward、optimizer 还是 checkpoint。

## 本地证据

- 已落地 raw artifact：`raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.md`（DDP vs FSDP vs FSDP+activation-checkpoint 显存与 step time 对照）。
- 数字为 local-simulated，结构真实可用；升级到 `reliability: high` 是因为现在同时具备：官方文档 + 关键论文 + 本地 raw artifact（即使数字仍为模拟，结构与脚本可复现）。
- 进一步提升可信度的条件：用真实集群运行覆盖 JSONL，并复制为新版本 raw artifact（不修改本页直接引用的旧版本）。

## 尚未本地验证的边界

- “shard 越彻底，常驻显存越低，但通信越频繁”在 raw artifact 中已得到方向性验证，但真实倍数依赖 NCCL overlap、PCIe/NVLink 拓扑、CUDA Graph。
- FSDP wrap 粒度对 all-gather 工作集和 overlap 的影响依赖具体模型与硬件，本页未引用本机数据。
- activation checkpoint + FSDP 的“重算 / 显存”折衷数字会随 layer、seq len 变化，raw artifact 仅给出 TinyTransformer 的一种配置。

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/deepspeed-docs]]
- [[70-sources/key-papers/zero-paper]]

## 相关页面

- [[60-frameworks/pytorch-distributed]]
- [[60-frameworks/deepspeed-megatron]]
- [[80-playbooks/fsdp-zero-oom-triage]]
