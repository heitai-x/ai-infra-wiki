---
title: PyTorch Profiler Docs
type: source
source_type: official_doc
source_url: https://pytorch.org/docs/stable/profiler.html
topic: ops
component: profiling
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [pytorch, profiler, trace, kineto, torch-profiler]
---

# PyTorch Profiler Docs

## Why It Matters

PyTorch Profiler 是 `80-playbooks/profiling-trace-playbook` 推荐的“先把 PyTorch op 拆开”工具，官方文档定义了 trace 字段、CUDA kernel 表、memory view 和 NVTX 标注方式，是 profiling-trace 的最权威依据。

## Key Claims

- 文档定义了 `torch.profiler` schedule、on_trace_ready、with_stack 和 experimental_config 等核心接口。
- 文档解释了 Chrome trace、kineto 输出与 TensorBoard plugin 的对应关系。
- 文档明确说明 memory view、kernel 表和 distributed collective 在 trace 中的位置。
- 文档给出与 Nsight Systems、CUDA event 的搭配方式与边界。

## Limits Or Caveats

- Profiler 自带 overhead，trace 结论必须和未 profile 状态做对比。
- 文档对部分 advanced 字段的解释较简略，需要结合源码或 release notes。
- 跨进程、跨 step 的对齐依赖显式 NVTX 或 `record_function`。

## Links To Concepts

- [[80-playbooks/profiling-trace-playbook]]
- [[90-experiments/torchrun-ddp-fsdp-minimal]]
- [[20-training-systems/training-performance-playbook]]

## Follow Up

- 后续补一个最小 profiler 脚本和 trace 截图到 `raw-sources/`。
- 后续补 NVTX 推荐命名约定的速查表。
