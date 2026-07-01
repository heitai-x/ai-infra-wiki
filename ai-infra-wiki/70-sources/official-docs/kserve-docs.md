---
title: KServe Docs
type: source
source_type: official_doc
source_url: https://kserve.github.io/website/
topic: serving
component: kserve
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [kserve, docs, kubernetes, serving]
---

# KServe Docs

## Why It Matters

KServe 文档是 Kubernetes 原生模型服务 API、InferenceService 和平台化部署流程的官方入口，适合用来约束平台控制面的术语和对象模型。

## Key Claims

- 文档覆盖 InferenceService、自定义 runtime 与 Kubernetes 集成方式。
- KServe 是模型平台层的标准化接口之一，适合用来理解声明式部署与服务治理。
- 需要讨论 K8s 原生 serving API 时，应优先回到 KServe 官方文档。

## Limits Or Caveats

- KServe 解决的是平台接口与编排，不直接回答 KV cache 或 LLM scheduler 细节。
- 生产部署行为还会受 Istio、Knative、GPU plugin 和 runtime 选择影响。

## Links To Concepts

- [[40-serving-platform/gpu-scheduling-kubernetes]]
- [[40-serving-platform/serving-platform-map]]
- [[60-frameworks/tensorrt-triton-ray-kserve]]

## Follow Up

- 后续补 InferenceService 字段级例子和 rollout 样例。
