---
title: Model Architecture Cost Formulas
type: concept
topic: hardware
component: model-cost
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [transformer, flops, parameters, kv-cache, capacity]
source_refs: [70-sources/key-papers, 70-sources/official-docs]
---

# Model Architecture Cost Formulas

## 目标

把 Transformer 结构连接到训练显存、推理 KV cache、FLOPs 和 MFU。容量规划不能只看“7B/70B”，必须展开 layers、hidden、heads、kv_heads、seq len 和 dtype。

## 参数量粗估

Decoder-only Transformer 单层主要参数：

```text
attention projections ~= hidden * (q_heads + 2 * kv_heads) * head_dim
output projection ~= hidden * hidden
mlp ~= hidden * intermediate * 2 or 3
norm/bias ~= small compared with matmul weights
```

如果是 GQA/MQA，`kv_heads` 小于 `q_heads`，K/V projection 和 KV cache 都下降。MoE 中 expert FFN 参数会显著增加总参数，但每 token 只激活 top-k experts。

## 训练显存账本

```text
parameters + gradients + optimizer_states + activations + temporary_buffers + fragmentation
```

activation 近似随以下维度增长：

```text
micro_batch * seq_len * hidden * layers * saved_tensors_per_layer * dtype_bytes
```

activation checkpoint 用重算换掉一部分 `saved_tensors_per_layer`。

## 推理 KV cache

```text
KV bytes per rank = live_tokens * layers_held_by_rank * 2 * kv_heads_held_by_rank * head_dim * dtype_bytes
```

`live_tokens` 是 running requests 的 prompt + generated token 总和，不是单个请求长度。serving 容量规划必须用 p95/p99 长度分布，而不是只看平均值。

## FLOPs 粗估

常见训练估算会用参数量和 token 数的简化公式，例如 dense decoder-only 模型训练约 `6 * params * tokens` 量级；精确分析需要展开 attention、MLP、vocab head、recompute 和 MoE 激活 expert。

服务端推理要拆：

- prefill：attention 随 prompt length 增大，矩阵乘较大。
- decode：每步 token 少，反复读权重和 KV，常见 memory-bound。

## 使用方式

1. 从 HuggingFace config 抽 `num_hidden_layers`、`hidden_size`、`num_attention_heads`、`num_key_value_heads`、`intermediate_size`。
2. 写参数量、KV、activation、FLOPs 四张账本。
3. 再选择 FSDP/TP/PP/CP/EP 或 serving TP/quantization。
4. 用 [[90-experiments/torchrun-ddp-fsdp-minimal]] 或 [[90-experiments/vllm-sglang-benchmark-harness]] 验证估算。

## 本地证据

- 暂无 `raw-sources/` 下的真实 HF config 拆解与本机 GPU 显存 / KV 容量复现样本。
- 章节中参数量公式、KV cache 公式、训练 / 推理 FLOPs 估算属于对 Transformer 论文 + FlashAttention / PagedAttention 论文 + MLSys Book 的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/training/model-cost-<model>.md`，含从 HF config 抽字段、参数估算 vs 实测、KV 在不同 seq len 下的本机数字。

## 尚未本地验证的边界

- “6 * params * tokens” 是 dense decoder-only 训练 FLOPs 的简化公式，不适用于 MoE、MoE activated、pipeline bubble、vocab head 等场景。
- GQA / MQA 的 KV 节省依赖 per-rank 切分，本页公式段已说明，但没引用本机数字。
- MFU 公式依赖 “是否计入重算 / activation checkpoint”，不同设置下数字差异显著。

## 来源

- [[70-sources/key-papers/transformer-architecture-papers]]
- [[70-sources/key-papers/flashattention-papers]]
- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/official-docs/mlsys-book-docs]]

## 相关页面

- [[10-foundations/memory-and-roofline]]
- [[30-inference-systems/kv-cache-paged-attention]]
- [[80-playbooks/serving-capacity-planning]]
