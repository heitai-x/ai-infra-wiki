---
title: Hardware Platform Entities
type: entity
source_type: curated
entity_type: hardware-platform

topic: hardware
component: platform
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [entities, gpu, nccl, kubernetes, network]
---

# Hardware Platform Entities

## NVIDIA GPU

- Role: 训练和推理的主要计算设备。
- Main concepts: SM、Tensor Core、HBM、L2、NVLink、MIG。
- Learning focus: 算力、带宽、显存容量、拓扑对系统行为的影响。
- Links: [[10-foundations/gpu-system-map]], [[10-foundations/memory-and-roofline]]。

## NCCL

- Role: NVIDIA GPU collective communication library。
- Main concepts: all-reduce、all-gather、reduce-scatter、broadcast、all-to-all。
- Learning focus: 分布式训练通信和 hang/timeout 排查。
- Links: [[10-foundations/nccl-and-networking]], [[80-playbooks/nccl-hang-triage]]。

## NVLink / NVSwitch

- Role: 节点内 GPU 高速互联。
- Main concepts: TP/FSDP intra-node 通信、拓扑亲和、带宽层次。
- Learning focus: 为什么高频通信并行组应优先贴近高速拓扑。
- Links: [[10-foundations/gpu-system-map]], [[20-training-systems/tensor-pipeline-context-parallel]]。

## InfiniBand / RoCE

- Role: 多节点 GPU 集群网络。
- Main concepts: RDMA、NIC locality、GID/MTU/interface、跨节点 collective。
- Learning focus: 多机训练和 PD 分离 serving 的网络瓶颈。
- Links: [[10-foundations/nccl-and-networking]], [[30-inference-systems/disaggregated-and-moe-serving]]。

## Kubernetes GPU Stack

- Role: 生产集群中的 GPU 资源抽象、调度和隔离。
- Main concepts: device plugin、operator、node labels、MIG、topology-aware scheduling。
- Learning focus: 把模型 runtime 变成可调度、可扩缩、可观测的服务。
- Links: [[40-serving-platform/gpu-scheduling-kubernetes]], [[40-serving-platform/serving-platform-map]]。
