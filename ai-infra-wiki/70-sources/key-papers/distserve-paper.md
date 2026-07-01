---
title: DistServe Paper
type: source
source_type: paper
source_url: https://arxiv.org/abs/2401.09670
topic: inference
component: disaggregated-serving
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [paper, distserve, disaggregation, serving]
---

# DistServe Paper

## Why It Matters

DistServe 是 prefill/decode 分离 serving 的代表论文，适合作为 disaggregated serving 与 goodput 优化问题的论文来源。

## Key Claims

- 论文强调 prefill 与 decode 的资源特征不同，适合拆开调度和部署。
- serving 优化目标不只是吞吐，也包括 goodput 与 SLO。
- disaggregation 带来更灵活的资源配置，但增加系统复杂度和网络依赖。

## Limits Or Caveats

- 论文中的系统假设和集群条件未必与本地部署一致。
- 分离架构的真实收益受网络、batching 和流量结构影响很大。

## Links To Concepts

- [[30-inference-systems/disaggregated-and-moe-serving]]
- [[30-inference-systems/llm-serving-map]]
- [[80-playbooks/serving-capacity-planning]]

## Follow Up

- 后续补 PD 分离下的指标与容量规划样例。
