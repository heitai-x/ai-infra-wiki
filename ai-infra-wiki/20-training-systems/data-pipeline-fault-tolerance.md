---
title: Data Pipeline Fault Tolerance
type: concept
topic: training
component: data-and-reliability
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [dataloader, checkpoint, fault-tolerance, reliability]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# Data Pipeline Fault Tolerance

## 一句话

训练系统不只是在 GPU 上算。数据读取、shuffle、一致性、checkpoint、恢复和容错决定了大规模训练能不能持续跑。

## 数据路径

```text
raw dataset -> preprocessing/tokenization -> shard/index
  -> dataloader workers -> CPU pinned memory
  -> GPU batch -> training step
```

## 常见瓶颈

- tokenizer 或 preprocessing 在 CPU 上饱和。
- dataloader worker 数不足或锁竞争。
- remote storage 抖动。
- shuffle buffer 太小导致数据质量问题。
- batch collation 产生大量 Python overhead。
- 多机 worker 数据切分重复或遗漏。

## 容错状态

恢复训练需要保存：

- model/optimizer/scheduler。
- global step、consumed samples、epoch。
- RNG state。
- dataset shard 和 dataloader offset。
- parallelism config。
- loss scale / mixed precision state。

只保存模型权重不能恢复“同一条训练轨迹”。

## 故障类型

| 类型 | 现象 | 处理 |
|---|---|---|
| Worker crash | 某 rank 退出，NCCL timeout | 自动重启或 fail-fast |
| Data stall | GPU 空转，dataloader wait 高 | profile CPU/data path |
| Checkpoint stall | 周期性 step time spike | async checkpoint、分片写入 |
| Bad sample | loss nan 或 tokenizer 异常 | 数据校验和 quarantine |
| Preemption | 节点被回收 | frequent checkpoint + elastic restore |

## 本地证据

- 暂无 `raw-sources/` 下的 dataloader wait 比例、checkpoint 写入 / 恢复耗时、bad sample 复现样本。
- 章节中数据路径、容错状态、故障类型表属于对 PyTorch Distributed 文档 + 数据 pipeline 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/data-pipeline-<commit>.md`，含 dataloader wait profile、一次 checkpoint 写入耗时、一次 resume 后 step 连续性验证。

## 尚未本地验证的边界

- “只保存模型权重不能恢复同一条训练轨迹” 是正确性结论，但具体到不同 framework / runtime 的差异，本页未引用源码或实验。
- 不同 fault 类型（worker crash / data stall / checkpoint stall / bad sample / preemption）的诊断命令与预期耗时依赖集群与 runtime，本页未给出本机数字。
- “frequent checkpoint + elastic restore” 平衡点是策略问题，需要用 SLO / cost 视角评估，本页未引用本机数字。

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/pytorch-profiler-docs]]
- [[70-sources/key-papers/data-pipeline-papers]]

## 相关页面

- [[20-training-systems/training-performance-playbook]]
- [[20-training-systems/activation-optimizer-checkpoint]]
- [[80-playbooks/nccl-hang-triage]]
