---
title: Normalization and Activation
type: concept
topic: inference
component: normalization-activation
level: intermediate
status: active
last_updated: 2026-09-23
owner: local
reliability: medium
tags: [rmsnorm, relu, activation, normalization, residual, dtype]
source_refs:
  - 70-sources/key-papers/transformer-architecture-papers
  - 70-sources/official-docs/cuda-programming-guide-docs
sources:
  - ../raw-sources/inference/transformer-components-smoke-2026-09-23.md
---

# Normalization and Activation

## 一句话

RMSNorm 控制每个 token 向量的尺度，ReLU 提供逐元素非线性；两者都在 Transformer block 的 residual 数据流中增加计算路径，却不改变 token 的主 shape。

## 系统位置

当前 IDE 文件分别是 `D:\桌面\code\RMSNorm.py` 和 `D:\桌面\code\ReLu.py`。它们是 block 中的局部组件，不负责 residual 相加或线性层本身：

```text
PreNorm block（常见 decoder 路径）

x ------------------------------+-------------------> residual output
 \-> RMSNorm -> attention/MLP ->+
                              add
```

一个简单的 MLP 子路径可以写成：

```text
h = W1 x + b1
a = ReLU(h)                 # 或 SwiGLU / GELU 等替代
y = W2 a + b2
out = x + y                 # residual 由 block 负责
```

## ReLU

### 公式与 shape

```text
ReLU(x) = max(0, x)
```

`relu(x)` 和 `ReLU.forward(x)` 都保持输入 shape、dtype 和 device。输入可以是 `[B,T,D]`、`[B,T,intermediate]` 或任意其他 shape；操作沿每个元素独立执行。

### 计算与内存

- 每个元素需要一次比较和一次选择，算术强度低，通常更接近 memory/elementwise 路径。
- 输出需要与输入同 shape 的写入；如果后续 kernel 没有融合，读写中间 activation 会增加 HBM 流量。
- “负值变成零”不等于框架自动压缩存储；dense tensor 仍然占据完整内存。
- ReLU 的零输出可以作为激活分布练习，但不要直接把零比例当作稀疏 kernel 的加速比。

### 边界

- 零点的梯度约定由 autograd 实现决定；当前文件只定义 forward。
- 没有 dropout、量化或激活统计；如果要比较 GELU/SwiGLU，需要固定输入分布、dtype 和 kernel 路径。

## RMSNorm

### 公式

对最后一维 `D` 的向量 `x`：

```text
mean_square(x) = (1 / D) * sum_j x_j^2
rms(x)         = sqrt(mean_square(x) + eps)
y_j            = gamma_j * x_j / rms(x) + beta_j (可选)
```

RMSNorm 不减去均值，因此它与 LayerNorm 的区别不是“少一个参数”这么简单：RMSNorm 保留向量的均值方向，只控制 root-mean-square 尺度。当前实现的参数 shape 是 `weight=[D]`，`bias=[D]` 只有在 `bias=True` 时创建。

### 代码中的 dtype 路径

`RMSNorm.forward` 的顺序是：

1. 要求输入至少一维、最后一维等于 `dim`，并且是浮点 dtype。
2. 对 fp16/bf16 输入，把 `x` 转成 fp32 计算平方均值和 `rsqrt`。
3. 归一化后转回输入 dtype。
4. 将 `weight`（和可选 `bias`）转换到输入 dtype 后逐通道应用。

因此，代码提供了“低精度存储、高精度归一化统计量”的教学路径，但最终输出仍可能受低精度舍入影响。`eps` 防止全零或极小向量在除法阶段产生无穷值；它不是用来修复 NaN 输入的。

### shape 与 layout

| 输入 | 归一化轴 | 参数 | 输出 |
|---|---|---|---|
| `[B,T,D]` | 最后一维 `D` | `[D]` | `[B,T,D]` |
| `[B,D]` | 最后一维 `D` | `[D]` | `[B,D]` |
| `[T,D]` | 最后一维 `D` | `[D]` | `[T,D]` |

它不会改变 token 数 `T`，也不生成 attention 的 `[T,T]` score。把 RMSNorm 和 attention 的 shape 混淆，会导致错误的显存估算。

## Residual、PreNorm 和 PostNorm

组件文件只实现归一化和激活；block 需要明确 residual 放置位置：

```text
PreNorm:  y = x + F(RMSNorm(x))
PostNorm: y = RMSNorm(x + F(x))
```

`F` 可以是 attention 或 MLP。PreNorm 常被用于改善深层训练的梯度路径，但具体模型架构、初始化和训练稳定性仍要看完整实现。推理时，两种路径都会影响 kernel 数量、临时 activation 和 residual buffer 的读写。

## 计算、显存与系统代价

- RMSNorm 对 `[B,T,D]` 需要读取并平方归约 `B*T*D` 个元素，再写回同样大小的输出；归约和 `rsqrt` 比 ReLU 更重。
- ReLU 对 `[B,T,I]` 只做逐元素比较/选择，但 MLP 的两次线性层通常远大于 ReLU 本身的 FLOPs。
- 低精度权重和 activation 降低存储与带宽，但 RMSNorm 的统计量是否转 fp32 会改变数值稳定性和临时 buffer dtype。
- fused RMSNorm、bias/activation fusion 可以减少中间写回；优化收益必须用 profiler 或 kernel benchmark 验证。

## 可运行证据

参考命令：

```text
python scripts/transformer_components_smoke.py \
  --source-root D:\桌面\code \
  --output artifacts/transformer-components/smoke-2026-09-23.json
```

本地结果验证了 ReLU 的负值清零，以及 fp16 输入的 RMSNorm 输出 RMS 接近 1。由于当前机器的 PyTorch native DLL 无法加载，这个结果仍标记为 NumPy reference，而不是 PyTorch kernel 测量。

## 代价与边界清单

- **统计轴**：代码固定沿最后一维归一化；改变 layout 后必须重新确认 `dim`。
- **dtype**：当前 RMSNorm 对 fp16/bf16 上采样到 fp32，ReLU 不做额外上采样。
- **参数**：可选 bias 是当前教学实现的扩展，不能默认等价于所有模型的 RMSNorm。
- **残差**：RMSNorm 文件没有 residual；需要从完整 Transformer block 判断 PreNorm/PostNorm。
- **性能**：elementwise 算子的零值比例不能直接换算成稀疏加速；要看融合、访存和 kernel 实现。

## 来源

- [[70-sources/key-papers/transformer-architecture-papers]]
- [[70-sources/official-docs/cuda-programming-guide-docs]]
- `raw-sources/inference/transformer-components-smoke-2026-09-23.md`

## 相关页面

- 前置：[[10-foundations/model-architecture-cost-formulas]]
- Attention：[[10-foundations/attention-masks-and-softmax]]、[[30-inference-systems/mha-gqa-attention]]
- Serving：[[30-inference-systems/llm-serving-map]]
