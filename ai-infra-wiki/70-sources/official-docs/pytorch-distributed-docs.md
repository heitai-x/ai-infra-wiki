---
title: PyTorch Distributed Docs
type: source
source_type: official_doc
source_url: https://docs.pytorch.org/docs/stable/distributed.html
topic: training
component: pytorch-distributed
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [pytorch, distributed, docs, fsdp, dtensor]
---

# PyTorch Distributed Docs

## Why It Matters

PyTorch Distributed 是 DDP、FSDP、DTensor、Tensor Parallel 和 distributed checkpoint 的原始定义入口。涉及 API、默认行为和概念边界时，应优先回到这组官方文档。

## Key Claims

- `torch.distributed` 定义 process group、collective、rank/world size 等基础分布式抽象。
- FSDP 文档解释参数分片、all-gather、reduce-scatter、reshard 和 auto wrap 等关键机制。
- DTensor/Tensor Parallel 文档是 PyTorch 原生张量并行接口和 placement 语义的官方来源。
- 训练系统页涉及 API、配置项和行为边界时，优先引用这组官方文档而不是二手博客。

## Limits Or Caveats

- PyTorch 文档随版本变化较快，升级版本后要复查 API 页面。
- 文档解释的是抽象和推荐用法，不等于某个上层框架的实际封装行为。
- 性能结论仍需 profiler、benchmark 和代码路径共同验证。

## Links To Concepts

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[80-playbooks/fsdp-zero-oom-triage]]
- [[60-frameworks/pytorch-distributed]]

## Follow Up

- 后续补充具体版本号和关键 API 章节定位。
- 后续将本地导出的关键文档页放入 `raw-sources/`，形成页面级来源追踪。
