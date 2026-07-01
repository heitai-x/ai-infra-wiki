---
title: DeepSpeed Docs
type: source
source_type: official_doc
source_url: https://www.deepspeed.ai/getting-started/
topic: training
component: deepspeed
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [deepspeed, docs, zero, offload]
---

# DeepSpeed Docs

## Why It Matters

DeepSpeed 官方文档是 ZeRO、offload、activation checkpointing 和配置驱动训练的主入口，适合用来确认 stage 切分语义和 JSON 配置项边界。

## Key Claims

- ZeRO 文档给出 ZeRO-1/2/3 对 optimizer state、gradient 和 parameter 的切分语义。
- getting started 与 tutorial 展示了 engine、config JSON 和常见训练配置入口。
- offload 与 precision 相关配置是理解显存优化取舍的重要资料。

## Limits Or Caveats

- 官方教程偏示例导向，复杂生产配置仍需结合源码和真实运行日志。
- DeepSpeed 版本差异较大，旧教程中的字段未必适用于当前版本。
- 与 FSDP 的行为差异不能只靠文档，需要用相同 workload 实测。

## Links To Concepts

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/activation-optimizer-checkpoint]]
- [[60-frameworks/deepspeed-megatron]]

## Follow Up

- 后续补充 ZeRO tutorial 的章节级定位。
- 后续补充和 PyTorch FSDP 对照的最小实验记录。
