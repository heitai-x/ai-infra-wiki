---
title: Batching Scheduling
type: concept
topic: inference
component: scheduler
level: intermediate
status: active
last_updated: 2026-06-29
owner: local
reliability: medium
tags: [batching, scheduling, continuous-batching, serving]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/key-papers/pagedattention-paper, 70-sources/key-papers/distserve-paper]
---

# Batching Scheduling

## 一句话

LLM serving scheduler 的任务是在 GPU 不空转、KV cache 不爆、SLO 不失控之间平衡。Continuous batching 允许请求在 decode 过程中动态加入和退出，大幅提高吞吐。

## 静态 batching 的问题

传统 batch 需要等一批请求一起完成。LLM 输出长度差异大，短请求会等长请求，GPU 也会因为 batch 生命周期固定而浪费。

## Continuous batching

```text
iteration 1: req A B C
iteration 2: req A B C D joins
iteration 3: req B finishes, A C D continue
iteration 4: req E joins
```

每个 decode iteration 重新组织 active sequences。这样可以持续填满 GPU，但 scheduler 需要处理 KV 分配、优先级、公平性和抢占。

## Admission control

新请求能否进入系统取决于：

- 当前队列长度。
- 可用 KV cache blocks。
- max batch tokens / max num seqs。
- prompt length 和预估 output length。
- 请求优先级和租户 quota。
- SLO budget。

## 调度目标

| 目标 | 策略 | 风险 |
|---|---|---|
| 最大吞吐 | 大 batch、高 occupancy | TTFT 增大 |
| 低延迟 | 小 batch、优先短请求 | GPU 利用率低 |
| 公平性 | tenant quota、aging | 吞吐下降 |
| 成本 | 高并发、高利用率 | 尾延迟和拒绝率上升 |

## 关键指标

- Queue time。
- TTFT / TPOT / ITL。
- Batch tokens per iteration。
- Running / waiting / swapped sequences。
- KV cache free blocks。
- Preemptions。
- Rejection rate。

## 本地证据

- 暂无 `raw-sources/` 下的调度策略对比、batch tokens / 排队时间 JSONL 样本。
- 章节中 continuous batching、admission control、调度目标表属于对 vLLM / SGLang 文档 + PagedAttention / DistServe 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/inference/<runtime>-sched-<commit>.md`，含 batch tokens / iteration、TTFT / TPOT、rejection / preemption 计数。

## 尚未本地验证的边界

- “最大吞吐 / 低延迟 / 公平性 / 成本”四个目标之间的具体权衡曲线依赖 workload 与 SLO，本页未引用任何本地 SLO 曲线。
- admission control 各项阈值是工程经验值，不等于任何 runtime 的默认值。
- preempt / swap 策略对最终用户感知的影响（如 SLO 失败率、用户重试成本）尚未本地复现。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/distserve-paper]]

## 相关页面

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[40-serving-platform/observability-slo-cost]]
