---
title: TensorRT Triton Ray KServe
type: source
topic: serving
component: production-serving
level: intermediate
status: active
source_type: official_doc
source_url: https://nvidia.github.io/TensorRT-LLM/
last_updated: 2026-06-13
last_checked: 2026-06-13
owner: local
reliability: high
tags: [tensorrt-llm, triton, ray-serve, kserve, serving]
---

# TensorRT Triton Ray KServe

## 为什么重要

生产推理平台通常不只运行一个 LLM runtime。TensorRT-LLM 关注 NVIDIA GPU 上的 LLM 优化，Triton 关注统一模型服务后端，Ray Serve 和 KServe 关注分布式服务编排和 Kubernetes 原生部署。

## TensorRT-LLM

关注点：

- build engine、kernel fusion、quantization、in-flight batching。
- NVIDIA GPU 上的高性能推理路径。
- 与 Triton backend 或自定义服务集成。

来源：https://nvidia.github.io/TensorRT-LLM/

## Triton Inference Server

关注点：

- 多框架模型 serving。
- model repository。
- dynamic batching、ensemble、backend。
- metrics 和 production deployment。

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/

## Ray Serve

关注点：

- Python 原生分布式 serving。
- autoscaling、deployment graph、replica。
- 与 Ray 集群和应用逻辑结合。

来源：https://docs.ray.io/en/latest/serve/index.html

## KServe

关注点：

- Kubernetes 原生 InferenceService。
- serverless/autoscaling、model runtime、canary。
- 平台化模型部署 API。

来源：https://kserve.github.io/website/

## 选择思路

| 需求 | 优先考虑 |
|---|---|
| NVIDIA 官方 LLM 优化路径，适合 engine、量化、IFB 和 NVIDIA GPU 特性评估 | TensorRT-LLM |
| 多模型/多框架统一服务 | Triton |
| Python 应用逻辑和动态服务图 | Ray Serve |
| Kubernetes 平台 CRD 和标准化部署 | KServe |

## 相关页面

- [[40-serving-platform/serving-platform-map]]
- [[40-serving-platform/gpu-scheduling-kubernetes]]
- [[80-playbooks/benchmark-design]]
