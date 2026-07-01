---
title: DeepSpeed Megatron
type: source
source_type: official_doc
source_url: https://docs.nvidia.com/megatron-core/developer-guide/latest/
topic: training
component: deepspeed-megatron
level: intermediate
status: active
last_updated: 2026-06-13
last_checked: 2026-06-13
owner: local
reliability: high
tags: [deepspeed, megatron, zero, tensor-parallel, pipeline-parallel]
---

# DeepSpeed Megatron

## 为什么重要

DeepSpeed 和 Megatron-Core/Megatron-LM 是大模型训练系统学习的两条主线。DeepSpeed 强调 ZeRO、offload、训练优化；Megatron 强调张量并行、流水并行、分布式 optimizer、MoE 和大规模训练工程。

## DeepSpeed 学习重点

- ZeRO-1/2/3 的状态切分。
- CPU/NVMe offload 的收益和代价。
- activation checkpointing。
- config JSON 中 batch、optimizer、precision、zero optimization。
- 与 PyTorch DDP/FSDP 的概念对应。

## Megatron 学习重点

- Tensor Parallel：column/row parallel layers。
- Pipeline Parallel：stage、micro-batch、schedule、bubble。
- Sequence/Context Parallel。
- Distributed optimizer。
- MoE / Expert Parallel。
- Checkpoint conversion 和 parallelism metadata。

## 对比

| 维度 | DeepSpeed | Megatron-Core |
|---|---|---|
| 主要入口 | 配置驱动训练优化 | 大模型并行训练组件 |
| 核心概念 | ZeRO、offload、engine | TP、PP、CP、EP、distributed optimizer |
| 学习价值 | 显存优化和易用性 | 大模型并行机制和代码结构 |

## 官方来源

- DeepSpeed ZeRO tutorial: https://www.deepspeed.ai/tutorials/zero/
- DeepSpeed getting started: https://www.deepspeed.ai/getting-started/
- Megatron-Core developer guide: https://docs.nvidia.com/megatron-core/developer-guide/latest/
- Megatron-LM GitHub: https://github.com/NVIDIA/Megatron-LM

## 相关页面

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[20-training-systems/expert-parallel-moe]]
