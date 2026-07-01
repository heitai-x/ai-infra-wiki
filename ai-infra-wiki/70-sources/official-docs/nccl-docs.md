---
title: NCCL Docs
type: source
source_type: official_doc
source_url: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/
topic: hardware
component: nccl
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [nccl, docs, collectives, networking]
---

# NCCL Docs

## Why It Matters

NCCL 文档是 collective 语义、环境变量、网络配置和故障排查入口的第一手资料。涉及 hang、接口选择、拓扑和通信调优时，应优先引用它。

## Key Claims

- 文档定义 all-reduce、all-gather、reduce-scatter、all-to-all 等 collective 的使用边界。
- 用户指南给出 `NCCL_DEBUG`、网络接口和拓扑相关环境变量的说明。
- 对网络和拓扑问题，NCCL 文档是训练/推理通信排障的基础资料。

## Limits Or Caveats

- 文档说明的是 NCCL 自身行为，不等于 PyTorch 或框架封装层的异常处理逻辑。
- 真正的 hang 往往涉及 rank 状态、dataloader、OOM 或容器设备可见性，不能只看 NCCL 文档。
- 网络与性能结论必须结合拓扑、日志和 benchmark 证据。

## Links To Concepts

- [[10-foundations/nccl-and-networking]]
- [[80-playbooks/nccl-hang-triage]]
- [[80-playbooks/nccl-network-baseline]]

## Follow Up

- 后续补通信环境变量与常见错误码速查表。
- 后续补 raw `NCCL_DEBUG=INFO` 样例日志。
