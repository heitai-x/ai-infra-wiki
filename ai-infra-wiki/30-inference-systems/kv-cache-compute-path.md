---
title: KV Cache Compute Path
type: concept
topic: inference
component: kv-cache-compute
level: intermediate
status: active
last_updated: 2026-09-23
owner: local
reliability: medium
tags: [kv-cache, prefill, decode, gqa, memory, serving]
source_refs:
  - 70-sources/key-papers/pagedattention-paper
  - 70-sources/key-papers/transformer-architecture-papers
  - 70-sources/official-docs/vllm-docs
  - 70-sources/key-papers/flashattention-papers
sources:
  - ../raw-sources/inference/transformer-components-smoke-2026-09-23.md
---

# KV Cache Compute Path

## 一句话

KV cache 把已经计算过的历史 key/value 保存在可复用的存储中，使 decode 每步只生成一个新 query 并读取历史 K/V；它把重复计算换成显存容量、带宽和调度管理。

## 系统位置

请求级路径可以拆成：

```text
prompt tokens
  -> prefill: 计算所有 prompt 的 Q/K/V
  -> append K/V to cache
  -> decode loop:
       new token -> Q
       historical K/V + new K/V -> attention
       append one position
  -> stream token
```

IDE 文件 `D:\桌面\code\kvcache.py` 给出一个连续、预分配、单一 batch length 的最小实现。它可以作为 prefill/decode 的状态机练习，但不是 paged attention runtime。

## Prefill 与 decode 的 shape

设 batch 为 `B`、query heads 为 `Hq`、KV heads 为 `Hkv`、head dimension 为 `Dh`：

| 阶段 | Q | 新 K/V | attention score | cache 读取 |
|---|---|---|---|---|
| prefill，prompt 长度 `P` | `[B,Hq,P,Dh]` | `[B,Hkv,P,Dh]` | `[B,Hq,P,P]` | 空或 prefix cache |
| decode，已有 `L` 个 token | `[B,Hq,1,Dh]` | `[B,Hkv,1,Dh]` | `[B,Hq,1,L+1]` | `[B,Hkv,L+1,Dh]` |

Prefill 计算更像大矩阵乘；decode 每次 query 很短，却需要反复读取随 `L` 增长的 K/V。这个差异连接到 [[30-inference-systems/llm-serving-map]] 的 TTFT/TPOT 和 [[30-inference-systems/batching-scheduling]] 的 iteration 调度。

## 当前连续 cache 的契约

`KVCache(batch_size, num_kv_heads, max_seq_len, head_dim, device, dtype)` 预分配：

```text
k: [B, Hkv, Tmax, Dh]
v: [B, Hkv, Tmax, Dh]
```

| 方法 / 属性 | 输入 / 输出 | 状态变化 |
|---|---|---|
| `append(new_k,new_v)` | 两者均为 `[B,Hkv,Tnew,Dh]` | 写入 `[length:length+Tnew]`，再把 `length` 增加 `Tnew` |
| `get()` | 返回 `[B,Hkv,length,Dh]` 的 K/V view | 不改变状态，不读取未初始化区域 |
| `remaining_length` | 整数 `Tmax-length` | 只读 |
| `is_full` | 布尔值 | `length >= Tmax` |
| `reset()` / `clear()` | 无 | 只把 `length` 置零，下次 append 覆盖旧数据 |

`append` 会严格检查 rank、shape、batch、KV head 数、head_dim、device 和 dtype；超过 `max_seq_len` 时抛出 overflow。`torch.no_grad()` 说明这是推理缓存，不应把 cache 写入 autograd 图。

## Append 与历史读取的具体状态机

```text
initial: length=0
prefill append Tnew=P  -> length=P
decode append 1        -> length=P+1
get()                  -> only [:length] is visible
reset()                -> length=0; storage remains allocated
```

这种连续布局适合单请求或所有请求同长度的教学实验。它不能表达 batch 内：

- request A 已经生成 100 token，而 request B 只有 20 token；
- 请求动态加入/退出后不同的物理位置；
- prefix cache 多请求共享同一组物理页；
- eviction、swap、block table 或 copy-on-write。

这些能力属于 [[30-inference-systems/kv-cache-paged-attention]] 和 serving runtime 的内存管理层。

## 显存账本

单层、单 rank 的连续 KV cache 近似为：

```text
bytes = B * Tlive * 2 * Hkv * Dh * dtype_bytes
```

全模型还要乘以 rank 实际持有的 layer 数：

```text
bytes_per_rank = live_tokens * layers_held_by_rank
                 * 2 * kv_heads_held_by_rank * head_dim * dtype_bytes
```

例子：`B=4`、`T=2048`、`layers=32`、`Hkv=8`、`Dh=128`、fp16（2 bytes）时：

```text
4 * 2048 * 32 * 2 * 8 * 128 * 2 bytes
= 536,870,912 bytes ~= 512 MiB
```

同样的 query heads `Hq=32` 如果采用 GQA 的 `Hkv=8`，KV cache 是 MHA `Hkv=32` 的四分之一。这个结论只在 layer、rank、dtype 和 layout 口径一致时成立；TP、PP、KV offload 或副本化 runtime 需要重新列账。

## 连续 cache 与 paged cache

| 设计 | 物理布局 | 优点 | 代价 |
|---|---|---|---|
| contiguous | 每个 batch 预分配 `[B,Hkv,Tmax,Dh]` | 索引简单、连续访问、适合教学和固定长度 | 长度差异造成浪费，扩容和碎片管理困难 |
| paged | 固定 block/page + logical-to-physical table | 支持动态 batch、prefix reuse、回收和更高利用率 | block table、分页 kernel、调度和碎片策略更复杂 |

Paged cache 仍然要满足同一数学契约：query 在逻辑位置 `j` 读取对应历史 K/V；变化的是物理地址和生命周期管理。不能因为采用 page 就改变 `scores` 的逻辑 shape。

## Serving 指标的连接

- **TTFT**：常受 prompt prefill、排队和首个 cache allocation 影响。
- **TPOT / ITL**：decode 每步的权重和 KV 读取、kernel launch、batch 组织共同决定。
- **KV utilization**：已分配 token/page 与可用容量的关系；连续 cache 的 `length/Tmax` 不是 paged runtime 的唯一利用率指标。
- **Admission / preemption**：scheduler 必须在新请求加入前估计 prompt + output 的 KV 需求，容量不足时选择拒绝、等待、换出或降低并发。

因此，“有了 KV cache 就更快”是不完整结论：cache 减少重复计算，但可能把 decode 推到 HBM 带宽、容量和调度瓶颈。

## 可运行证据

```text
python scripts/transformer_components_smoke.py \
  --source-root D:\桌面\code \
  --output artifacts/transformer-components/smoke-2026-09-23.json
```

参考实验执行了 3-token prefill append、1-token decode append、`get()` 历史读取和 `reset()`。结果为 `length=4`、读取 shape `[2,2,4,2]`，并通过 AST 盘点确认 `KVCache.append/get/reset/clear` 入口存在。

## 代价与边界清单

- 当前实现使用单一 `length`，不支持 ragged batch；生产 serving 需要 request-level lengths 或 block table。
- `reset()` 不清零张量；如果调试或安全策略要求清除旧值，需要额外的显式清理成本。
- append 只验证输入和容量，不验证 position id、layer id 或跨请求 ownership。
- cache dtype 必须与新 K/V 完全一致；真实 runtime 还要考虑量化 KV、scale、混合精度和 kernel 支持。
- per-rank 显存公式必须使用该 rank 的 layer/head 切分；global 公式不能直接用于单卡 admission。

## 来源

- [[70-sources/key-papers/pagedattention-paper]]
- [[70-sources/key-papers/transformer-architecture-papers]]
- [[70-sources/key-papers/flashattention-papers]]
- [[70-sources/official-docs/vllm-docs]]
- `raw-sources/inference/transformer-components-smoke-2026-09-23.md`

## 相关页面

- 前置：[[30-inference-systems/mha-gqa-attention]]
- 分页：[[30-inference-systems/kv-cache-paged-attention]]
- 调度：[[30-inference-systems/batching-scheduling]]、[[30-inference-systems/prefix-cache-chunked-prefill-preemption]]
- 容量：[[80-playbooks/serving-capacity-planning]]、[[10-foundations/model-architecture-cost-formulas]]
