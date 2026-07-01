---
title: FlashAttention Papers
type: source
source_type: paper
source_url: https://arxiv.org/abs/2205.14135
topic: hardware
component: attention-kernel
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, flashattention, kernel, attention]
---

# FlashAttention Papers

## Why It Matters

FlashAttention/FlashAttention-2 是 attention IO-aware 优化的代表论文，适合作为 memory-bound attention 与 kernel 设计的权威来源。

## Key Claims

- 论文强调 attention 性能常受 IO 与 memory movement 支配。
- kernel 设计可以通过 tile、重算和更好的 memory access 降低 HBM 读写压力。
- FlashAttention-2 继续优化并行性和硬件利用率。

## Limits Or Caveats

- 论文结论依赖 kernel、硬件和实现细节，不能直接等同于任意框架实测收益。
- 某些实际 serving/runtime 的 attention 路径可能不是论文中的实现。

## Links To Concepts

- [[10-foundations/memory-and-roofline]]
- [[10-foundations/cuda-kernel-basics]]
- [[30-inference-systems/llm-serving-map]]

## Follow Up

- 后续补 FlashAttention 与 paged attention 的关系说明。
