---
title: TensorRT-LLM Docs
type: source
source_type: official_doc
source_url: https://nvidia.github.io/TensorRT-LLM/
topic: inference
component: tensorrt-llm
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [tensorrt-llm, docs, inference, quantization, engine]
---

# TensorRT-LLM Docs

## Why It Matters

TensorRT-LLM 文档是 NVIDIA GPU 上高性能 LLM 推理优化的重要官方入口，覆盖 engine、量化、并行和 deployment 相关能力。

## Key Claims

- 文档说明了 TensorRT-LLM 的构建、量化、部署和 benchmark 工作流。
- 它是理解 NVIDIA 特定优化路径、engine 生命周期和 serving 集成方式的一手资料。
- 对涉及 TensorRT-LLM 参数、量化能力和部署方式的结论，应优先回到该文档。

## Limits Or Caveats

- 文档内容高度依赖 CUDA、驱动、TensorRT 和 GPU 代际。
- 某些优化路径只适用于特定模型或特定量化格式。
- 真实性能仍需本地 benchmark 与 profiling 验证。

## Links To Concepts

- [[30-inference-systems/parallelism-quantization-speculation]]
- [[40-serving-platform/serving-platform-map]]
- [[60-frameworks/tensorrt-triton-ray-kserve]]

## Follow Up

- 后续补量化格式、engine build 和部署路径的速查表。
- 后续补本地导出的关键版本文档快照到 `raw-sources/`。
