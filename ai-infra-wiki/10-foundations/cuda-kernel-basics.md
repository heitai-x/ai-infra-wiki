---
title: CUDA Kernel Basics
type: concept
topic: hardware
component: cuda
level: beginner
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [cuda, kernel, profiling]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# CUDA Kernel Basics

## 一句话

CUDA kernel 是 GPU 上执行计算的基本单位。AI Infra 中的 PyTorch、Triton、TensorRT-LLM、vLLM kernel 最终都会表现为 profiler timeline 上的一段 kernel 执行。

## 执行模型

- Grid：一次 kernel launch 的全局任务集合。
- Block：被调度到 SM 上执行的线程组。
- Thread：最小执行上下文。
- Warp：通常是 32 个 thread 的调度单位。
- Occupancy：SM 上可同时驻留的 warp/block 比例，受 register、shared memory、block size 限制。

## 内存层级

| 层级 | 特性 | 性能影响 |
|---|---|---|
| Register | 每线程最快 | register pressure 会降低 occupancy 或 spill |
| Shared memory | block 内共享 | 适合 tile，但有 bank conflict 风险 |
| L2 | 全 GPU 共享缓存 | 影响重复读和跨 SM 数据复用 |
| HBM | 大容量高带宽 | decode、embedding、elementwise 常受其限制 |
| Host memory | CPU 侧 | host-device transfer 会造成 pipeline 空洞 |

## 常见 kernel 类型

- GEMM：Transformer 中线性层主力，通常依赖 Tensor Cores。
- Attention：QK、softmax、PV，可被 FlashAttention 类 kernel 融合优化。
- Elementwise：LayerNorm、RMSNorm、activation、residual，常受 memory bandwidth 影响。
- Reduction：loss、norm、softmax 归约。
- NCCL kernel：collective communication 在 GPU timeline 中也表现为 kernel。

## 读 profiler 的顺序

1. 是否有 CPU gap：kernel launch 之间是否有空洞。
2. 是否有大量小 kernel：可能需要 fusion 或 CUDA graph。
3. GEMM 是否占主要时间：看 tensor core 利用率和 shape。
4. Attention 是否随 seq len 放大：看 prefill/long context。
5. NCCL 是否与 compute overlap：看通信是否挡住 backward 或 forward。

## 常见误区

- GPU utilization 高不等于模型快；可能是低效 kernel 占满了 GPU。
- 占用率高不一定好；memory-bound kernel 提高 occupancy 未必改善。
- 单个 kernel 快不等于端到端快；调度、通信、队列、IO 可能主导。

## 来源

- [[70-sources/official-docs/cuda-programming-guide-docs]]
- [[70-sources/official-docs/pytorch-profiler-docs]]
- [[70-sources/official-docs/mlsys-book-docs]]

## 相关页面

- [[10-foundations/memory-and-roofline]]
- [[20-training-systems/training-performance-playbook]]
- [[30-inference-systems/batching-scheduling]]
