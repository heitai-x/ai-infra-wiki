---
title: MHA and GQA Attention
type: concept
topic: inference
component: mha-gqa
level: intermediate
status: active
last_updated: 2026-09-23
owner: local
reliability: medium
tags: [mha, gqa, attention, qkv, heads, kv-memory]
source_refs:
  - 70-sources/key-papers/transformer-architecture-papers
  - 70-sources/key-papers/flashattention-papers
  - 70-sources/official-docs/vllm-docs
sources:
  - ../raw-sources/inference/transformer-components-smoke-2026-09-23.md
---

# MHA and GQA Attention

## 一句话

MHA 为每个 query head 配一组独立的 K/V head，GQA 保留多个 query head 但让一组 query 共享一个 K/V head，从而减少 K/V projection、KV cache 和部分通信容量。

## 系统位置

当前 IDE 文件是 `D:\桌面\code\MHA.py` 和 `D:\桌面\code\GQA.py`。它们实现的是完整序列 self-attention 的教学路径，尚未把 KV cache 接到 forward：

```text
X [B,T,input_dim]
  -> Q/K/V projection
  -> split heads
  -> QK^T / sqrt(Dh)
  -> causal / user mask
  -> safe softmax
  -> weights @ V
  -> concat heads
  -> output projection
  -> Y [B,T,d_model]
```

## MHA 的 shape 账本

取一个具体例子：`B=2`、`T=8`、`input_dim=16`、`d_model=32`、`Hq=Hkv=4`、`Dh=8`。

| 步骤 | shape | 说明 |
|---|---|---|
| 输入 `X` | `[2,8,16]` | 每个 token 的输入向量 |
| `qkv_layer(X)` | `[2,8,96]` | `3*d_model=96`，Q/K/V 拼在最后一维 |
| `view` | `[2,8,3,4,8]` | 拆出 Q/K/V、head 和 head_dim |
| `permute` | `[3,2,4,8,8]` | 第一维索引取出 Q/K/V，layout 为 `[B,H,T,Dh]` |
| `scores=QK^T` | `[2,4,8,8]` | 每个 query 读取 8 个 key |
| `weights@V` | `[2,4,8,8]` | 仍然是 head layout |
| transpose/concat | `[2,8,32]` | 回到 token-major layout |
| `out_layer` | `[2,8,32]` | 输出投影不改变 `d_model` |

公式为：

```text
Q = X W_Q, K = X W_K, V = X W_V
S = Q K^T / sqrt(Dh)
A = safe_softmax(S, mask, dim=-1)
O = A V
Y = concat_heads(O) W_O
```

`MHA.py` 用一个 `qkv_layer` 生成 `3*d_model`，这与三个独立线性层在数学上等价，但权重布局和 kernel 融合方式可能不同。

## GQA 的 shape 和 group 映射

设 `Hq=4`、`Hkv=2`、`Dh=8`，则 `group_size=Hq/Hkv=2`：

| 张量 | 初始 shape | 代码处理后 |
|---|---|---|
| Q | `[B,T,32]` -> `[B,4,T,8]` | 保持 4 个 query heads |
| K | `[B,T,16]` -> `[B,2,T,8]` | 每个 KV head 服务 2 个 query head |
| V | `[B,T,16]` -> `[B,2,T,8]` | 与 K 相同 |
| K/V for score | `[B,2,T,8]` | `repeat_interleave` 后变成 `[B,4,T,8]` |

映射顺序是：

```text
KV head 0 -> Q head 0, 1
KV head 1 -> Q head 2, 3
```

当前实现通过 `repeat_interleave` 显式复制 K/V，因此它清楚展示了 group 关系，但会在 attention 计算前物化重复数据。真实 fused GQA kernel 可以保持 `[B,Hkv,T,Dh]`，在读取时按 group 映射，避免完整复制。

## MHA、MQA、GQA 的资源差异

| 变体 | Query heads | KV heads | KV cache 相对 MHA | 典型取舍 |
|---|---:|---:|---:|---|
| MHA | `Hq` | `Hq` | `1x` | 表达能力和 K/V 独立性最强，KV 最贵 |
| GQA | `Hq` | `1 < Hkv < Hq` | `Hkv/Hq` | 在质量、容量和吞吐之间折中 |
| MQA | `Hq` | `1` | `1/Hq` | KV 最省，共享最强，质量和 kernel 适配需验证 |

假设 `input_dim=d_model=D`，忽略 bias：

```text
MHA QKV weight ~= 3 * D * D
GQA QKV weight ~= D*D + 2 * D * (Hkv * Dh)
                 = D*D + 2 * D*D * Hkv/Hq
KV bytes/layer  = B * T * 2 * Hkv * Dh * dtype_bytes
```

因此，在 `Hq=32,Hkv=8` 时，K/V cache 只有 MHA 的四分之一；Q projection 和 score 的 query head 数并没有减少。GQA 不是把整个 attention 计算变成四分之一，而是主要减少 K/V 投影、缓存和相关读取。

## Prefill 和 decode 的 shape

当前两个 IDE 模块的 `forward` 都接收单一 `seq_len`，所以它们的 `Q` 和 `K/V` 长度相同。接入 KV cache 后应区分：

```text
prefill: Q [B,Hq,Tprompt,Dh], K/V [B,Hkv,Tprompt,Dh]
decode:  Q [B,Hq,1,Dh],       K/V [B,Hkv,Tpast+1,Dh]
scores:  [B,Hq,1,Tpast+1]
```

这是从模型组件连接到 serving 的关键一步：decode 的 query 很短，但每步都读取不断增长的历史 K/V。对应 cache 细节见 [[30-inference-systems/kv-cache-compute-path]]。

## 计算、显存和通信

- score/value 主项近似 `O(B * Hq * Tq * Tk * Dh)`；GQA 仍使用 `Hq` 个 query head，所以 score 规模不按 `Hkv/Hq` 线性缩小。
- Q/K/V projection 的 K/V 输出宽度按 `Hkv*Dh` 缩小；当 `input_dim=d_model` 时，GQA 的 K/V 权重和激活都少于 MHA。
- KV cache 公式必须明确是 global 还是 per-rank。TP 下使用每个 rank 实际持有的 `Hkv` 和 `Dh`，不能把全局 head 数直接乘到单卡显存。
- head layout 的 transpose/contiguous 会影响内存访问；`MHA.py` 和 `GQA.py` 在 concat 前调用 `contiguous()`，避免把非连续 view 直接送入线性层。
- fused attention、paged KV 和 GQA kernel 的收益来自减少 HBM 往返、避免重复 K/V 或改善 tile；不能只从 Python FLOPs 公式推断实际吞吐。

## 可运行证据

```text
python scripts/transformer_components_smoke.py \
  --source-root D:\桌面\code \
  --output artifacts/transformer-components/smoke-2026-09-23.json
```

参考检查验证了 `MHA output=[2,4,8]`、`weights=[2,4,4,4]`，以及 `Hq=4,Hkv=2` 的 GQA 输出 shape 和 causal mask。它同时通过 AST 盘点确认两个 IDE 文件仍包含 `MultiheadAttention`、`GQA` 和 alias `GroupedQueryAttention`。

## 代价与边界清单

- 当前实现只做 self-attention；cross-attention 需要独立的 `Tq`、`Tk` 和 Q/K/V 输入。
- 当前实现没有 dropout、rotary embedding、cache offset 或 block table；这些属于完整模型/runtime 的额外状态。
- GQA 中显式 `repeat_interleave` 会放大临时 K/V；生产 kernel 应评估是否能按 group 读取。
- mask 需要和 `[B,H,Tq,Tk]` 广播一致；GQA 的 Python 文件对 list mask 的预处理比 MHA 更严格，调用方应传入 tensor/array 并测试 shape。
- “KV 少”不等于“总延迟按同一比例下降”：Q projection、score、output projection、权重读取和调度仍在关键路径上。

## 来源

- [[70-sources/key-papers/transformer-architecture-papers]]
- [[70-sources/key-papers/flashattention-papers]]
- [[70-sources/official-docs/vllm-docs]]
- `raw-sources/inference/transformer-components-smoke-2026-09-23.md`

## 相关页面

- 前置：[[10-foundations/attention-masks-and-softmax]]、[[10-foundations/normalization-and-activation]]
- 成本：[[10-foundations/model-architecture-cost-formulas]]
- KV：[[30-inference-systems/kv-cache-compute-path]]、[[30-inference-systems/kv-cache-paged-attention]]
- Serving：[[30-inference-systems/llm-serving-map]]、[[30-inference-systems/batching-scheduling]]
