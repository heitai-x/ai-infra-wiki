---
title: AI Infra Skill Tree
type: roadmap
topic: ai-infra
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [roadmap, skill-tree]
---

# AI Infra Skill Tree

## Level 0: 系统语言

目标：能用同一套语言描述训练、推理、平台问题。

- 张量 shape、dtype、layout、stride。
- FLOPs、bandwidth、latency、throughput、utilization。
- GPU memory hierarchy、host/device transfer、collective communication。
- queueing、batching、SLO、backpressure。

对应页面：

- [[10-foundations/gpu-system-map]]
- [[10-foundations/memory-and-roofline]]
- [[10-foundations/nccl-and-networking]]

## Level 1: 单机 GPU 与 kernel

目标：能解释一个 PyTorch op 最终如何变成 kernel timeline。

- CUDA execution model。
- memory coalescing、shared memory、tensor core。
- profiler timeline：CPU launch、GPU kernel、memcpy、NCCL。
- roofline 估算。

对应页面：

- [[10-foundations/cuda-kernel-basics]]
- [[10-foundations/memory-and-roofline]]

## Level 2: 分布式训练

目标：能画出一个 8 机 64 卡训练 step 的状态流。

- DDP：replica + gradient all-reduce。
- FSDP / ZeRO：参数、梯度、optimizer state sharding。
- TP / PP / CP / EP：模型切分维度和通信模式。
- checkpoint、fault tolerance、data pipeline。

对应页面：

- [[20-training-systems/distributed-training-map]]
- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/tensor-pipeline-context-parallel]]
- [[20-training-systems/expert-parallel-moe]]

## Level 3: 训练性能工程

目标：能把慢 step 拆成可证伪假设。

- MFU / HFU / step time breakdown。
- compute-communication overlap。
- pipeline bubble。
- straggler、NCCL timeout、dataloader bottleneck。
- checkpoint stall。

对应页面：

- [[20-training-systems/training-performance-playbook]]
- [[80-playbooks/nccl-hang-triage]]
- [[80-playbooks/fsdp-zero-oom-triage]]

## Level 4: LLM 推理系统

目标：能解释 LLM serving 的吞吐、延迟和显存之间的交换。

- Prefill / decode。
- KV cache 和 paged KV。
- continuous batching、scheduler、admission control。
- TP/PP inference、quantization、speculative decoding。
- disaggregated serving 和 MoE serving。

对应页面：

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/batching-scheduling]]
- [[30-inference-systems/parallelism-quantization-speculation]]

## Level 5: Serving 平台

目标：能设计多模型、多租户、有 SLO 的 GPU serving 平台。

- Gateway、routing、rate limit、quota。
- Model registry、deployment、canary、rollback。
- Kubernetes GPU scheduling、Triton、Ray Serve、KServe。
- observability、capacity planning、cost accounting。

对应页面：

- [[40-serving-platform/serving-platform-map]]
- [[40-serving-platform/gpu-scheduling-kubernetes]]
- [[40-serving-platform/observability-slo-cost]]

## Level 6: AI 应用 Infra

目标：能区分模型 serving、RAG、agent runtime、MLOps 各自边界。

- embedding pipeline、chunking、vector DB、hybrid search。
- reranker、retrieval eval、prompt/cache/eval。
- tool calling、agent runtime、feedback loop。

对应页面：

- [[50-rag-agent-infra/embedding-retrieval-agent-infra]]
- [[50-rag-agent-infra/evaluation-feedback-loop]]
