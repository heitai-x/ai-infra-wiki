---
title: Training Performance Playbook
type: playbook
topic: training
component: performance
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [training, performance, profiler, mfu]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# Training Performance Playbook

## 一句话

训练性能优化的第一步不是调参数，而是把 step time 拆成 compute、communication、data、checkpoint、scheduler/CPU overhead，并用证据证明瓶颈。

## Step time 拆解

```text
step_time = data_wait + forward + backward + communication_blocking + optimizer + checkpoint/logging + idle
```

实际 timeline 中 communication 可能与 backward overlap，因此要区分通信总时间和阻塞时间。

## 核心指标

- tokens/sec 或 samples/sec。
- step time p50/p95/p99。
- MFU：`model_FLOPs_per_step * steps_per_second / (num_gpus * peak_FLOPs_per_gpu)`。必须写清楚模型 FLOPs 假设、GPU 数量、precision 对应峰值和是否计入重算。
- GPU memory peak。
- NCCL time、bytes、overlap ratio。
- dataloader wait time。
- checkpoint write time。
- rank skew：最快和最慢 rank 差异。

## 诊断顺序

1. 是否 GPU 空转：看 profiler gap 和 dataloader wait。
2. 是否 kernel 低效：看小 kernel、GEMM shape、fusion。
3. 是否通信阻塞：看 NCCL 是否在 critical path。
4. 是否 pipeline bubble：看 stage timeline。
5. 是否 straggler：看 rank-wise step time。
6. 是否 checkpoint/IO stall：看周期性 spike。

## 常见优化手段

| 瓶颈 | 手段 | 风险 |
|---|---|---|
| Dataloader | 预处理、缓存、worker、pinned memory | 数据一致性、CPU 内存 |
| GEMM shape | batch/seq/micro-batch 调整 | 显存、收敛 |
| 小 kernel | fusion、compile、CUDA graph | 调试难度 |
| 通信 | bucket、overlap、拓扑、并行组 | 峰值显存、复杂性 |
| PP bubble | micro-batch、stage balance | activation 增加 |
| Checkpoint | async、sharded、频率调整 | 恢复点变远 |

## 证据模板

```text
hypothesis: step 慢在 NCCL 阻塞
hardware: 8xH100, NVSwitch, 2 nodes IB
model: ...
framework_commit: ...
command: ...
evidence:
  - torch profiler shows NCCL all-reduce on critical path
  - rank 3 step p95 20% slower
  - NCCL_DEBUG shows cross-node ring bandwidth lower than expected
next_action:
  - adjust process group placement / bucket size / overlap
```

## 本地证据

- 暂无 `raw-sources/` 下的本地 trace、step time 或 MFU 复现样本。
- 章节中给出的 MFU、step time 拆分、overlap 结论仍属于“官方文档 + 关键论文”支持的学习型结论，尚未用本机 / 集群数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/<framework>-<hw>-<commit>.md`，含命令、profile 输出、step time / MFU 与排队 / 通信比例。

## 尚未本地验证的边界

- 公式 `step_time = data_wait + forward + backward + communication_blocking + optimizer + checkpoint/logging + idle` 是结构化拆解模型，不等于具体实现的真实耗时比例。
- MFU 公式对 activation checkpoint / MoE 激活 / vocab head / pipeline bubble 的折算依赖不同假设，未经过本机对照。
- “NCCL overlap ratio” 与 “rank skew” 需要本地 `torch.profiler` + Nsight Systems 真实数据，本页尚未引用任何本地 raw artifact。

## 来源

- [[70-sources/official-docs/pytorch-profiler-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/nccl-docs]]
- [[70-sources/official-docs/mlsys-book-docs]]
- [[70-sources/key-papers/zero-paper]]

## 相关页面

- [[10-foundations/nccl-and-networking]]
- [[80-playbooks/nccl-hang-triage]]
- [[80-playbooks/profiling-trace-playbook]]
- [[90-experiments/single-node-training]]
