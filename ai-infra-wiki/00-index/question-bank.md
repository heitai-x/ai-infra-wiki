---
title: Question Bank
type: eval-set
topic: ai-infra
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [rag, evaluation, questions]
---

# Question Bank

这些问题用于评测 Wiki/RAG 是否真的能支撑系统学习。回答必须引用 Wiki 页面或 source card。

## 基础层

1. 一次 GPU kernel 执行中，SM、register、shared memory、L2、HBM 分别承担什么角色？
2. 如何判断一个算子是 compute-bound 还是 memory-bound？
3. PCIe、NVLink、NVSwitch、IB/RoCE 对训练和推理瓶颈分别有什么影响？
4. NCCL all-reduce、reduce-scatter、all-gather、all-to-all 的输入输出语义是什么？
5. 为什么拓扑不匹配会导致多机训练 step time 抖动？

## 分布式训练

1. DDP、FSDP、ZeRO-2、ZeRO-3 分别切分了哪些状态？
2. Tensor Parallel 和 Pipeline Parallel 的通信模式有什么不同？
3. 为什么 Pipeline Parallel 会出现 bubble？micro-batch 如何影响 bubble？
4. Context Parallel 解决长上下文训练的什么问题？
5. MoE 的 Expert Parallel 为什么常见 all-to-all 瓶颈？
6. Activation checkpointing 的显存收益和重算成本如何估算？
7. Distributed checkpoint 需要解决哪些一致性和恢复问题？
8. 如何定位训练慢在 dataloader、通信、kernel、checkpoint 还是 straggler？

## 推理系统

1. Prefill 和 decode 在计算/内存瓶颈上有什么不同？
2. KV cache 显存如何随 batch、context length、layer、hidden size、dtype 变化？
3. PagedAttention 或 paged KV cache 解决了什么内存管理问题？
4. Continuous batching 为什么能提高吞吐？它如何影响尾延迟？
5. TTFT、TPOT、ITL、QPS、throughput 的关系是什么？
6. Speculative decoding 的收益取决于哪些因素？
7. 量化权重、activation、KV cache 的风险分别是什么？
8. Disaggregated serving 为什么要拆 prefill 和 decode？代价是什么？

## 平台工程

1. 一个多租户 LLM serving 平台至少需要哪些组件？
2. GPU 调度为什么需要考虑拓扑、MIG、NUMA、网络亲和？
3. Serving SLO 应该如何拆成 admission control、queueing、runtime、network 指标？
4. 如何设计一次 vLLM vs TensorRT-LLM vs SGLang 的公平 benchmark？
5. 模型上线 canary、rollback、capacity guardrail 应该记录哪些证据？

## RAG / Agent Infra

1. Wiki RAG 为什么需要 hybrid search，而不是只用向量检索？
2. Chunking 策略如何影响召回和引用质量？
3. reranker、query rewrite、metadata filter 各自解决什么问题？
4. 如何评测一个 AI Infra Wiki RAG 的回答是否可信？
5. Agent runtime 与普通 RAG 系统的边界在哪里？
