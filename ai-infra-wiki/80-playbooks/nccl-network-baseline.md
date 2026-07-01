---
title: NCCL Network Baseline
type: playbook
topic: hardware
component: nccl
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [nccl, network, nccl-tests, topology]
source_refs: [70-sources/official-docs/nccl-docs, 70-sources/official-docs/pytorch-distributed-docs, 70-sources/official-docs/mlsys-book-docs]
---

# NCCL Network Baseline

## 目标

在调训练框架之前，先证明 GPU 拓扑和网络 baseline 是健康的。否则 NCCL timeout、all-reduce 慢、MoE all-to-all 慢会被误判成框架问题。

## 必收环境

```bash
nvidia-smi topo -m
nvidia-smi -L
ibstat || true
ip addr
```

记录：GPU 型号、GPU 数、NVLink/NVSwitch、NIC 型号、IB/RoCE、MTU、容器网络、rank 到 GPU/NIC 的映射。

## NCCL 环境变量

常用调试变量：

```bash
export NCCL_DEBUG=INFO
export NCCL_DEBUG_SUBSYS=INIT,COLL,GRAPH,NET
export TORCH_DISTRIBUTED_DEBUG=DETAIL
```

在多 NIC 机器上，显式指定接口比依赖自动选择更可控：

```bash
export NCCL_SOCKET_IFNAME=<interface>
```

IB/RoCE 还需要结合集群实际配置确认 GID、MTU、PFC/ECN、RDMA 权限和容器设备暴露。

## nccl-tests 基线

如果已安装 `nccl-tests`：

```bash
./build/all_reduce_perf -b 8M -e 4G -f 2 -g 8
./build/all_gather_perf -b 8M -e 4G -f 2 -g 8
./build/reduce_scatter_perf -b 8M -e 4G -f 2 -g 8
```

多机需要通过 MPI、Slurm 或集群 launcher 启动，并记录 rank placement。结果要区分：

- 节点内带宽。
- 跨节点带宽。
- p50/p95 波动。
- 是否有 error/retry/timeout。

## 诊断映射

| 现象 | 可能原因 |
|---|---|
| 单机快、多机慢 | NIC、IB/RoCE、路由、MTU、跨 rack |
| 小消息慢 | latency、算法选择、CPU launch overhead |
| 大消息慢 | 网络带宽、PCIe/NVLink、NUMA/NIC locality |
| 某 rank 慢 | rank placement、坏 GPU/NIC、进程负载 |

## 本地证据

- 暂无 `raw-sources/` 下的 `nvidia-smi topo -m`、`nccl-tests` 输出、跨节点带宽矩阵样本。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/hardware/nccl-baseline-<gpu>.md`，含 `nvidia-smi topo -m`、`nccl-tests` 输出、跨节点带宽矩阵。

## 尚未本地验证的边界

- “显式指定接口比依赖自动选择更可控”是经验结论，本页未引用本机对照。
- `nccl-tests` 参数是示例，真实基线需要根据 GPU 型号和互联调整。
- 诊断映射表是经验方向，需要真实 `NCCL_DEBUG=INFO` 日志确认。

## 来源

- [[70-sources/official-docs/nccl-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/mlsys-book-docs]]

## 相关页面

- [[10-foundations/nccl-and-networking]]
- [[80-playbooks/nccl-hang-triage]]
- [[80-playbooks/profiling-trace-playbook]]
