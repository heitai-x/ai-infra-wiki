---
title: Transformer Components Smoke Experiment
type: experiment
topic: inference
component: transformer-components
level: beginner
status: active
last_updated: 2026-09-23
owner: local
reliability: medium
tags: [experiment, transformer, softmax, rmsnorm, mha, gqa, kv-cache]
source_refs:
  - 70-sources/key-papers/transformer-architecture-papers
  - 70-sources/key-papers/pagedattention-paper
  - 70-sources/official-docs/vllm-docs
sources:
  - ../raw-sources/inference/transformer-components-smoke-2026-09-23.md
---

# Transformer Components Smoke Experiment

## Question

六个小型组件能否在 CPU 参考路径上验证 mask、数值、shape、head mapping 和 KV cache 状态变化，并把结果连接到后续 GPU/serving 实验？

## Environment

- Python：3.11.7
- NumPy：1.26.4
- 主机：Windows CPU
- 源码：`D:\桌面\code\softmax.py`、`ReLu.py`、`RMSNorm.py`、`MHA.py`、`GQA.py`、`kvcache.py`
- PyTorch：本机安装版本为 2.13.0，但导入时 `c10.dll` 触发 `WinError 1114`
- GPU / CUDA：本实验没有 GPU 测量

## Commands

```text
python scripts/transformer_components_smoke.py \
  --source-root D:\桌面\code \
  --output artifacts/transformer-components/smoke-2026-09-23.json
```

## Inputs and expected shapes

| Check | Input | Expected observation |
|---|---|---|
| safe softmax | scores `[2,3]`、部分 mask、全 mask row | 有效 row 和为 1；无效位置和全 mask row 为零；结果有限 |
| ReLU | `[1,3]`，含负、零、正值 | 输出 `[1,3]`，负值变零，dtype 保持 |
| RMSNorm | fp16 `[1,2]` | 输出 shape 不变；RMS 接近 1；统计量参考 fp32 |
| MHA | `X=[2,4,8]`、`H=4` | output `[2,4,8]`，weights `[2,4,4,4]`，未来位置为零 |
| GQA | `X=[2,4,8]`、`Hq=4,Hkv=2` | output shape 与 MHA 相同，KV group ratio 为 2:1 |
| KV cache | cache `[2,2,5,2]`；append 3 + 1 token | get shape `[2,2,4,2]`，reset 后 length=0 |

## Raw Artifacts

- JSON：`artifacts/transformer-components/smoke-2026-09-23.json`
- 说明：`raw-sources/inference/transformer-components-smoke-2026-09-23.md`
- 源码盘点：`artifacts/transformer-components/source-inventory-2026-09-23.md`

## Result summary

```text
NumPy/reference checks: 9 passed
AST source inventory: 6 files / all expected definitions passed
PyTorch runtime checks: skipped because c10.dll could not load
```

## Interpretation

- 数值层：safe softmax 的减最大值、mask 清零和全 mask 约定可以独立验证。
- shape 层：MHA/GQA 的 query head 输出 shape 相同；GQA 的 `Hkv` 变化主要反映在 K/V projection、KV cache 和读取量。
- 状态层：连续 cache 的 `length` 单调追加、`get()` 只暴露有效 prefix、`reset()` 复用预分配存储。
- 证据边界：这是 NumPy 参考和 AST 盘点，不包含 PyTorch kernel、GPU HBM 带宽、CUDA graph 或 serving latency。

## Next experiment

1. 在可导入 PyTorch 的环境中复跑同一命令，比较参考输出与 `softmax.py`、`RMSNorm.py`、`MHA.py`、`GQA.py`、`kvcache.py` 的实际输出。
2. 增加 `B=1/4`、`T=1/128/2048`、fp32/fp16/bf16 的 shape 和有限性矩阵。
3. 将连续 cache 改造成 ragged/paged reference，记录 block size、free blocks、admission 和 TTFT/TPOT 的关系。

## 相关页面

- [[10-foundations/attention-masks-and-softmax]]
- [[10-foundations/normalization-and-activation]]
- [[30-inference-systems/mha-gqa-attention]]
- [[30-inference-systems/kv-cache-compute-path]]
- [[90-experiments/experiment-ladder]]
