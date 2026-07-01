---
title: Torchrun DDP FSDP Minimal Experiment
type: experiment
topic: training
component: ddp-fsdp
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [torchrun, ddp, fsdp, experiment, profiler]
source_refs: [70-sources/official-docs/pytorch-distributed-docs, 70-sources/official-docs/pytorch-profiler-docs, 70-sources/key-papers/zero-paper]
---

# Torchrun DDP FSDP Minimal Experiment

## 目标

把 [[20-training-systems/ddp-fsdp-zero]] 从概念变成可复现实验：同一 Tiny Transformer，在 DDP 与 FSDP 下比较 step time、显存峰值和通信行为。

## 脚本

- 本地脚本：`scripts/experiments/torchrun_ddp_fsdp_minimal.py`
- 输出 artifact：`artifacts/torchrun_ddp_fsdp_metrics.jsonl`

## 命令

单进程 smoke test：

```bash
python3 scripts/experiments/torchrun_ddp_fsdp_minimal.py --strategy single --steps 2 --warmup 1
```

单机 2 卡 DDP：

```bash
torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py   --strategy ddp --steps 20 --warmup 5 --batch-size 4 --seq-len 128
```

单机 2 卡 FSDP：

```bash
torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py   --strategy fsdp --steps 20 --warmup 5 --batch-size 4 --seq-len 128
```

FSDP + activation checkpoint：

```bash
torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py   --strategy fsdp --activation-checkpoint --steps 20 --warmup 5 --batch-size 4 --seq-len 128
```

## 必收指标

- `avg_step_time_ms`
- `max_memory_allocated_mb`
- `max_memory_reserved_mb`
- loss 是否正常下降或至少无 NaN
- world size、strategy、batch、seq len、hidden、layers、precision

## Profiler 扩展

先跑脚本确认配置，再用 [[80-playbooks/profiling-trace-playbook]] 加 torch profiler 或 Nsight Systems：

```bash
nsys profile -o artifacts/nsys_ddp_report   torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py --strategy ddp
```

## 验收问题

1. DDP 和 FSDP 的显存峰值差异是否符合 [[20-training-systems/ddp-fsdp-zero]] 的状态账本？
2. FSDP 是否引入更多 all-gather / reduce-scatter？
3. activation checkpoint 是否降低显存，并增加 step time？
4. profiler 中通信是否在 backward critical path 上？

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/pytorch-profiler-docs]]
- [[70-sources/key-papers/zero-paper]]

## 相关页面

- [[90-experiments/single-node-training]]
- [[20-training-systems/training-performance-playbook]]
- [[80-playbooks/fsdp-zero-oom-triage]]
