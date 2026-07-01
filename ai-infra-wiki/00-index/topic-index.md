---
title: Topic Index
type: index
topic: ai-infra
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [index, topics]
---

# Topic Index

## 基础层

- [[10-foundations/gpu-system-map]]：GPU、SM、HBM、NVLink、PCIe、NVSwitch、CPU host 的系统图。
- [[10-foundations/cuda-kernel-basics]]：kernel、thread/block/grid、occupancy、memory coalescing。
- [[10-foundations/memory-and-roofline]]：compute-bound / memory-bound、roofline、带宽估算。
- [[10-foundations/model-architecture-cost-formulas]]：模型结构到参数量、FLOPs、activation、KV cache 成本。
- [[10-foundations/nccl-and-networking]]：collective、拓扑、IB/RoCE、NCCL hang 排查入口。

## 分布式训练

- [[20-training-systems/distributed-training-map]]：训练 step 总图。
- [[20-training-systems/ddp-fsdp-zero]]：DDP、FSDP、ZeRO 的状态切分与通信。
- [[20-training-systems/tensor-pipeline-context-parallel]]：TP、PP、SP/CP。
- [[20-training-systems/expert-parallel-moe]]：MoE、router、expert parallel、all-to-all。
- [[20-training-systems/activation-optimizer-checkpoint]]：activation checkpoint、optimizer state、distributed checkpoint。
- [[20-training-systems/data-pipeline-fault-tolerance]]：数据流、容错、恢复。
- [[20-training-systems/rl-post-training-infra]]：RLHF/GRPO/PPO 类 post-training 的 rollout、reward、训练耦合。
- [[20-training-systems/training-performance-playbook]]：MFU、bubble、straggler、overlap。

## 推理系统

- [[30-inference-systems/llm-serving-map]]：prefill/decode、scheduler、KV cache、SLO。
- [[30-inference-systems/kv-cache-paged-attention]]：KV cache 与 paged memory。
- [[30-inference-systems/batching-scheduling]]：continuous batching、admission control、fairness。
- [[30-inference-systems/parallelism-quantization-speculation]]：推理并行、量化、投机解码。
- [[30-inference-systems/prefix-cache-chunked-prefill-preemption]]：prefix/radix cache、chunked prefill、preemption/swap。
- [[30-inference-systems/disaggregated-and-moe-serving]]：PD 分离、MoE serving。

## 服务平台

- [[40-serving-platform/serving-platform-map]]：多模型、多租户、网关、调度、runtime。
- [[40-serving-platform/gpu-scheduling-kubernetes]]：Kubernetes GPU 调度和拓扑。
- [[40-serving-platform/observability-slo-cost]]：指标、追踪、日志、成本、SLO。

## RAG / Agent Infra

- [[50-rag-agent-infra/embedding-retrieval-agent-infra]]：embedding、chunk、hybrid search、reranker。
- [[50-rag-agent-infra/evaluation-feedback-loop]]：离线评测、在线反馈、数据闭环。

## 框架

- [[60-frameworks/source-walkthrough-protocol]]
- [[60-frameworks/pytorch-distributed]]
- [[60-frameworks/deepspeed-megatron]]
- [[60-frameworks/vllm-sglang]]
- [[60-frameworks/tensorrt-triton-ray-kserve]]
