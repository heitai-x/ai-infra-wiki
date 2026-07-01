---
title: GPU System Map
type: concept
topic: hardware
component: gpu
level: beginner
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [gpu, hardware, memory, topology]
source_refs: [70-sources/official-docs/nccl-docs, 70-sources/official-docs/cuda-programming-guide-docs, 70-sources/official-docs/mlsys-book-docs]
---

# GPU System Map

## 一句话

AI Infra 的性能问题最终会落到几类硬件资源：GPU SM 算力、HBM 带宽/容量、GPU 间互联、CPU host、网络和存储。理解系统图比记框架参数更重要。

## 关键组件

| 组件 | 作用 | 常见瓶颈信号 |
|---|---|---|
| SM | 执行 CUDA cores / Tensor Cores 上的计算 | GPU util 高但吞吐不达预期、occupancy 低 |
| Register / Shared Memory | 每个 block/thread 的高速片上资源 | occupancy 降低、spill 到 local memory |
| L2 Cache | 跨 SM 缓存和内存访问缓冲 | cache hit 低、HBM 压力高 |
| HBM | GPU 主显存，存权重、activation、KV cache | OOM、memory bandwidth 饱和 |
| PCIe | CPU-GPU 或部分 GPU-GPU 连接 | host-device copy 慢、跨 NUMA 抖动 |
| NVLink / NVSwitch | GPU-GPU 高速互联 | TP/FSDP/NCCL 通信瓶颈 |
| NIC / IB / RoCE | 多机通信 | 跨节点 all-reduce、all-to-all 抖动 |
| CPU / DRAM | dataloader、tokenizer、调度器、网络栈 | dataloader wait、tokenizer 饱和、网关排队 |
| Storage | dataset、checkpoint、model weights | checkpoint stall、启动加载慢 |

## 训练中的硬件路径

```text
dataloader/storage -> CPU pinned memory -> GPU HBM
GPU SM/TensorCore compute forward/backward
GPU HBM <-> GPU HBM via NVLink/NVSwitch for intra-node collective
GPU <-> NIC <-> remote NIC <-> GPU for inter-node collective
checkpoint -> CPU/host -> local or remote storage
```

## 推理中的硬件路径

```text
request -> CPU tokenizer/router -> GPU prefill
KV cache allocated in HBM
iterative decode reads weights + KV cache repeatedly
streaming output -> CPU/network
```

## 重要直觉

- 训练通常在大矩阵乘上更接近 compute-bound，但分布式并行会引入通信和同步瓶颈。
- decode 阶段每步只生成少量 token，权重和 KV cache 反复读，常见 memory-bound。
- TP 很依赖 GPU-GPU 互联；EP/MoE 常依赖 all-to-all 和网络拓扑。
- checkpoint 和数据读取不是 GPU 问题，但可以把 GPU 饿住。

## 如何观测

- `nvidia-smi dmon` / DCGM：SM、memory、PCIe/NVLink、功耗。
- torch profiler：kernel timeline、CPU launch、NCCL。
- Nsight Systems：跨 CPU/GPU/NCCL 时间线。
- NCCL debug：通信拓扑、算法、超时。
- 平台 metric：队列长度、token throughput、GPU memory、network bytes、storage latency。

## 来源

- [[70-sources/official-docs/nccl-docs]]
- [[70-sources/official-docs/cuda-programming-guide-docs]]
- [[70-sources/official-docs/mlsys-book-docs]]

## 相关页面

- [[10-foundations/cuda-kernel-basics]]
- [[10-foundations/memory-and-roofline]]
- [[10-foundations/nccl-and-networking]]
- [[20-training-systems/training-performance-playbook]]
