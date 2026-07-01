---
title: GShard Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/2006.16668
topic: training
component: moe
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, gshard, moe, expert-parallel]
---

# GShard Paper

## Why It Matters

GShard 是大规模稀疏 MoE 与自动分片的重要代表论文，适合作为 expert routing 和规模扩展的早期主线资料。

## Key Claims

- 论文展示了通过稀疏 expert 激活提升参数规模的路径。
- expert routing、capacity 与负载均衡是 MoE 系统设计的核心约束。
- 大规模 MoE 需要通信与分片策略共同配合。

## Limits Or Caveats

- 论文语境偏 Google 体系，不同开源框架的实现细节会不同。
- 训练和推理中的 expert 热点与延迟问题仍需结合系统实现看。

## Links To Concepts

- [[20-training-systems/expert-parallel-moe]]
- [[30-inference-systems/disaggregated-and-moe-serving]]

## Follow Up

- 后续补与 Switch Transformer 的差异对比。
