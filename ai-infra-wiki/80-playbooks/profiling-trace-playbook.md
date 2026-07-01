---
title: Profiling Trace Playbook
type: playbook
topic: ops
component: profiling
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [profiling, torch-profiler, nsight-systems, nsight-compute]
source_refs: [70-sources/official-docs/pytorch-profiler-docs, 70-sources/official-docs/pytorch-distributed-docs, 70-sources/official-docs/mlsys-book-docs]
---

# Profiling Trace Playbook

## 目标

把“慢”拆成证据：CPU gap、GPU kernel、NCCL、memory bandwidth、dataloader、checkpoint、scheduler queue。没有 trace 的性能结论只能算假设。

## 工具分层

| 工具 | 适合回答的问题 | 输出 |
|---|---|---|
| torch profiler | PyTorch op、CUDA kernel、NCCL 是否在 critical path | Chrome trace / table |
| Nsight Systems | CPU/GPU/NCCL/OS runtime 的全局时间线 | `.nsys-rep` |
| Nsight Compute | 单 kernel 的 occupancy、memory、tensor core 指标 | kernel report |
| DCGM / nvidia-smi | 长时间 GPU health 和利用率 | metrics |

## Torch profiler 最小流程

1. 先跑 smoke test，确认 workload 稳定。
2. 跳过 warmup，profile 3-5 个 step。
3. 打开 trace，看 CPU launch gap、kernel 排布、NCCL overlap。
4. 导出 raw trace 到 `artifacts/`。
5. 把结论写回 experiment note。

## Nsight Systems 最小流程

```bash
nsys profile -o artifacts/nsys_report   --trace=cuda,nvtx,osrt,cudnn,cublas   <training-or-serving-command>
```

检查顺序：

- GPU 是否有大段空白。
- NCCL kernel 是否阻塞 compute。
- CPU 线程是否在 dataloader、tokenizer、network 或 logging 上卡住。
- 多 rank 时间线是否有 straggler。

## Nsight Compute 使用边界

Nsight Compute 适合单 kernel 深挖，不适合一开始就全量 profile。先用 Systems 找到可疑 kernel，再用 Compute 看：

- achieved occupancy。
- memory throughput。
- tensor core utilization。
- shared memory bank conflict。
- register spill。

## 结论模板

```text
hypothesis:
trace_artifact:
critical_path:
  cpu_gap:
  gpu_kernel:
  nccl:
  io:
evidence:
fix:
after_metric:
```

## 本地证据

- 暂无 `raw-sources/` 下的 torch profiler Chrome trace、Nsight Systems `.nsys-rep`、Nsight Compute kernel report 样本。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/traces/profiling-<framework>-<commit>.md`，含 torch profiler trace、Nsight Systems 报告、critical path 分析。

## 尚未本地验证的边界

- “先跑 smoke test 确认 workload 稳定”是方法论建议，本页未引用具体 smoke test 输出。
- “Nsight Compute 适合单 kernel 深挖”是经验建议，真实场景需要根据 workload 调整。
- 结论模板中的 `critical_path` 字段需要真实 trace 才能填写。

## 来源

- [[70-sources/official-docs/pytorch-profiler-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/mlsys-book-docs]]

## 相关页面

- [[20-training-systems/training-performance-playbook]]
- [[90-experiments/torchrun-ddp-fsdp-minimal]]
- [[80-playbooks/nccl-network-baseline]]
