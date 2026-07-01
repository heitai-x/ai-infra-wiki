---
title: Benchmark Design
type: playbook
topic: ops
component: benchmark
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [benchmark, serving, training, methodology]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/official-docs/mlsys-book-docs, 70-sources/key-papers/pagedattention-paper, 70-sources/key-papers/distserve-paper]
---

# Benchmark Design

## 目标

设计可复现、公平、能回答问题的 AI Infra benchmark。benchmark 不是跑一个数字，而是控制变量、记录证据、解释边界。

## 必填字段

- Hardware：GPU 型号、数量、互联、CPU、内存、网络。
- Software：driver、CUDA、NCCL、framework commit、container。
- Model：模型名、参数、precision、quantization、max context。
- Workload：prompt/output 分布、batch/concurrency、dataset。
- Command：server 启动命令和 client benchmark 命令。
- Metrics：吞吐、延迟、显存、GPU util、错误率。
- Raw artifacts：logs、profiles、CSV/JSON 输出。

## Serving benchmark 公平性

- 相同模型权重和 tokenizer。
- 相同 precision/quantization，或明确说明差异。
- 相同 prompt/output 分布。
- 预热后测量。
- 分别报告 TTFT、TPOT、throughput、错误率。
- 报告 SLO 下的最大 goodput，而不是只报告无限压测吞吐。
- 记录所有 runtime 参数。

## Training benchmark 公平性

- 相同 global batch、seq len、precision、optimizer。
- 明确 gradient accumulation。
- 明确 activation checkpoint 和 sharding strategy。
- 排除或单独报告 checkpoint 时间。
- 报告 step time 分布而不是单个最好值。
- 报告 MFU 公式和模型 FLOPs 假设。

## 反模式

- 只报告最高 tokens/sec，不报告延迟。
- 框架之间使用不同 precision。
- 不记录 commit 和命令。
- 把 warmup 阶段混进结果。
- 用平均 prompt length 掩盖长尾。
- 没有错误率和拒绝率。

## 本地证据

- 暂无 `raw-sources/` 下专门针对 benchmark methodology 的对照样本。
- 章节中 serving / training benchmark 公平性、反模式属于对 vLLM / SGLang 文档 + PagedAttention / DistServe 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/benchmarks/benchmark-design-<date>.md`，含一次公平性对照实验的命令、输出和结论。

## 尚未本地验证的边界

- “报告 SLO 下的最大 goodput”是方法论建议，本页未引用具体 goodput 数字。
- “报告 step time 分布而不是单个最好值”是方法论建议，本页未引用本机 step time 分布。
- 反模式清单是经验总结，不等于所有场景都适用。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/mlsys-book-docs]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/distserve-paper]]

## 相关页面

- [[90-experiments/llm-serving-benchmark]]
- [[90-experiments/vllm-sglang-benchmark-harness]]
- [[90-experiments/single-node-training]]
- [[00-index/skill-index]]
