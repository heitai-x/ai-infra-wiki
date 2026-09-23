# Transformer Component Source Inventory

## Scope

- 盘点日期：2026-09-23
- IDE 源码根目录：`D:\桌面\code`
- 仓库内实验脚本：`scripts/transformer_components_smoke.py`
- 参考输出：`artifacts/transformer-components/smoke-2026-09-23.json`
- 说明：六个 Python 文件目前仍以 IDE 工作区为权威输入，没有直接复制到 Wiki 仓库。仓库保存入口、静态盘点和可复现实验；源码变更后需要重新运行 inventory 和 smoke test。

## 文件与入口

| 文件 | 入口 | 输入 / 输出 shape | dtype / layout | 当前边界 |
|---|---|---|---|---|
| `softmax.py` | `safe_softmax(x, mask=None, dim=-1)` | `x` 任意 `ndim >= 1`；输出与 `x` 相同 | 浮点输入；mask 布尔化并按广播规则使用；沿 `dim` 归一化 | 没有显式检查 mask 是否可广播；NaN 输入不会被清理；全 mask 行约定为全零 |
| `ReLu.py` | `relu(x)`、`ReLU.forward(x)` | 任意 shape；输出与 `x` 相同 | `torch.where` 保留 dtype/device；逐元素路径 | 没有额外 shape 约束；零值输出为零；没有记录激活统计 |
| `RMSNorm.py` | `RMSNorm(dim, eps=1e-6, bias=False)`、`forward(x)` | `x[..., dim]`；输出相同 shape | fp16/bf16 转 fp32 计算，再转回输入 dtype；参数是 `[dim]` | 归一化最后一维；可选 bias 是教学扩展；空最后一维会产生非有限值 |
| `MHA.py` | `MultiheadAttention(input_dim, d_model, num_heads)`、`forward(x, mask=None, is_causal=False)` | 输入 `[B,T,input_dim]`；Q/K/V 临时 `[B,H,T,Dh]`；scores/weights `[B,H,T,T]`；输出 `[B,T,d_model]` | `qkv_layer` 一次生成 `[B,T,3*d_model]`；head layout 从 `[B,T,3,H,Dh]` permute 为 `[3,B,H,T,Dh]` | 只实现 self-attention，Q/K 长度相同；mask 支持 2D/3D 扩展；没有 dropout 或 cache |
| `GQA.py` | `GQA(input_dim, d_model, num_q_heads, num_kv_heads)`、`forward(...)` | Q `[B,Hq,T,Dh]`；K/V 初始 `[B,Hkv,T,Dh]`，复制后 `[B,Hq,T,Dh]`；输出 `[B,T,d_model]` | `Hq % Hkv == 0`；`repeat_interleave` 显式复制 KV head | 教学实现会 materialize 复制后的 K/V；真实 fused kernel 可以按 group 读取而不复制 |
| `kvcache.py` | `KVCache(...)`、`append(new_k,new_v)`、`get()`、`reset()` | cache `[B,Hkv,Tmax,Dh]`；追加 `[B,Hkv,Tnew,Dh]`；get 返回 `[B,Hkv,length,Dh]` | contiguous preallocated tensor；严格检查 device/dtype；单一全 batch `length` | 不能表示 batch 内 ragged length；没有 block table、page、position id、eviction 或 prefix reuse |

## 代码路径与系统概念

```text
softmax.py -> attention mask / numerical stability
ReLu.py + RMSNorm.py -> transformer block elementwise path
MHA.py -> QKV projection / score / value aggregation
GQA.py -> fewer KV heads / repeated group mapping
kvcache.py -> prefill append / decode read / contiguous storage
```

## 已运行的静态与参考测试

命令：

```text
python scripts/transformer_components_smoke.py \
  --source-root D:\桌面\code \
  --output artifacts/transformer-components/smoke-2026-09-23.json
```

结果：

- 六个文件都存在，AST 入口定义全部找到。
- safe softmax 的 causal/全 mask 行、fp32/fp16 参考计算通过。
- ReLU、RMSNorm、MHA causal shape、GQA shape、KV append/decode/reset 参考测试通过。
- 当前 Python 进程无法加载本机 PyTorch 2.13.0 的 `c10.dll`（Windows `WinError 1114`），所以本轮没有把 NumPy 参考结果写成 PyTorch 实测结果。恢复 PyTorch 运行环境后，使用同一命令会自动追加六个 IDE 文件的运行时测试。

## 待补证据

1. 在可导入 PyTorch 的 CPU 或 GPU 环境运行同一 smoke test，并记录 `torch.__version__`、CUDA 可用性和设备信息。
2. 为 MHA/GQA 增加不同 batch、sequence、dtype 的实际输出对照。
3. 为 KV cache 增加 batch 内不同请求长度、paged layout 和 eviction 的实验。
