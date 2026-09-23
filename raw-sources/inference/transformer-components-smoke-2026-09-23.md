---
title: Transformer Components Smoke Test
type: raw
topic: inference
component: transformer-components
level: beginner
status: active
last_updated: 2026-09-23
owner: local
reliability: medium
tags: [raw, transformer, softmax, rmsnorm, mha, gqa, kv-cache, smoke]
artifact:
  kind: component-test
  source: local-run
  collected_at: 2026-09-23
  framework: numpy-reference
  framework_version: numpy-1.26.4
  hardware: Windows CPU host; no GPU measurement
  driver: unavailable
  cuda: unavailable
  command: python scripts/transformer_components_smoke.py --source-root D:\桌面\code --output artifacts/transformer-components/smoke-2026-09-23.json
  raw_output: artifacts/transformer-components/smoke-2026-09-23.json
  sha256: pending
related_sources:
  - 70-sources/key-papers/transformer-architecture-papers
  - 70-sources/key-papers/flashattention-papers
  - 70-sources/official-docs/cuda-programming-guide-docs
related_concepts:
  - 10-foundations/attention-masks-and-softmax
  - 10-foundations/normalization-and-activation
  - 30-inference-systems/mha-gqa-attention
  - 30-inference-systems/kv-cache-compute-path
note: |
  本 artifact 的 NumPy 检查用于验证公式、mask、shape 和连续 cache 状态机。脚本同时盘点 IDE 六个源文件的 AST 定义。
  当前本机 PyTorch 2.13.0 导入时触发 Windows WinError 1114（c10.dll 初始化失败），因此没有记录 PyTorch 运行时数值，也没有 GPU 性能结论。
---

# Transformer Components Smoke Test

## 研究问题

从六个 IDE 源文件出发，能否在一个小 CPU 参考实验中验证：

1. masked softmax 的有限值、因果 mask 和全 mask 行约定；
2. ReLU 和 RMSNorm 的逐元素 / 逐向量输出；
3. MHA 与 GQA 的输出和 score shape；
4. KV cache 的 prefill append、decode append、历史读取和 reset；
5. 源文件中的函数 / 类入口是否仍与交接文档一致。

## 环境

- Python：3.11.7
- NumPy：1.26.4
- 主机：Windows 10（CPU 参考运行）
- 源码根目录：`D:\桌面\code`
- PyTorch：2.13.0 已安装但在导入 `c10.dll` 时触发 `WinError 1114`，运行时检查被跳过
- GPU / CUDA：本 artifact 不包含 GPU 测量

## 命令

```text
python scripts/transformer_components_smoke.py \
  --source-root D:\桌面\code \
  --output artifacts/transformer-components/smoke-2026-09-23.json
```

## 原始结果摘要

```text
source_inventory=passed
safe_softmax_mask_and_full_row=passed
safe_softmax_float_dtypes=passed
relu_forward=passed
rmsnorm_unit_rms=passed
mha_shape_and_causal_mask=passed
gqa_shape_and_kv_ratio=passed
kv_cache_prefill_decode_append=passed
kv_cache_reset=passed
pytorch.status=unavailable (WinError 1114 while loading c10.dll)
overall=passed_for_numpy_reference_and_source_inventory
```

具体 JSON 保存在 `artifacts/transformer-components/smoke-2026-09-23.json`。

## 解读

- safe softmax 参考实现把屏蔽位置设为零，fully masked row 的输出保持全零；这是 `softmax.py` 的显式约定，便于后续 value aggregation 不产生 NaN。
- MHA 参考 shape 为 `output=[2,4,8]`、`weights=[2,4,4,4]`；GQA 在 `Hq=4,Hkv=2` 时保持 query/head 输出 shape，但实际模型可以少生成一半的 K/V projection 和 KV cache head。
- cache 参考布局为 `[B,Hkv,Tmax,Dh]`，先追加 3 个 token，再追加 1 个 token，`length=4`；reset 只重置有效长度，不清零预分配存储。
- 以上是 CPU NumPy 参考与 AST 盘点结果，不代表 PyTorch kernel、GPU throughput、HBM 带宽或 serving latency。

## 复现与升级

1. 修复或切换 PyTorch 环境后重新运行同一命令；脚本会自动测试原始六个模块。
2. 在 `raw-sources/` 新增日期版本，记录 `torch.__version__`、CUDA、GPU、dtype、命令和原始 JSON。
3. 用真实 GPU 结果补充 MHA/GQA 的显存、kernel 和 prefill/decode 观察；不要覆盖本文件的环境边界说明。
