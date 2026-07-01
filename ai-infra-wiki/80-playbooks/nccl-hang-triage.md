---
title: NCCL Hang Triage
type: playbook
topic: training
component: nccl
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [nccl, hang, distributed, triage]
source_refs: [70-sources/official-docs/nccl-docs, 70-sources/official-docs/pytorch-distributed-docs, 70-sources/key-papers/data-pipeline-papers]
---

# NCCL Hang Triage

## 目标

定位多卡/多机训练中 NCCL hang、timeout、collective 卡住的问题，并区分通信问题、rank 崩溃、代码分支不一致、数据阻塞和拓扑配置错误。

## 快速判断

1. 是否所有 rank 都还活着。
2. 是否某个 rank 已 OOM 或 Python exception。
3. 是否所有 rank 进入了同一个 collective。
4. 是否 collective 顺序一致。
5. 是否只有跨节点慢/挂。
6. 是否 dataloader 或 checkpoint 让部分 rank 没到 barrier。

## 必收证据

```bash
NCCL_DEBUG=INFO
NCCL_DEBUG_SUBSYS=INIT,COLL,GRAPH,NET
TORCH_DISTRIBUTED_DEBUG=DETAIL
```

还需要：

- 每个 rank 的完整日志。
- GPU topo：`nvidia-smi topo -m`。
- 节点、rank、GPU 映射。
- 网络接口、IB/RoCE 配置。
- 训练命令和环境变量。
- 最近一次 OOM、SIGKILL、dataloader error。

## 排查路径

| 现象 | 假设 | 下一步 |
|---|---|---|
| 某 rank 无日志继续 | rank crash 或 OOM | 查 dmesg/container exit/GPU OOM |
| 所有 rank 停在 barrier | 前面某 rank 未到 | 对齐代码路径和 dataloader |
| 只跨节点慢 | 网络或接口 | 检查 NCCL_SOCKET_IFNAME、IB、MTU、GID |
| 初始化阶段挂 | 拓扑/地址/端口 | 检查 master addr、端口、防火墙 |
| all-to-all 慢 | MoE imbalance 或网络 | 看 expert token count 和 bytes |

## 修复方向

- 先修 rank crash，再修 NCCL。
- 固定 rank/GPU 映射。
- 明确网络接口。
- 缩小复现：2 GPU -> 1 node -> 2 nodes。
- 用 `nccl-tests` 区分框架问题和网络问题。
- 避免不同 rank 条件分支进入不同 collective。

## 本地证据

- 暂无 `raw-sources/` 下的 NCCL hang 复现日志、`NCCL_DEBUG=INFO` 输出、rank crash stack trace 样本。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/nccl-hang-<commit>.md`，含 `NCCL_DEBUG=INFO` 日志、rank/GPU 映射、修复前后对照。

## 尚未本地验证的边界

- “先修 rank crash，再修 NCCL”是经验顺序，不等于所有 hang 都由 rank crash 导致。
- “缩小复现：2 GPU -> 1 node -> 2 nodes”是方法论建议，真实复现可能需要更多变量控制。
- 排查路径表是经验映射，需要真实日志确认。

## 来源

- [[70-sources/official-docs/nccl-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/key-papers/data-pipeline-papers]]

## 相关页面

- [[10-foundations/nccl-and-networking]]
- [[20-training-systems/training-performance-playbook]]
