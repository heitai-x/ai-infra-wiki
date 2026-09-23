---
title: Attention Masks and Safe Softmax
type: concept
topic: inference
component: attention-softmax
level: intermediate
status: active
last_updated: 2026-09-23
owner: local
reliability: medium
tags: [attention, softmax, mask, numerical-stability, causal]
source_refs:
  - 70-sources/key-papers/transformer-architecture-papers
  - 70-sources/key-papers/flashattention-papers
  - 70-sources/official-docs/cuda-programming-guide-docs
sources:
  - ../raw-sources/inference/transformer-components-smoke-2026-09-23.md
---

# Attention Masks and Safe Softmax

## 一句话

Attention mask 决定一个 query 能看到哪些 key；safe softmax 在屏蔽、极端 logits 和低精度输入下仍保持有限输出，并把 fully masked row 明确约定为全零。

## 系统位置

它位于 `QK^T / sqrt(Dh)` 和 `weights @ V` 之间，是 Transformer attention 的数值边界：

```text
Q, K -> scores [B,H,Tq,Tk]
             -> mask（causal / padding / request-local）
             -> safe softmax [B,H,Tq,Tk]
             -> weights @ V
```

这个页面对应 IDE 文件 `D:\桌面\code\softmax.py` 的 `safe_softmax(x, mask=None, dim=-1)`。`MHA.py` 和 `GQA.py` 都把它作为最后一个 Key 维度上的归一化算子。

## 输入、输出和 layout

| 张量 | 常见 shape | 语义 |
|---|---|---|
| `scores` | `[B,H,Tq,Tk]` | 每个 query 对每个 key 的缩放点积 |
| causal mask | `[Tk,Tk]` 或 `[1,1,Tq,Tk]` | `True` 表示允许读取，`False` 表示未来位置不可读 |
| padding / request mask | `[B,Tq,Tk]` 或 `[B,H,Tq,Tk]` | 屏蔽 padding、跨请求或无效 token |
| `weights` | 与 `scores` 相同 | 沿 `Tk` 归一化；有效 row 的和约为 1 |

`softmax.py` 先把 mask 转成布尔张量，再用 `masked_fill` 应用 mask。调用者仍然需要保证 mask 能广播到 `scores`；文件本身没有提供更详细的 shape error message。

## Mask 的两类语义

### Causal mask

对于自回归生成，第 `i` 个 query 只能读取位置 `j <= i`：

```text
M[i,j] = True  if j <= i
         False otherwise
```

长度为 4 的 mask 是：

```text
[[1, 0, 0, 0],
 [1, 1, 0, 0],
 [1, 1, 1, 0],
 [1, 1, 1, 1]]
```

### Padding / request mask

它表达输入数据是否有效，而不是时间方向。例如 batch 中两条请求长度不同，可以把短请求末尾的 key 列设为 `False`。真实 serving 还可能需要 request-local mask，避免一个 batch 内的序列互相读取。

两种 mask 可以按逻辑与合并：

```text
effective_mask = causal_mask & padding_or_request_mask
```

## 稳定计算路径

对每个固定的 query row `i`，令 `S_i` 为 logits，`M_i` 为保留位置：

```text
m_i = max(S_i[j] for j where M_i[j] is True)
e_i[j] = exp(S_i[j] - m_i)              if M_i[j] is True
         0                              otherwise
d_i = sum_j e_i[j]
p_i[j] = e_i[j] / d_i                   if d_i > 0
         0                              otherwise
```

`softmax.py` 对应的代码顺序是：

1. `masked_fill(~mask, -inf)`：先让无效位置不会参与最大值和指数。
2. `max(dim=dim)`：减去 row max，避免大正数直接 `exp` 溢出。
3. `torch.where(isfinite(row_max), row_max, 0)`：fully masked row 没有有限最大值时使用零作为安全基准。
4. `exp` 后再次把 mask 外位置设成零。
5. 分母为零时改成一，最终让 fully masked row 保持全零而不是 NaN。

### Fully masked row 的含义

全 `False` 的 row 输出全零，行和也为零；它不是一个概率分布。这个约定适合让后续 `weights @ V` 产生零向量，但调用者必须知道“行和为 1”只适用于至少有一个有效 key 的 row。上游 scheduler 或数据整理逻辑仍应尽量避免产生无效 query。

## dtype 和非有限值边界

- 代码要求 `x` 是浮点张量，不接受整数输入。
- fp32 通常提供最宽的动态范围。
- fp16/bf16 输入在当前实现中没有像 `RMSNorm.py` 那样显式转 fp32；减去最大值后正向溢出风险降低，但很小的概率可能下溢为零。
- 输入包含 NaN 时，`max`、`exp` 或分母仍可能传播 NaN；当前函数不是 NaN 清洗器。
- `-inf` 作为已屏蔽值是可行的，但如果调用者把 `-inf` 当作有效 logits，结果会进入 fully masked 或非有限边界，需要单独检查。

## 计算、显存和 kernel 代价

未融合的 attention 需要物化 `scores` 和 `weights`，其主要开销近似为：

```text
score FLOPs   ~= 2 * B * H * Tq * Tk * Dh
weight memory ~= B * H * Tq * Tk * dtype_bytes
```

mask 本身通常是布尔值，但如果显式物化为 `[B,H,Tq,Tk]`，它也会增加读写和带宽压力。FlashAttention 一类 kernel 把 tile、mask、softmax 统计量和 `V` 聚合放在更紧凑的执行路径中，减少 HBM 往返；这属于 kernel 实现收益，不改变上面的数学契约。

## 可运行证据

命令：

```text
python scripts/transformer_components_smoke.py \
  --source-root D:\桌面\code \
  --output artifacts/transformer-components/smoke-2026-09-23.json
```

本地参考结果验证了：

- causal mask 后未来位置权重为零；
- fully masked row 为全零且保持有限；
- fp32 和 fp16 参考路径没有产生非有限值。

这是 NumPy 参考和源码 AST 盘点；当前机器的 PyTorch 2.13.0 在加载 `c10.dll` 时触发 Windows `WinError 1114`，所以没有把这组数字标为 PyTorch kernel 实测。

## 代价与边界清单

- **数值**：极端 logits、NaN、全 mask row 需要显式测试。
- **shape**：mask 必须能广播到 `[B,H,Tq,Tk]`；safe softmax 不负责把任意 1D mask 猜成正确语义。
- **性能**：`Tq * Tk` 仍是 attention 的主要二次项；融合 kernel、分块和在线 softmax 才能减少中间张量 IO。
- **系统**：decode 通常 `Tq=1`、`Tk` 为历史长度，mask 和 cache 索引需要一起维护。

## 来源

- [[70-sources/key-papers/transformer-architecture-papers]]
- [[70-sources/key-papers/flashattention-papers]]
- [[70-sources/official-docs/cuda-programming-guide-docs]]
- `raw-sources/inference/transformer-components-smoke-2026-09-23.md`

## 相关页面

- 前置：[[10-foundations/model-architecture-cost-formulas]]
- 后续：[[30-inference-systems/mha-gqa-attention]]
- KV 连接：[[30-inference-systems/kv-cache-compute-path]]
- Serving：[[30-inference-systems/kv-cache-paged-attention]]、[[30-inference-systems/batching-scheduling]]
