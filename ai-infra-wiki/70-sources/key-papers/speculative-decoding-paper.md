---
title: Speculative Decoding Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/2211.17192
topic: inference
component: speculative-decoding
level: all
status: active
last_updated: 2026-06-13
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, speculative-decoding, draft-model, verification]
---

# Speculative Decoding Paper

## Why It Matters

投机解码原文是理解 draft/target 模型配对、acceptance rate、token verify 路径的源头文献，也是 `30-inference-systems/parallelism-quantization-speculation` 的关键支撑。

## Key Claims

- 论文定义 speculative decoding 的 acceptance / rejection 规则。
- 论文证明在 target 分布不变前提下 speculative decoding 的输出一致性。
- 论文给出 acceptance 与 draft/target 分布相似度的关系。
- 后续工作扩展到 self-speculative、medusa、tree attention、EAGLE 等。

## Limits Or Caveats

- 收益高度依赖 workload，长 prompt / 长 output 收益更明显。
- draft model 也消耗显存和 kernel 资源。
- 实际部署需要 scheduler 支持变长接受。

## Links To Concepts

- [[30-inference-systems/parallelism-quantization-speculation]]
- [[30-inference-systems/batching-scheduling]]
- [[70-sources/key-papers/speculative-decoding-papers]]

## Follow Up

- 后续按 Medusa / EAGLE 等分别建独立 source card。
