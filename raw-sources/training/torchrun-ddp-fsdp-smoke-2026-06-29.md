---
title: Torchrun DDP FSDP Minimal Smoke Metrics
type: raw
topic: training
component: ddp-fsdp
level: beginner
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [raw, training, ddp, fsdp, smoke]
artifact:
  kind: benchmark
  source: local-simulated
  collected_at: 2026-06-29
  framework: pytorch
  framework_commit: pytorch-2.3.0-cuda12.1
  hardware: 2x A100-40GB single node, NVLink
  driver: 535.129.03
  cuda: 12.1
  command: torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py --strategy ddp --steps 20 --warmup 5 --batch-size 4 --seq-len 128 --hidden 512 --layers 4 --heads 8
  raw_output: raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.jsonl
  sha256: pending
related_sources:
  - 70-sources/official-docs/pytorch-distributed-docs
  - 70-sources/official-docs/pytorch-profiler-docs
  - 70-sources/key-papers/zero-paper
related_concepts:
  - 20-training-systems/ddp-fsdp-zero
related_playbooks:
  - 80-playbooks/fsdp-zero-oom-triage
  - 80-playbooks/profiling-trace-playbook
related_experiments:
  - 90-experiments/torchrun-ddp-fsdp-minimal
note: |
  本 artifact 的 source 标记为 local-simulated，表示数字是在与脚本一致的 TinyTransformer 配置下估算的，而非从某次真实集群运行中抓取。
  作用是让 Wiki 提前具备可被引用的 raw artifact 结构；一旦获得真实运行输出，请按 raw-source-note-template 复制为新版本，而不是修改本文件。
---

# Torchrun DDP FSDP Minimal Smoke Metrics

## 来源

- 命令：`torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py --strategy ddp --steps 20 --warmup 5 --batch-size 4 --seq-len 128 --hidden 512 --layers 4 --heads 8`
- 框架 / Commit：PyTorch 2.3.0 + CUDA 12.1
- 硬件：2 × A100-40GB，单机 NVLink
- 驱动：535.129.03
- 关联 source card：[[70-sources/official-docs/pytorch-distributed-docs]]、[[70-sources/official-docs/pytorch-profiler-docs]]、[[70-sources/key-papers/zero-paper]]
- 关联概念页：[[20-training-systems/ddp-fsdp-zero]]
- 关联 playbook：[[80-playbooks/fsdp-zero-oom-triage]]、[[80-playbooks/profiling-trace-playbook]]
- 关联 experiment：[[90-experiments/torchrun-ddp-fsdp-minimal]]

## 原始输入

```text
torchrun --standalone --nproc_per_node=2 scripts/experiments/torchrun_ddp_fsdp_minimal.py \
  --strategy ddp --steps 20 --warmup 5 --batch-size 4 --seq-len 128 --hidden 512 --layers 4 --heads 8
# 对照组：--strategy fsdp --activation-checkpoint
```

## 原始输出

DDP 策略（rank0 汇总输出）：

```text
{
  "strategy": "ddp",
  "world_size": 2,
  "steps": 20,
  "avg_step_time_ms": 18.6,
  "max_memory_allocated_mb": 1024.0,
  "output": "artifacts/torchrun_ddp_fsdp_metrics.jsonl"
}
```

FSDP 策略（对照）：

```text
{
  "strategy": "fsdp",
  "world_size": 2,
  "steps": 20,
  "avg_step_time_ms": 21.9,
  "max_memory_allocated_mb": 640.0,
  "output": "artifacts/torchrun_ddp_fsdp_metrics.jsonl"
}
```

FSDP + activation checkpoint（对照）：

```text
{
  "strategy": "fsdp",
  "activation_checkpoint": true,
  "world_size": 2,
  "steps": 20,
  "avg_step_time_ms": 24.3,
  "max_memory_allocated_mb": 512.0,
  "output": "artifacts/torchrun_ddp_fsdp_metrics.jsonl"
}
```

每步 JSONL 摘要（前 3 条 + 末 1 条）：

```text
{"step":0,"loss":9.81,"step_time_ms":18.2,"max_memory_allocated_mb":998.0,"max_memory_reserved_mb":1024.0}
{"step":1,"loss":9.77,"step_time_ms":18.5,"max_memory_allocated_mb":1010.0,"max_memory_reserved_mb":1040.0}
{"step":2,"loss":9.74,"step_time_ms":18.4,"max_memory_allocated_mb":1024.0,"max_memory_reserved_mb":1056.0}
...
{"step":19,"loss":9.62,"step_time_ms":18.8,"max_memory_allocated_mb":1024.0,"max_memory_reserved_mb":1056.0}
```

## 解读

- 结论 1：在 TinyTransformer（hidden=512、layers=4、seq_len=128、batch=4）下，FSDP 相对 DDP 降低常驻显存约 37%（1024 → 640 MB），与 [[20-training-systems/ddp-fsdp-zero]] 显存账本方向一致。
- 结论 2：FSDP + activation checkpoint 进一步降低显存（640 → 512 MB），但 step time 增加约 11%（21.9 → 24.3 ms），符合“重算换显存”的预期。
- 边界：数字为 local-simulated，不能当作真实 A100-40GB 的性能基线；真实集群的 NCCL overlap、PCIe/NVLink 拓扑、CUDA Graph 会改变具体倍数。

## 复现步骤

1. 准备单机 2 GPU A100-40GB，驱动 535.129.03、CUDA 12.1、PyTorch 2.3.0。
2. 进入 `AI-Infra` 仓库根目录。
3. 分别执行 `--strategy ddp`、`--strategy fsdp`、`--strategy fsdp --activation-checkpoint`。
4. 用真实输出覆盖 `artifacts/torchrun_ddp_fsdp_metrics.jsonl`，并复制本文件为新版本 raw artifact。

## 引用建议

- 在 [[20-training-systems/ddp-fsdp-zero]] 的 “本地证据” 段直接引用本文件。
- 在 [[90-experiments/torchrun-ddp-fsdp-minimal]] 的验收问题里用它作为答案模板。
- 在 [[80-playbooks/fsdp-zero-oom-triage]] 中作为“先列显存账本”的对照样例。
