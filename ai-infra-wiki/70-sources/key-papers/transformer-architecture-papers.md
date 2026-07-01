---
title: Transformer Architecture Papers
type: source
source_type: paper
source_url: https://arxiv.org/abs/1706.03762
topic: hardware
component: model-cost
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [paper, transformer, attention, gqa, mqa, moe]
---

# Transformer Architecture Papers

## Why It Matters

`10-foundations/model-architecture-cost-formulas` 的所有公式都来自 Transformer 原文及其后续对 GQA/MQA、MoE、KV cache 优化的工作；这是把“参数量/FLOPs/KV cache”映射到具体 AI Infra 决策的源头文献。

## Key Claims

- Transformer 原文给出 encoder/decoder、自注意力和 scaled dot-product attention 的标准形式。
- FlashAttention 论文给出 IO-aware attention 复杂度分析，解释 attention 在长上下文下的带宽与显存压力。
- GQA / MQA 工作解释了 KV 头共享对显存和 inference 吞吐的提升。
- MoE 原始工作（GShard / Switch Transformer）解释 expert routing 和容量设计。
- 后续 analysis 论文给出 6N dense 训练 FLOPs 公式的来源和误差。

## Limits Or Caveats

- 公式和今天的 runtime 实际数字可能不同；具体显存还要看 dtype、activation checkpoint、并行策略。
- MoE 论文结论不能直接外推到所有 expert 数量和 token 分布。
- 引用时应区分“公式来源”和“实测数字”，避免误把公式当成实测。
- 同一篇论文的不同版本可能结论不同，引用前要确认版本与章节。

## Links To Concepts

- [[10-foundations/model-architecture-cost-formulas]]
- [[10-foundations/memory-and-roofline]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/disaggregated-and-moe-serving]]
- [[70-sources/key-papers/flashattention-papers]]

## Follow Up

- 后续按 GQA、MoE、FlashAttention 分别建独立 source card。
- 后续补原始 PDF 摘要到 `raw-sources/`。
