---
title: Switch Transformer Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/2101.03961
topic: training
component: moe
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, switch-transformer, moe]
---

# Switch Transformer Paper

## Why It Matters

Switch Transformer 是 top-1 routing 与大规模稀疏 Transformer 的经典论文，适合作为 capacity、负载均衡与训练稳定性讨论的来源。

## Key Claims

- 论文强调稀疏 expert 激活下的扩展路径与路由简化。
- capacity factor 与 load balancing 直接影响 token drop、利用率和稳定性。
- MoE 的训练收益和工程复杂度是同时上升的。

## Limits Or Caveats

- top-1 routing 只是 MoE 设计空间中的一种选择。
- 现代 dropless MoE 与生产 serving 的权衡超出论文本身范围。

## Links To Concepts

- [[20-training-systems/expert-parallel-moe]]
- [[30-inference-systems/disaggregated-and-moe-serving]]

## Follow Up

- 后续补 token drop 与 dropless MoE 的实践差异。
