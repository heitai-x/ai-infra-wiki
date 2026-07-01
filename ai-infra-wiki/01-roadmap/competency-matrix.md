---
title: Competency Matrix
type: roadmap
topic: ai-infra
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [competency, assessment]
---

# Competency Matrix

## Beginner

你能：

- 解释训练 step 和推理请求生命周期。
- 说清楚 GPU 显存、算力、通信、IO 的基本瓶颈。
- 区分 DDP、FSDP、TP、PP、KV cache、continuous batching。
- 跑通一个单机多卡训练和一个 LLM serving demo。

证据：

- 画出训练 step 图。
- 写出 KV cache 显存公式。
- 提交一次带命令、日志、metric 的实验记录。

## Intermediate

你能：

- 从 profiler 或日志定位训练/推理瓶颈。
- 估算 FSDP/ZeRO、TP/PP、KV cache、batching 对显存和性能的影响。
- 设计公平 benchmark。
- 写一份 incident playbook。

证据：

- 对同一 workload 比较至少两个训练/推理配置。
- 对一次 OOM 或 latency regression 给出证据链。
- 能说明一个框架参数为什么改变吞吐或延迟。

## Advanced

你能：

- 修改框架代码或 kernel 改善性能。
- 设计多租户 GPU serving 平台。
- 处理多机通信、straggler、checkpoint、调度和 SLO 的综合问题。
- 建立可持续维护的 Wiki/RAG/benchmark 体系。

证据：

- 有可复现 patch、profile、benchmark before/after。
- 有覆盖生产场景的 capacity plan。
- 有带 source citation 的 Wiki/RAG 评测集和回归结果。
