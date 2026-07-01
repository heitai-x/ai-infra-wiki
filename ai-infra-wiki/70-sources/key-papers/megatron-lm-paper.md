---
title: Megatron LM Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/1909.08053
topic: training
component: tensor-parallel
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, megatron, tensor-parallel]
---

# Megatron LM Paper

## Why It Matters

Megatron-LM 论文是 Tensor Model Parallelism 的经典起点，适合作为 TP 的论文级定义来源。

## Key Claims

- 论文展示了 column/row parallel linear 与层内张量切分的基本思想。
- TP 的核心收益是把单层计算和参数分摊到多卡上。
- TP 代价来自频繁 collective 与对高速互联的依赖。

## Limits Or Caveats

- 论文主要是早期 Megatron-LM 视角，后续实现与术语已演化。
- 真正的大规模训练往往是 TP/PP/DP/FSDP/CP 组合，而不是只用 TP。

## Links To Concepts

- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[60-frameworks/deepspeed-megatron]]

## Follow Up

- 后续补 TP 通信路径与现代 Megatron-Core 对应关系。
