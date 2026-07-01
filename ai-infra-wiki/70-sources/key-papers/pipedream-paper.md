---
title: PipeDream Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/1806.03377
topic: training
component: pipeline-parallel
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, pipedream, pipeline-parallel]
---

# PipeDream Paper

## Why It Matters

PipeDream 论文代表了 pipeline schedule、吞吐与 staleness 之间的系统权衡，是理解 GPipe 之外另一条 PP 设计路线的重要资料。

## Key Claims

- 论文强调通过流水调度提高设备利用率和训练吞吐。
- schedule 设计可能引入权重版本或 staleness 问题，需要与 correctness 一起看。
- PP 不只是分层，还包括调度策略本身。

## Limits Or Caveats

- 论文中的 staleness 讨论不应直接套用到所有现代 PP 实现。
- 实际训练框架常采用不同 schedule，需结合实现细节阅读。

## Links To Concepts

- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[20-training-systems/training-performance-playbook]]

## Follow Up

- 后续补 GPipe 与 PipeDream 的 schedule 对比表。
