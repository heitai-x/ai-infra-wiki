---
title: GPU Scheduling Kubernetes
type: concept
topic: serving
component: kubernetes
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [kubernetes, gpu-scheduling, topology]
sources: [../raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.md]
source_refs: [70-sources/official-docs/kserve-docs, 70-sources/official-docs/nvidia-k8s-device-plugin-docs, 70-sources/official-docs/ray-serve-docs]
---

# GPU Scheduling Kubernetes

## 一句话

GPU 调度不是简单把 pod 放到有空 GPU 的节点上。AI workload 需要考虑 GPU 型号、显存、拓扑、MIG、NUMA、网络、存储和模型加载时间。

## 调度维度

| 维度 | 为什么重要 |
|---|---|
| GPU type | H100/A100/L40S 等性能和显存不同 |
| GPU count | TP/PP 需要同一副本占多卡 |
| Topology | TP 需要高速 GPU-GPU 互联 |
| MIG | 隔离小模型，但限制互联和显存规格 |
| NUMA | CPU tokenizer / network 亲和影响 latency |
| NIC locality | 多机或 PD 分离依赖网络 |
| Storage locality | 模型权重加载和 checkpoint |
| Fragmentation | 多规格模型造成集群碎片 |

## Kubernetes 组件

- Device plugin：暴露 GPU 资源给 kubelet。
- Scheduler extender / framework plugin：实现拓扑、gang、quota 等策略。
- Node labels / taints / tolerations：表达硬件能力和隔离。
- RuntimeClass / container runtime：GPU container runtime。
- Autoscaler：节点池扩缩容。
- Operator：管理 GPU driver、DCGM exporter、runtime。

## Serving 特有问题

- 模型加载慢，扩容不是瞬时的。
- 副本需要预热 tokenizer、CUDA graph、KV cache pool。
- TP 副本需要 gang scheduling，否则只拿到部分 GPU 没法启动。
- 多租户下 GPU 碎片会导致高成本低利用。

## 本地证据

- 已落地 raw artifact：`raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.md`（Helm values + Prometheus rules）。
- 数字为 local-simulated，结构真实可用；升级到 `reliability: high` 是因为现在同时具备：官方文档 + 本地 raw artifact。
- 进一步提升可信度的条件：用真实集群部署覆盖配置，并复制为新版本 raw artifact。

## 尚未本地验证的边界

- “TP 副本需要 gang scheduling” 是正确性结论，但具体 scheduler extender / framework plugin 的实现依赖集群版本，本页未引用源码或实验。
- MIG / NUMA / NIC locality 的具体收益依赖硬件，本页未引用本机数字。
- “模型加载慢，扩容不是瞬时的”是经验结论，没有具体加载耗时数字。

## 来源

- [[70-sources/official-docs/kserve-docs]]
- [[70-sources/official-docs/nvidia-k8s-device-plugin-docs]]
- [[70-sources/official-docs/ray-serve-docs]]

## 相关页面

- [[40-serving-platform/serving-platform-map]]
- [[40-serving-platform/observability-slo-cost]]
- [[80-playbooks/benchmark-design]]
