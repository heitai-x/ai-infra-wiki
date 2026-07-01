---
title: GPipe Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/1811.06965
topic: training
component: pipeline-parallel
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, gpipe, pipeline-parallel]
---

# GPipe Paper

## Why It Matters

GPipe 是 pipeline parallel、micro-batch 与 bubble 分析的经典论文，适合作为 PP 基础机制的论文入口。

## Key Claims

- 论文给出 stage 划分与 micro-batch 流动的基本框架。
- micro-batch 数量和 stage 数量决定 bubble 与 activation 代价的权衡。
- PP 解决的是层级切分与单卡放不下的模型规模问题。

## Limits Or Caveats

- 论文中的调度和现代 1F1B、interleaving 等实现不完全相同。
- 真正的系统表现还与 activation rematerialization、拓扑和负载均衡有关。

## Links To Concepts

- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[20-training-systems/training-performance-playbook]]

## Follow Up

- 后续补 PP bubble 估算公式与现代训练实现对比。
