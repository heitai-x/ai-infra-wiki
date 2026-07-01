---
title: Concept Index
type: index
topic: ai-infra
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [index, concepts]
---

# Concept Index

## 训练核心概念

| 概念 | 解决的问题 | 主要代价 | 入口 |
|---|---|---|---|
| DDP | 多卡复制参数并同步梯度 | all-reduce 通信 | [[20-training-systems/ddp-fsdp-zero]] |
| FSDP / ZeRO-3 | 切分参数、梯度、optimizer state | all-gather / reduce-scatter 更多 | [[20-training-systems/ddp-fsdp-zero]] |
| Tensor Parallel | 单层内矩阵切分 | 高频 collective | [[20-training-systems/tensor-pipeline-context-parallel]] |
| Pipeline Parallel | 层切分到不同 GPU | bubble、调度复杂度 | [[20-training-systems/tensor-pipeline-context-parallel]] |
| Context Parallel | 长上下文序列维切分 | attention 通信 | [[20-training-systems/tensor-pipeline-context-parallel]] |
| Expert Parallel | MoE expert 切分 | router、all-to-all、负载不均 | [[20-training-systems/expert-parallel-moe]] |
| Activation Checkpoint | 降低 activation 显存 | 重算开销 | [[20-training-systems/activation-optimizer-checkpoint]] |
| Distributed Checkpoint | 大规模状态恢复 | IO、元数据、一致性 | [[20-training-systems/activation-optimizer-checkpoint]] |

## 推理核心概念

| 概念 | 解决的问题 | 主要代价 | 入口 |
|---|---|---|---|
| Prefill / Decode | 区分 prompt 计算与逐 token 生成 | 两阶段资源特性不同 | [[30-inference-systems/llm-serving-map]] |
| KV Cache | 避免重复计算历史 token | 显存随并发和上下文增长 | [[30-inference-systems/kv-cache-paged-attention]] |
| Paged KV | 降低 KV 内存碎片和浪费 | 页表/调度复杂度 | [[30-inference-systems/kv-cache-paged-attention]] |
| Continuous Batching | 提高 decode 阶段吞吐 | 调度公平性和尾延迟 | [[30-inference-systems/batching-scheduling]] |
| Speculative Decoding | 用草稿模型减少大模型步数 | 接受率、系统集成复杂度 | [[30-inference-systems/parallelism-quantization-speculation]] |
| Quantization | 降低权重/KV/激活成本 | 精度、kernel 支持、校准 | [[30-inference-systems/parallelism-quantization-speculation]] |
| Disaggregated Serving | 分离 prefill 与 decode 资源池 | 网络传 KV、调度复杂 | [[30-inference-systems/disaggregated-and-moe-serving]] |

## 性能与运维概念

| 概念 | 使用场景 | 入口 |
|---|---|---|
| MFU / HFU | 训练算力利用率评估 | [[20-training-systems/training-performance-playbook]] |
| TTFT / TPOT | LLM serving 延迟拆解 | [[30-inference-systems/llm-serving-map]] |
| Roofline | 判断算子 compute-bound 或 memory-bound | [[10-foundations/memory-and-roofline]] |
| SLO / Error Budget | 平台级可靠性目标 | [[40-serving-platform/observability-slo-cost]] |
| Hybrid Search | Wiki/RAG 检索召回 | [[50-rag-agent-infra/embedding-retrieval-agent-infra]] |
