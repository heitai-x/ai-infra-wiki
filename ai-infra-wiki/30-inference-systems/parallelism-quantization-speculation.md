---
title: Parallelism Quantization Speculation
type: concept
topic: inference
component: optimization
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [tensor-parallel, quantization, speculative-decoding, inference]
source_refs: [70-sources/official-docs/vllm-docs, 70-sources/official-docs/sglang-docs, 70-sources/official-docs/tensorrt-llm-docs, 70-sources/key-papers/speculative-decoding-paper, 70-sources/key-papers/speculative-decoding-papers, 70-sources/key-papers/flashattention-papers]
---

# Parallelism Quantization Speculation

## 一句话

推理优化主要围绕三类杠杆：并行让模型放得下或吞吐更高，量化降低显存和带宽，投机解码减少大模型 decode 步数。

## 推理并行

- Tensor Parallel：切分线性层和 attention heads，常用于单卡放不下或需要更高吞吐的模型。
- Pipeline Parallel：层切分，推理中受流水调度和 latency 影响更敏感。
- Data Parallel / replica：多副本处理不同请求，是平台扩容最直接方式。
- Expert Parallel：MoE serving 中按 expert 分布，但要解决热点和 all-to-all。

推理并行的关键不是“卡越多越快”，而是通信是否小于并行带来的计算/容量收益。

## Quantization

| 类型 | 降低什么 | 风险 |
|---|---|---|
| Weight INT8/INT4/FP8 | 权重显存和带宽 | 精度、kernel 支持、校准 |
| KV cache quantization | KV 显存和带宽 | 长上下文质量、attention kernel |
| Activation quantization | 中间激活带宽 | 数值稳定性 |

量化收益在 decode 阶段通常更明显，因为权重和 KV 反复从 HBM 读取。

## Speculative decoding

使用小模型或轻量 draft mechanism 先生成多个候选 token，再由目标模型验证。若接受率高，可以减少目标模型 decode iteration 数。

收益取决于：

- draft 生成速度。
- token acceptance rate。
- 目标模型验证 kernel 是否高效。
- batch 和 scheduler 是否能处理变长接受。
- 小模型额外显存和部署成本。

## 观测点

- tokens/sec before/after。
- TTFT、TPOT、ITL。
- acceptance rate。
- GPU memory、HBM bandwidth。
- quality regression eval。
- kernel path 是否 fallback。

## 本地证据

- 暂无 `raw-sources/` 下的量化精度对比、speculative decoding acceptance rate、TP/EP 实测吞吐样本。
- 章节中推理并行、量化、speculative decoding 收益属于对 vLLM / SGLang / TensorRT-LLM 文档 + 投机解码论文 / FlashAttention 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/inference/quant-<model>.md` 与 1 份 `raw-sources/inference/speculative-<draft>-<target>.md`，含量化精度、tokens/sec、acceptance rate、TPOT。

## 尚未本地验证的边界

- “量化在 decode 阶段收益更明显”依赖具体 kernel 与量化方案，本页未引用本机数字。
- speculative decoding 的收益高度依赖 acceptance rate，本页未给出实测曲线。
- “kernel path 是否 fallback” 是经验检查项，需要 Nsight Compute 验证。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/tensorrt-llm-docs]]
- [[70-sources/key-papers/speculative-decoding-paper]]
- [[70-sources/key-papers/speculative-decoding-papers]]
- [[70-sources/key-papers/flashattention-papers]]

## 相关页面

- [[30-inference-systems/llm-serving-map]]
- [[80-playbooks/benchmark-design]]
- [[60-frameworks/tensorrt-triton-ray-kserve]]
