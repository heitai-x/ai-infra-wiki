---
title: NVIDIA K8s Device Plugin Docs
type: source
source_type: official_doc
source_url: https://github.com/NVIDIA/k8s-device-plugin
topic: serving
component: kubernetes-gpu
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [kubernetes, gpu, nvidia, device-plugin, docs]
---

# NVIDIA K8s Device Plugin Docs

## Why It Matters

NVIDIA Kubernetes Device Plugin 是 Kubernetes 暴露和编排 NVIDIA GPU 资源的基础组件之一，是理解 GPU 资源发现、分配和节点能力暴露的重要官方入口。

## Key Claims

- 文档说明了如何在 Kubernetes 中向调度器暴露 NVIDIA GPU 资源。
- 它是 GPU 资源可见性、节点配置和运行时依赖关系的关键参考。
- 涉及 GPU 资源分配、device plugin 配置和部署问题时，应优先引用此来源。

## Limits Or Caveats

- 该插件只覆盖资源暴露与分配，不等于完整的 serving 平台方案。
- 实际部署还受到 container runtime、driver、MIG、节点拓扑和集群策略影响。
- 平台级行为仍需结合 KServe、调度器配置和集群运维实践一起分析。

## Links To Concepts

- [[40-serving-platform/gpu-scheduling-kubernetes]]
- [[40-serving-platform/serving-platform-map]]
- [[80-playbooks/serving-production-deployment]]

## Follow Up

- 后续补 MIG、runtime class 和常见部署参数速查表。
- 后续补本地集群部署 YAML 或 Helm values 到 `raw-sources/`。
