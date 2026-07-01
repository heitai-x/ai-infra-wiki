---
title: Distributed Training Map
type: concept
topic: training
component: distributed-training
level: beginner
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [training, distributed, map]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# Distributed Training Map

## 一句话

分布式训练是把模型状态、计算、activation、梯度、optimizer state、数据和 checkpoint 分布到多 GPU/多节点上，同时尽量让 compute、communication、IO overlap。

## 一个训练 step

```text
load batch
  -> forward
  -> loss
  -> backward
  -> gradient communication
  -> optimizer update
  -> scheduler/logging/checkpoint
```

不同并行策略改变的是“哪些状态被复制或切分”和“在哪些时间点通信”。

## 状态分类

| 状态 | 规模 | 是否必须保存 | 常见切分方式 |
|---|---|---|---|
| Parameters | O(model params) | 是 | FSDP/ZeRO、TP、PP、EP |
| Gradients | O(model params) | step 内需要 | DDP all-reduce、ZeRO reduce-scatter |
| Optimizer states | Adam 常见 2x params | 是 | ZeRO/FSDP distributed optimizer |
| Activations | O(batch * seq * hidden * layers) | backward 需要 | activation checkpoint、sequence/context parallel |
| RNG / dataloader state | 小但关键 | 恢复需要 | checkpoint metadata |
| Checkpoint | 全局训练状态 | 是 | sharded checkpoint |

## 并行维度

| 并行 | 切什么 | 通信 | 适合场景 |
|---|---|---|---|
| Data Parallel | batch | gradient sync | 最基础扩展 |
| FSDP/ZeRO | 按策略切分参数、梯度、optimizer state；ZeRO-1/2 不切参数，ZeRO-3/FSDP 才切参数 | all-gather / reduce-scatter | 显存不足 |
| Tensor Parallel | 层内张量维度 | all-reduce / all-gather / reduce-scatter | 单层太大 |
| Pipeline Parallel | 层 | activation send/recv | 模型层数多、单卡放不下 |
| Sequence/Context Parallel | sequence/context | attention、布局转换、RNG 一致性相关通信 | 长上下文 |
| Expert Parallel | expert | all-to-all | MoE |

## 决策顺序

1. 单卡能否放下模型和 batch？不能，先看 FSDP/ZeRO、activation checkpoint。
2. 单层是否太大？看 TP。
3. 层数是否太多？看 PP。
4. context 是否太长？看 CP/SP。
5. MoE expert 是否太多？看 EP。
6. step time 是否被通信支配？看 overlap、bucket、拓扑、并行组。

## 本地证据

- 暂无 `raw-sources/` 下的多维并行（DP × TP × PP × CP × EP）profile trace 与 step time 样本。
- 章节中“一个训练 step”拆解、状态分类、并行维度表、决策顺序属于对 PyTorch Distributed / Megatron-Core / DeepSpeed 文档 + ZeRO / Megatron-LM / GPipe 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/parallel-ladder-<commit>.md`，含每种并行的 step time、显存峰值、通信占比、bubble 占比。

## 尚未本地验证的边界

- 各并行的“适用场景”是经验判断，不等于具体集群下的最优解。
- 决策顺序（单卡 → FSDP → TP → PP → CP → EP）是经验路径，复杂场景下需要并行优化器、profile-guided 调整。
- 表格中的“通信 / 切什么”描述属于定性结论，不构成运行时具体行为。

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/megatron-core-docs]]
- [[70-sources/official-docs/deepspeed-docs]]
- [[70-sources/key-papers/zero-paper]]
- [[70-sources/key-papers/megatron-lm-paper]]
- [[70-sources/key-papers/gpipe-paper]]

## 相关页面

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[20-training-systems/expert-parallel-moe]]
- [[20-training-systems/training-performance-playbook]]
