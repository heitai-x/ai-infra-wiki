---
title: Source Index
type: index
topic: ai-infra
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [index, sources, references]
---

# Source Index

## 官方文档总导航

- [[70-sources/official-docs]]：官方文档总导航与拆分说明。

## 官方文档细粒度 source cards

- [[70-sources/official-docs/mlsys-book-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/deepspeed-docs]]
- [[70-sources/official-docs/megatron-core-docs]]
- [[70-sources/official-docs/nccl-docs]]
- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/tensorrt-llm-docs]]
- [[70-sources/official-docs/triton-inference-server-docs]]
- [[70-sources/official-docs/ray-serve-docs]]
- [[70-sources/official-docs/kserve-docs]]
- [[70-sources/official-docs/nvidia-k8s-device-plugin-docs]]

## 论文总导航

- [[70-sources/key-papers]]：关键论文总导航与拆分说明。

## 论文细粒度 source cards

- [[70-sources/key-papers/zero-paper]]
- [[70-sources/key-papers/megatron-lm-paper]]
- [[70-sources/key-papers/gpipe-paper]]
- [[70-sources/key-papers/pipedream-paper]]
- [[70-sources/key-papers/gshard-paper]]
- [[70-sources/key-papers/switch-transformer-paper]]
- [[70-sources/key-papers/flashattention-papers]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/speculative-decoding-paper]]
- [[70-sources/key-papers/distserve-paper]]

## 使用规则

1. 官方文档优先用于 API、配置、命令、支持矩阵。
2. 论文优先用于机制动机、算法设计、实验定义。
3. 代码优先用于真实行为和边界条件。
4. benchmark 和 trace 优先用于性能结论。
5. 任何“最佳实践”都必须记录硬件、模型、框架版本、precision、workload、启动命令和评测命令。
6. 优先引用细粒度 source card；聚合页只作为导航入口。
