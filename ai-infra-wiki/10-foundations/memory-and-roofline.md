---
title: Memory And Roofline
type: concept
topic: hardware
component: performance-model
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [roofline, memory, flops, bandwidth]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# Memory And Roofline

## 一句话

Roofline 模型用算术强度把性能瓶颈分成 compute-bound 和 memory-bound。AI Infra 做容量规划和性能优化时，先问“这个操作每读写 1 byte 做多少 FLOPs”。

## 核心公式

```text
arithmetic_intensity = FLOPs / bytes_moved
attainable_performance = min(peak_flops, arithmetic_intensity * peak_bandwidth)
```

如果 `arithmetic_intensity * bandwidth < peak_flops`，操作通常 memory-bound；否则可能 compute-bound。

## 训练直觉

- 大 GEMM 通常有较高算术强度，是训练 MFU 的主要来源。
- LayerNorm、embedding、optimizer update 通常更偏 memory-bound。
- FSDP/ZeRO 会降低状态显存，但引入参数 all-gather 和梯度 reduce-scatter。
- Activation checkpointing 用额外 compute 换显存，适合 compute 还有余量而显存紧张的场景。

## 推理直觉

- Prefill 对长 prompt 做大矩阵/attention，计算密度较高。
- Decode 每步 token 少，反复读取权重和 KV cache，常见 memory-bound。
- 权重量化降低 HBM 读带宽和容量压力，但可能引入 dequant kernel 或精度损失。
- KV cache 量化/分页降低容量压力，但调度和 kernel 支持很关键。

## 显存账本

训练显存主要由以下部分组成：

```text
parameters + gradients + optimizer_states + activations + temporary_buffers + fragmentation
```

推理显存主要由以下部分组成：

```text
model_weights + kv_cache + runtime_workspace + cuda_graph_pools + fragmentation
```

KV cache 粗略估算：

```text
bytes = batch * seq_len * layers * 2(K,V) * kv_heads * head_dim * dtype_bytes
```

若使用 GQA/MQA，`kv_heads` 小于 query heads，KV cache 显存会下降。

## 如何把公式用于排障

- OOM：先列显存账本，再判断哪一项随 batch/seq/parallelism 增长。
- 吞吐低：估算 FLOPs 上限，再看 profiler 中 GEMM 是否占比合理。
- decode 慢：看 HBM 带宽、KV cache 访问、batch size、scheduler。
- 通信慢：不要用 roofline 硬套，转去看 collective 大小、拓扑和 overlap。

## 本地证据

- 暂无 `raw-sources/` 下的 GPU 实测 peak FLOPS / HBM bandwidth、kernel intensity profiler 输出。
- 章节中 Roofline 公式、训练 / 推理直觉与显存账本属于对 MLSys Book + Transformer 论文 + FlashAttention 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/hardware/roofline-<gpu>.md`，含本机 peak FLOPS、bandwidth、若干 kernel 的 intensity 与实测占比。

## 尚未本地验证的边界

- Roofline 模型假设 “单层算术强度能算清楚”，真实 GEMM / attention kernel 不一定落在 simple bound 上。
- “GQA / MQA 减小 KV cache 显存” 依赖 per-rank 口径，本页已在公式段说明，但未引用本机数字。
- “通信慢不要硬套 roofline” 是经验提醒，本页未引用具体通信 trace 样本。

## 来源

- [[70-sources/official-docs/mlsys-book-docs]]
- [[70-sources/key-papers/transformer-architecture-papers]]
- [[70-sources/key-papers/flashattention-papers]]

## 相关页面

- [[30-inference-systems/kv-cache-paged-attention]]
- [[20-training-systems/activation-optimizer-checkpoint]]
- [[80-playbooks/serving-capacity-planning]]
