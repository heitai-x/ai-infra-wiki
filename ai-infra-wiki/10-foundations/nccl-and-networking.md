---
title: NCCL And Networking
type: concept
topic: hardware
component: nccl
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [nccl, networking, collectives, distributed]
source_refs: [70-sources/official-docs/nccl-docs, 70-sources/official-docs/pytorch-distributed-docs]
---

# NCCL And Networking

## 一句话

NCCL 提供 GPU 间 collective communication。分布式训练的很多“慢”和“挂”本质是 collective 大小、拓扑、算法、网络、同步顺序或 rank 状态不一致的问题。

## 常见 collective

| Collective | 语义 | 训练/推理场景 |
|---|---|---|
| AllReduce | 所有 rank 求和并拿到完整结果 | DDP 梯度同步 |
| ReduceScatter | 求和后按 rank 切分结果 | ZeRO/FSDP 梯度 shard |
| AllGather | 每个 rank 收集所有 shard | FSDP 参数重建、TP 输出拼接 |
| Broadcast | 一个 rank 发送给所有 rank | 初始化参数、控制信息 |
| AllToAll | 每个 rank 给每个 rank 发送不同切片 | MoE expert dispatch、某些 sequence parallel |

## 拓扑层次

```text
GPU same NVLink island
  -> same node via NVSwitch/PCIe
  -> same rack via IB/RoCE
  -> cross rack network
```

一般越跨层，延迟越高，带宽越低，抖动越大。TP 和 FSDP 的最佳并行组通常应尽量贴近高速拓扑。

## NCCL hang 常见原因

- 某些 rank 没有进入同一个 collective。
- collective 顺序不一致。
- 某个 rank OOM、异常退出或被 dataloader 卡住。
- 网络接口选择错误。
- IB/RoCE 配置、MTU、GID、NCCL env 不匹配。
- 拓扑变化或容器设备可见性不一致。

## 观测工具

- `NCCL_DEBUG=INFO`：输出通信初始化和错误信息。
- `NCCL_DEBUG_SUBSYS=INIT,COLL,GRAPH,NET`：定位初始化、collective、拓扑、网络。
- `torch.distributed` 日志：rank 状态、barrier、timeout。
- `nvidia-smi topo -m`：节点内拓扑。
- NIC counters / DCGM / Prometheus：网络错误、吞吐、重传。

## 学习重点

不要只记 all-reduce 名字，而要能回答：

1. 每个 rank 输入输出 tensor shape 是什么？
2. bytes 大小是多少？
3. 发生在 forward、backward、optimizer 还是 serving scheduler？
4. 是否能和 compute overlap？
5. 并行组和硬件拓扑是否匹配？

## 来源

- [[70-sources/official-docs/nccl-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]

## 相关页面

- [[80-playbooks/nccl-hang-triage]]
- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/expert-parallel-moe]]
