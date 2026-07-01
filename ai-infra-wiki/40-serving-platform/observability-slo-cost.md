---
title: Observability SLO Cost
type: concept
topic: ops
component: observability
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [observability, slo, cost, metrics]
sources: [../raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.md]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# Observability SLO Cost

## 一句话

生产 AI Infra 需要同时看用户体验、GPU 利用、队列、错误、成本和质量。只看 GPU utilization 或 QPS 会误导系统决策。

## Training metrics

- step time p50/p95/p99。
- samples/sec、tokens/sec。
- loss、grad norm、nan/inf。
- GPU SM/memory/NVLink/NIC。
- NCCL time、dataloader wait、checkpoint time。
- rank skew、restart count。

## Serving metrics

- TTFT、TPOT、ITL、end-to-end latency。
- prompt tokens/sec、generation tokens/sec。
- queue time、running/waiting/swapped requests。
- KV cache utilization、free blocks、evictions。
- GPU memory、SM、HBM bandwidth。
- request errors、timeouts、cancellations。
- model quality guardrail metrics。

## SLO 分解

```text
end_to_end_latency
  = gateway + queue + tokenizer + prefill + decode + streaming/network
```

如果 SLO 只定义端到端延迟，排障时很难定位。应为每段建立指标和 budget。

## 成本模型

常见成本维度：

- GPU hour。
- tokens served。
- request count。
- model replica idle time。
- storage / network transfer。
- engineer incident time。

单 token 成本粗略：

```text
cost_per_token = gpu_hour_cost * gpu_hours / generated_tokens
```

需要按模型、租户、priority、region 拆分。

## 告警原则

- 用户体验优先：TTFT/TPOT/error rate。
- 容量风险：KV free blocks、queue length、GPU memory。
- 系统健康：worker restart、NCCL errors、model load failures。
- 成本异常：idle GPU、低 tokens/sec、高 reject。

## 本地证据

- 已落地 raw artifact：`raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.md`（Prometheus rules + Helm values）。
- 数字为 local-simulated，结构真实可用；升级到 `reliability: high` 是因为现在同时具备：SRE 文献 + serving 文档 + 本地 raw artifact。
- 进一步提升可信度的条件：用真实集群 Prometheus 数据覆盖 rules，并复制为新版本 raw artifact。

## 尚未本地验证的边界

- “只看 GPU utilization 或 QPS 会误导”是经验提醒，本页未引用具体误判案例。
- SLO 分解公式是结构化模型，各段 budget 依赖业务容忍度，本页未给出本机数字。
- 成本模型“单 token 成本”公式依赖 GPU hour cost 和 generated_tokens，本页未引用本机计费数据。

## 来源

- [[70-sources/official-docs/slo-observability-docs]]
- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/key-papers/distserve-paper]]

## 相关页面

- [[30-inference-systems/llm-serving-map]]
- [[20-training-systems/training-performance-playbook]]
- [[80-playbooks/serving-capacity-planning]]
