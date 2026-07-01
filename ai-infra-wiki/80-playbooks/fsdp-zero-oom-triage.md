---
title: FSDP ZeRO OOM Triage
type: playbook
topic: training
component: memory
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [fsdp, zero, oom, memory]
source_refs: [70-sources/official-docs/pytorch-distributed-docs, 70-sources/official-docs/deepspeed-docs, 70-sources/key-papers/zero-paper]
---

# FSDP ZeRO OOM Triage

## 目标

定位 FSDP/ZeRO 训练 OOM 的来源：常驻状态、activation、all-gather 工作集、optimizer、临时 buffer、fragmentation 或 checkpoint。

## 先列显存账本

```text
params/shards
+ gradients/shards
+ optimizer_states/shards
+ all_gathered_params_working_set
+ activations
+ temporary_buffers
+ CUDA context / allocator fragmentation
+ checkpoint / logging buffers
```

## 必收证据

- 模型参数量、层数、hidden、heads、seq len、micro/global batch。
- dtype、optimizer、activation checkpoint 配置。
- FSDP wrap policy 或 ZeRO stage。
- GPU memory peak 时间点。
- OOM stack trace。
- 是否发生在 forward、backward、optimizer step、checkpoint。
- framework version/commit。

## 诊断表

| OOM 位置 | 常见原因 | 处理 |
|---|---|---|
| forward 某层前 | all-gather 参数峰值 | 调整 wrap 粒度、prefetch、reshard |
| backward | activation + grad + comm buffer | activation checkpoint、减 micro-batch |
| optimizer step | optimizer state 或 master params | ZeRO-1/2/3、offload、8-bit optimizer |
| checkpoint | gather full state 或 IO buffer | sharded checkpoint、streaming save |
| 启动阶段 | 权重加载复制 | meta init、load sharded weights |

## 修复顺序

1. 减小 micro-batch 或 seq len，确认是否 activation 主导。
2. 开 activation checkpoint，比较峰值和 step time。
3. 调整 FSDP wrap granularity。
4. 检查 prefetch 是否造成峰值。
5. 使用 ZeRO/FSDP 更高 sharding stage。
6. 检查 checkpoint 是否 gather full state。
7. 记录吞吐损失，避免只看能否跑通。

## 本地证据

- 暂无 `raw-sources/` 下专门针对 OOM triage 的 stack trace、显存峰值时间点、修复前后对照样本。
- 章节中显存账本、诊断表、修复顺序属于对 PyTorch Distributed / DeepSpeed 文档 + ZeRO 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/oom-triage-<commit>.md`，含 OOM stack trace、显存峰值时间点、修复前后 step time 与显存对照。

## 尚未本地验证的边界

- 诊断表中“forward 某层前 OOM = all-gather 参数峰值”是经验映射，不等于所有 OOM 都符合。
- “调整 wrap 粒度”的具体效果依赖模型和硬件，本页未引用本机数字。
- “记录吞吐损失，避免只看能否跑通”是方法论建议，本页未引用具体吞吐损失数字。

## 来源

- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/deepspeed-docs]]
- [[70-sources/key-papers/zero-paper]]

## 相关页面

- [[20-training-systems/ddp-fsdp-zero]]
- [[20-training-systems/activation-optimizer-checkpoint]]
- [[10-foundations/memory-and-roofline]]
