---
title: Megatron Core Docs
type: source
source_type: official_doc
source_url: https://docs.nvidia.com/megatron-core/developer-guide/latest/
topic: training
component: megatron-core
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [megatron, docs, tensor-parallel, pipeline-parallel, moe]
---

# Megatron Core Docs

## Why It Matters

Megatron-Core 文档是 TP、PP、CP、EP、distributed optimizer 和大模型训练组件化设计的权威入口，适合用来对齐多维并行的官方术语和组件边界。

## Key Claims

- 文档覆盖 tensor parallel、pipeline parallel、context/sequence parallel、MoE 与 distributed optimizer 等核心并行组件。
- developer guide 能帮助定位并行组、模块拆分和训练配方的官方约定。
- 对 Megatron-LM 相关实现问题，文档和 GitHub 仓库应一起阅读。

## Limits Or Caveats

- 文档更偏组件说明，不会完整覆盖所有 launch 细节和版本迁移问题。
- 并行策略组合的真实性能仍依赖硬件拓扑、micro-batch 和 workload。
- 某些新特性会先出现在仓库或 release note 中，再进入文档。

## Links To Concepts

- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[20-training-systems/expert-parallel-moe]]
- [[60-frameworks/deepspeed-megatron]]

## Follow Up

- 后续补充开发指南中的并行章节定位。
- 后续补 Megatron-LM 代码入口和训练脚本 source card。
