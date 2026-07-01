---
title: Tensor Pipeline Context Parallel
type: concept
topic: training
component: model-parallelism
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [tensor-parallel, pipeline-parallel, context-parallel, sequence-parallel]
source_refs: [70-sources/official-docs/megatron-core-docs, 70-sources/key-papers/megatron-lm-paper, 70-sources/key-papers/gpipe-paper, 70-sources/key-papers/pipedream-paper]
---

# Tensor Pipeline Context Parallel

## 一句话

模型并行把模型计算沿不同维度切开：Tensor Parallel 切层内矩阵，Pipeline Parallel 切层，Context/Sequence Parallel 切序列维度。

## Tensor Parallel

TP 把一个 layer 内的矩阵乘分到多个 GPU。常见模式：

- Column parallel linear：输出 hidden 维切分，后续可能需要 all-gather 或配对 row parallel。
- Row parallel linear：输入 hidden 维切分，输出需要 all-reduce。
- Attention heads split：不同 heads 分到不同 rank。

优点：解决单层太大、提高单层计算并行。代价：每层都有 collective，对 NVLink/NVSwitch 依赖强。

## Pipeline Parallel

PP 把不同层放到不同 stage。micro-batch 在 pipeline 中流动。

```text
stage0 layers -> stage1 layers -> stage2 layers -> ...
```

优点：解决层数多、模型整体放不下。代价：pipeline bubble、activation send/recv、调度复杂。micro-batch 越多，bubble 占比通常越低，但 activation 和调度成本增加。

## Sequence / Context Parallel

SP/CP 把 sequence 或 context 维度切分，用于长上下文训练和降低 activation/KV 类状态压力。

常见代价：

- attention 需要跨 rank 交换 Q/K/V 或中间结果。
- 某些 SP/CP 实现需要在 attention 或张量布局转换处 all-gather/reduce-scatter；dropout 需要处理跨 rank RNG 一致性。LayerNorm/RMSNorm 通常是 per-token hidden 维操作，不应笼统说它们天然需要 sequence 维同步。
- 长上下文收益明显，但通信和实现复杂度高。

## 组合策略

大模型训练常见组合：

```text
DP/FSDP x TP x PP x CP x EP
```

组合时必须明确每个 process group 的 rank 映射。经验上高频通信的 group 应放在更快互联内，例如 TP 优先放节点内 NVLink/NVSwitch。

## 观测点

- TP collective 是否频繁且未 overlap。
- PP stage 是否负载均衡。
- pipeline bubble 占比。
- context parallel 通信是否随 seq len 放大。
- rank placement 是否符合拓扑。

## 本地证据

- 暂无 `raw-sources/` 下的 TP / PP / CP 真实 profile trace 或通信开销样本。
- 章节中 TP / PP / CP 通信模式、bubble、组合策略属于对 Megatron-Core 文档 + Megatron-LM / GPipe / PipeDream 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/<framework>-parallel-<commit>.md`，含 TP / PP / CP 三种配置下的 step time、bubble 占比、NCCL 时间。

## 尚未本地验证的边界

- SP/CP 中“dropout RNG 一致性 / 布局转换”需要结合具体实现，章节中已经写到 LayerNorm 不应笼统同步，但没引用具体源码或实验。
- TP 优先放在 NVLink 内的“经验原则”依赖集群拓扑，本页未引用具体硬件 / 拓扑数据。
- pipeline bubble 占比随 micro-batch 变化的具体曲线，本页未给出本机数字。

## 来源

- [[70-sources/official-docs/megatron-core-docs]]
- [[70-sources/key-papers/megatron-lm-paper]]
- [[70-sources/key-papers/gpipe-paper]]
- [[70-sources/key-papers/pipedream-paper]]

## 相关页面

- [[20-training-systems/distributed-training-map]]
- [[20-training-systems/training-performance-playbook]]
- [[60-frameworks/deepspeed-megatron]]
