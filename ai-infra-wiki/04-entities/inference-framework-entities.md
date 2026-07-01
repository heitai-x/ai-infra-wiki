---
title: Inference Framework Entities
type: entity
source_type: curated
entity_type: framework

topic: inference
component: frameworks
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [entities, inference-frameworks, vllm, sglang, tensorrt-llm, triton]
---

# Inference Framework Entities

## vLLM

- Role: 高吞吐 LLM serving runtime。
- Main concepts: PagedAttention、paged KV cache、continuous batching、scheduler、OpenAI-compatible API。
- Best for learning: KV cache 管理和 serving scheduler。
- Links: [[60-frameworks/vllm-sglang]], [[30-inference-systems/kv-cache-paged-attention]]。

## SGLang

- Role: 高性能 LLM serving 和 structured generation runtime。
- Main concepts: scheduler、prefix/radix cache、speculative decoding、constrained decoding、multi-node serving。
- Best for learning: serving runtime 优化和端到端 benchmark。
- Links: [[60-frameworks/vllm-sglang]], [[30-inference-systems/batching-scheduling]]。

## TensorRT-LLM

- Role: NVIDIA GPU 上面向 LLM 的高性能推理优化栈。
- Main concepts: engine build、kernel fusion、quantization、in-flight batching。
- Best for learning: GPU vendor runtime、engine 化和量化 kernel 路径。
- Links: [[60-frameworks/tensorrt-triton-ray-kserve]], [[30-inference-systems/parallelism-quantization-speculation]]。

## Triton Inference Server

- Role: 生产推理服务器和多后端模型 serving 平台。
- Main concepts: model repository、backend、dynamic batching、ensemble、metrics。
- Best for learning: 生产推理服务形态和多模型部署。
- Links: [[60-frameworks/tensorrt-triton-ray-kserve]], [[40-serving-platform/serving-platform-map]]。

## Ray Serve

- Role: Python-first 分布式服务框架。
- Main concepts: deployment、replica、autoscaling、application graph。
- Best for learning: 应用逻辑与模型 serving 编排。
- Links: [[60-frameworks/tensorrt-triton-ray-kserve]], [[40-serving-platform/serving-platform-map]]。

## KServe

- Role: Kubernetes 原生模型 serving CRD 和平台 API。
- Main concepts: InferenceService、runtime、autoscaling、canary。
- Best for learning: 平台化模型部署和 Kubernetes 集成。
- Links: [[60-frameworks/tensorrt-triton-ray-kserve]], [[40-serving-platform/gpu-scheduling-kubernetes]]。
