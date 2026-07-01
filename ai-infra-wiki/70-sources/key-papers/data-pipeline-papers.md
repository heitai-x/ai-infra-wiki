---
title: Data Pipeline And Fault Tolerance Papers
type: source
source_type: paper
source_url: https://arxiv.org/abs/2104.04473
topic: training
component: data-pipeline
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [paper, data-pipeline, fault-tolerance, checkpoint, dataloader]
---

# Data Pipeline And Fault Tolerance Papers

## Why It Matters

这一组论文覆盖 dataloader 瓶颈、checkpoint 频率、straggler、straggler-aware scheduling 和重启策略，是 `20-training-systems/data-pipeline-fault-tolerance` 引用密度最高的一手文献来源。

## Key Claims

- 论文提出 data loading、preprocessing、shuffle 和 tokenization 的开销分析。
- 论文给出 checkpoint frequency、checkpoint size 与 restart cost 的折衷。
- 论文讨论 straggler detection、elastic worker 和 graceful restart 的工程路径。
- 论文为 fault-tolerance 设计提供公式和实证 baseline。

## Limits Or Caveats

- 论文结论与今天的大模型训练栈、object store、parallel strategy 可能有偏差。
- 论文不直接回答 GPU/host memory、磁盘吞吐和容器限制下的具体数字。
- 引用时应明确哪个结论来自哪篇论文的哪一节。

## Links To Concepts

- [[20-training-systems/data-pipeline-fault-tolerance]]
- [[20-training-systems/activation-optimizer-checkpoint]]
- [[80-playbooks/nccl-hang-triage]]
- [[80-playbooks/training-performance-playbook]]

## Follow Up

- 后续按论文分别建独立 source card，便于精确引用。
- 后续补 raw 论文 PDF 摘要或导出到 `raw-sources/`。
