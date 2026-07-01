---
title: Disaggregated And MoE Serving
type: concept
topic: inference
component: advanced-serving
level: advanced
status: active
last_updated: 2026-06-13
owner: local
reliability: medium
tags: [disaggregated-serving, prefill-decode, moe, serving]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
---

# Disaggregated And MoE Serving

## 一句话

Disaggregated serving 把 prefill 和 decode 放到不同资源池，以匹配两者不同的计算/内存特性；MoE serving 则要处理 expert routing、热点、all-to-all 和多租户负载不均。

## 为什么拆 prefill / decode

Prefill：

- prompt 长时计算量大。
- 对并行计算和 attention kernel 要求高。
- 产生 KV cache。

Decode：

- 每轮生成少量 token。
- 反复读权重和 KV cache。
- 对 latency 和 memory bandwidth 更敏感。

如果把两者混在同一批 GPU 上，长 prompt 可能阻塞 decode，decode 也可能让 prefill 资源利用不足。

## PD 分离挑战

- KV cache 如何从 prefill worker 传给 decode worker。
- 网络传输是否抵消收益。
- scheduler 如何决定路由和迁移。
- prefix cache 和 KV ownership 如何管理。
- 故障时请求状态如何恢复。

## MoE serving 挑战

- 请求 token 的 expert 分布不均。
- 热门 expert 成为瓶颈。
- all-to-all 和网络拓扑影响 latency。
- 是否复制热门 expert 需要成本/收益评估。
- admission control 需要考虑 expert capacity，而不只是 GPU memory。

## 适用场景

PD 分离更适合：

- prompt 很长、output 较短或 mix 很复杂。
- prefill 和 decode 资源需求明显不同。
- 有足够网络带宽和工程能力。

MoE serving 更适合：

- 参数量巨大但每 token 激活稀疏。
- 能接受 routing 和平台复杂度。

## 本地证据

- 暂无 `raw-sources/` 下的 PD 分离部署 YAML、KvCache 传输延迟、MoE 专家分布样本。
- 章节中 PD 分离动机、挑战与适用场景属于对 vLLM / SGLang / TensorRT-LLM 文档 + DistServe / GShard / Switch Transformer 论文的总结，尚未用本机数据验证。
- 升级到 `reliability: high` 的最小条件：补 1 份 `raw-sources/inference/pd-separate-<commit>.md` + 1 份 `raw-sources/inference/moe-serving-<commit>.md`，含网络拓扑、KV 传输延迟、expert 分布与排队数据。

## 尚未本地验证的边界

- “PD 分离在长 prompt / mix 复杂时收益更明显”是经验结论，没有具体收益数字。
- 热门 expert 是否值得 replicate 的判断标准是平台策略，不等于实际收益。
- 故障时请求状态如何恢复的方案依赖 runtime 实现，本页未引用具体实现。

## 来源

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/tensorrt-llm-docs]]
- [[70-sources/key-papers/distserve-paper]]
- [[70-sources/key-papers/gshard-paper]]
- [[70-sources/key-papers/switch-transformer-paper]]

## 相关页面

- [[30-inference-systems/llm-serving-map]]
- [[20-training-systems/expert-parallel-moe]]
- [[40-serving-platform/serving-platform-map]]
