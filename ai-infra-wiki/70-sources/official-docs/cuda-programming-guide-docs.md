---
title: CUDA Programming Guide
type: source
source_type: official_doc
source_url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
topic: hardware
component: cuda
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [cuda, programming-guide, kernel, memory-model]
---

# CUDA Programming Guide

## Why It Matters

CUDA Programming Guide 是 `10-foundations/cuda-kernel-basics` 和 `10-foundations/memory-and-roofline` 的最权威官方来源，覆盖 execution model、memory hierarchy、occupancy、kernel launch、warp scheduling 和 Tensor Core 调用方式。

## Key Claims

- 文档定义 grid/block/warp/thread 层级和 launch 配置。
- 文档说明 register、shared memory、L1/L2、HBM、host memory 的带宽与一致性模型。
- 文档给出 occupancy 计算公式和限制因素。
- 文档解释 warp scheduler、latency hiding 与 latency-bound kernel 的关系。
- 文档覆盖 Tensor Core 的 WMMA / mma 调用与精度支持。

## Limits Or Caveats

- 文档不直接给出特定 GPU 的实测 peak FLOPS 或 HBM 带宽，需要结合 device-specific tuning guide。
- 文档描述的语义和某一具体 CUDA Toolkit 版本可能略有差异。
- AI Infra 性能判断必须结合 Nsight Compute / Systems 实际数据。

## Links To Concepts

- [[10-foundations/cuda-kernel-basics]]
- [[10-foundations/memory-and-roofline]]
- [[10-foundations/gpu-system-map]]
- [[80-playbooks/profiling-trace-playbook]]

## Follow Up

- 后续补 CUDA 12.x 与 cuDNN / cuBLAS 版本对应表。
- 后续补 Nsight Compute 关键指标速查表。
