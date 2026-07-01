---
title: Speculative Decoding Paper Deep Dive
type: source
source_type: paper
source_url: https://arxiv.org/abs/2211.17192
topic: inference
component: optimization
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [paper, speculative-decoding, draft-model, acceptance]
---

# Speculative Decoding Paper Deep Dive

## Why It Matters

`30-inference-systems/parallelism-quantization-speculation` 中关于投机解码的结论，需要追溯到 speculative decoding 的原始论文和后续工作，才能正确判断 acceptance rate、target 验证 cost、draft overhead。

## Key Claims

- 论文给出 speculative decoding 的形式化：draft model 生成 candidate tokens，target model 一次前向验证多个 token。
- 论文分析 acceptance rate 和目标分布的关系。
- 后续工作讨论 self-speculative decoding、medusa-style head、EAGLE / Lookahead 等机制。
- 论文说明 speculative decoding 的正确性前提：target model 实际概率分布不变。

## Limits Or Caveats

- 论文假设 draft model 和 target model 共享 vocab。
- acceptance rate 与 workload 强相关，不能照搬论文数字。
- 收益在 batch size 小、长 prompt / 长 output 时更明显。
- 引入 draft model 也会增加显存、调度复杂度和 kernel 路径。

## Links To Concepts

- [[30-inference-systems/parallelism-quantization-speculation]]
- [[30-inference-systems/batching-scheduling]]
- [[70-sources/key-papers/speculative-decoding-paper]]

## Follow Up

- 后续按 Medusa / EAGLE / Lookahead 分别建独立 source card。
- 后续补 acceptance-rate 经验曲线来源。
