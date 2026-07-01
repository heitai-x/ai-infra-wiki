---
title: Serving Platform Map
type: concept
topic: serving
component: platform
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [serving-platform, kubernetes, multi-tenant]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/triton-inference-server-docs, 70-sources/official-docs/ray-serve-docs, 70-sources/official-docs/kserve-docs, 70-sources/official-docs/nvidia-k8s-device-plugin-docs, 70-sources/official-docs/tensorrt-llm-docs, 70-sources/key-papers/distserve-paper]
---

# Serving Platform Map

## 一句话

Serving 平台把模型 runtime 变成可上线、可扩缩、可隔离、可观测、可计费、可回滚的生产系统。

## 控制面与数据面

```text
Control plane:
  model registry -> deployment controller -> scheduler/autoscaler -> rollout/rollback

Data plane:
  gateway -> router -> model server/runtime -> GPU workers -> streaming response
```

## 平台组件

| 组件 | 职责 |
|---|---|
| Model registry | 权重、tokenizer、config、版本、artifact provenance |
| Gateway | auth、quota、rate limit、API compatibility |
| Router | model/tenant 路由、负载均衡、灰度 |
| Runtime | vLLM、SGLang、TensorRT-LLM、Triton、custom backend |
| Scheduler | GPU placement、replica scaling、batch policy |
| Observability | metric、log、trace、profiling、alert |
| Cost accounting | GPU hour、token、tenant、model 维度成本 |
| Release | canary、rollback、compatibility test |

## 多租户问题

- 租户 quota 和 rate limit。
- 请求优先级与公平性。
- GPU 显存隔离和 noisy neighbor。
- 模型权重共享与安全边界。
- 成本归因。
- SLO 分层：premium / best-effort。

## 设计输出

一个 serving 平台设计文档至少要包含：

- 支持的模型类型和最大规格。
- 延迟和吞吐 SLO。
- 单模型容量规划。
- 扩缩容策略。
- 失败模式和降级策略。
- 观测指标和报警。
- 上线、灰度、回滚流程。

## 本地证据

- 暂无 `raw-sources/serving/` 下的真实 platform 部署 YAML、rollout / rollback 决策记录、多租户 SLO 样本。
- 章节中控制面 / 数据面、平台组件、多租户问题、设计输出属于对 vLLM / Triton / Ray Serve / KServe / TensorRT-LLM 文档 + DistServe 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/serving/platform-<cluster>.md`，含部署 YAML、canary / rollback 决策记录、多租户 SLO 与成本归因样本。

## 尚未本地验证的边界

- “控制面 / 数据面”划分是通用工程视角，不等于某个 platform 的实际模块名。
- 多租户 quota / 优先级 / 公平性 / noisy neighbor 是策略方向，没有具体收益数字。
- 设计输出清单是模板要求，不构成已验证的 platform 设计。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/triton-inference-server-docs]]
- [[70-sources/official-docs/ray-serve-docs]]
- [[70-sources/official-docs/kserve-docs]]
- [[70-sources/official-docs/nvidia-k8s-device-plugin-docs]]
- [[70-sources/official-docs/tensorrt-llm-docs]]
- [[70-sources/key-papers/distserve-paper]]

## 相关页面

- [[40-serving-platform/gpu-scheduling-kubernetes]]
- [[40-serving-platform/observability-slo-cost]]
- [[80-playbooks/serving-production-deployment]]
- [[80-playbooks/serving-capacity-planning]]
