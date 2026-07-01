---
title: PyTorch Distributed
type: source
source_type: official_doc
source_url: https://docs.pytorch.org/docs/stable/distributed.html
topic: training
component: pytorch-distributed
level: intermediate
status: active
last_updated: 2026-06-13
last_checked: 2026-06-13
owner: local
reliability: high
tags: [pytorch, distributed, fsdp, dtensor]
---

# PyTorch Distributed

## 为什么重要

PyTorch Distributed 是理解现代训练系统的基础入口。DDP、FSDP、DTensor、Tensor Parallel、checkpoint 和 process group 等抽象，是很多上层框架和内部训练平台的共同语言。

## 重点模块

- `torch.distributed`：process group、collectives、barrier、rank/world size。
- DDP：梯度 bucket 和 all-reduce。
- FSDP：参数 shard、all-gather、reduce-scatter、reshard。
- DTensor：分布式张量抽象，用 placement 描述张量如何分布。
- Tensor Parallel API：基于 DTensor 的张量并行接口。
- Distributed checkpoint：sharded state 保存和恢复。

## 学习路径

1. 用 DDP 跑最小训练脚本，理解 rank、backend、init method。
2. 打开 profiler，看 backward 中梯度 all-reduce。
3. 切换 FSDP，记录显存峰值和通信变化。
4. 阅读 DTensor placement：Shard、Replicate、Partial。
5. 用 Tensor Parallel 理解 column/row parallel linear。

## 官方来源

- PyTorch Distributed overview: https://docs.pytorch.org/docs/stable/distributed.html
- PyTorch FSDP: https://docs.pytorch.org/docs/stable/fsdp.html
- PyTorch DTensor: https://docs.pytorch.org/docs/stable/distributed.tensor.html
- PyTorch Tensor Parallelism: https://docs.pytorch.org/docs/stable/distributed.tensor.parallel.html

## 相关页面

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[80-playbooks/fsdp-zero-oom-triage]]
