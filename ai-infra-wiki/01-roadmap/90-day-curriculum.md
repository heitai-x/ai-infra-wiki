---
title: 90 Day Curriculum
type: roadmap
topic: ai-infra
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [curriculum, roadmap]
---

# 90 Day Curriculum

## 第 1-2 周：GPU / CUDA / NCCL 基础

目标：

- 能读懂一个 profiler timeline。
- 能解释 all-reduce、all-gather、reduce-scatter。
- 能做简单 roofline 估算。

阅读：

- [[10-foundations/gpu-system-map]]
- [[10-foundations/cuda-kernel-basics]]
- [[10-foundations/memory-and-roofline]]
- [[10-foundations/nccl-and-networking]]

练习：

- 运行矩阵乘、elementwise、reduction，比较 FLOPs 与带宽瓶颈。
- 用 `nccl-tests` 或框架通信 benchmark 测 all-reduce 带宽。

## 第 3-5 周：分布式训练主线

目标：

- 能画出 DDP/FSDP/ZeRO 的状态分布。
- 能解释 TP/PP/CP/EP 的通信形态。
- 能对一次 OOM 给出显存账本。

阅读：

- [[20-training-systems/distributed-training-map]]
- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[20-training-systems/expert-parallel-moe]]
- [[60-frameworks/pytorch-distributed]]
- [[60-frameworks/deepspeed-megatron]]

练习：

- 跑 DDP 与 FSDP 小实验，记录参数、梯度、optimizer state 显存。
- 对同一模型尝试 activation checkpointing，比较显存和 step time。

## 第 6-7 周：训练性能与可靠性

目标：

- 能拆 step time。
- 能定位 dataloader、communication、kernel、checkpoint 问题。
- 能写训练故障复盘。

阅读：

- [[20-training-systems/training-performance-playbook]]
- [[20-training-systems/data-pipeline-fault-tolerance]]
- [[80-playbooks/nccl-hang-triage]]
- [[80-playbooks/fsdp-zero-oom-triage]]

练习：

- 制造 dataloader sleep、NCCL 超时、checkpoint stall，记录指标和日志。

## 第 8-10 周：LLM serving 主线

目标：

- 能解释 prefill/decode 的瓶颈差异。
- 能估算 KV cache。
- 能读懂 vLLM/SGLang serving 参数。

阅读：

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/batching-scheduling]]
- [[30-inference-systems/parallelism-quantization-speculation]]
- [[60-frameworks/vllm-sglang]]

练习：

- 部署一个 7B/14B 模型，改变 max seq len、batch、TP、quantization，记录 TTFT、TPOT、显存。

## 第 11-12 周：Serving 平台与 RAG/Agent Infra

目标：

- 能设计多租户 serving 平台。
- 能写公平 benchmark 计划。
- 能搭建 Wiki/RAG 的 ingestion、metadata、eval。

阅读：

- [[40-serving-platform/serving-platform-map]]
- [[40-serving-platform/gpu-scheduling-kubernetes]]
- [[40-serving-platform/observability-slo-cost]]
- [[50-rag-agent-infra/embedding-retrieval-agent-infra]]
- [[02-llm-wiki-workflow/rag-metadata-schema]]

练习：

- 写一次 serving 容量规划。
- 用 [[00-index/question-bank]] 评测 Wiki/RAG。
