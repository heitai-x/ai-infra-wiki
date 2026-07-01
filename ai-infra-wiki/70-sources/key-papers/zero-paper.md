---
title: ZeRO Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/1910.02054
topic: training
component: zero
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, zero, fsdp, sharding]
---

# ZeRO Paper

## Why It Matters

ZeRO 是参数、梯度和 optimizer state 分片主线的奠基论文，是理解 ZeRO/FSDP 显存账本与通信代价的核心文献。

## Key Claims

- 论文提出按 stage 逐步切分 optimizer state、gradient 和 parameter 的思路。
- 其核心价值是把数据并行的显存复制问题拆成可工程化的状态分片问题。
- 后续很多 FSDP/ZeRO-3 的讨论，都可以回溯到这篇论文的状态划分框架。

## Limits Or Caveats

- 论文中的实现和 today 的 FSDP/DeepSpeed 细节不完全一致。
- 论文结论不等于当前硬件和软件栈下的性能最优策略。
- 实际收益还依赖 bucket、overlap、checkpoint 和网络拓扑。

## Links To Concepts

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/distributed-training-map]]
- [[80-playbooks/fsdp-zero-oom-triage]]

## Follow Up

- 后续补论文中 memory saving 公式与现代 FSDP 的差异说明。
