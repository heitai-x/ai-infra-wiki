---
title: SLO And Observability References
type: source
source_type: official_doc
source_url: https://sre.google/sre-book/monitoring-distributed-systems/
topic: ops
component: observability
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [slo, observability, sli, sre, golden-signals]
---

# SLO And Observability References

## Why It Matters

`40-serving-platform/observability-slo-cost` 的指标体系、SLO 分解和告警原则，需要追溯到 SRE 经典文献、Prometheus / OpenTelemetry 生态以及 SLO 计算的标准做法，才能让 AI Infra 平台的观测层是“可解读、可比较”的。

## Key Claims

- 文档定义 SLI、SLO、error budget 的标准术语和计算方式。
- 文档提出 golden signals：latency、traffic、errors、saturation。
- 文档说明 USE 方法（utilization / saturation / errors）作为资源视角的补充。
- 文档解释 user-impact-first 告警原则，反对把 GPU util 当作主要告警源。
- 文档给出 burn rate alerting 的常见 pattern。

## Limits Or Caveats

- 通用 SRE 文献不直接覆盖 LLM serving 的 TTFT / TPOT / KV cache 指标，需要结合 serving runtime 文档。
- 实际告警阈值依赖业务容忍度，不能照搬通用数字。
- 文档多基于传统服务，AI 系统的 rollout、奖励、verifier 失败是补充维度。

## Links To Concepts

- [[40-serving-platform/observability-slo-cost]]
- [[30-inference-systems/llm-serving-map]]
- [[80-playbooks/serving-production-deployment]]

## Follow Up

- 后续补 Prometheus / OpenTelemetry collector 在 LLM serving 中的最小部署。
- 后续补 burn rate alert 的具体公式与样例。
