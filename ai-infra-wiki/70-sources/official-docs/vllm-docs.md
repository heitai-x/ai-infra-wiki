---
title: vLLM Docs
type: source
source_type: official_doc
source_url: https://docs.vllm.ai/en/stable/
topic: inference
component: vllm
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [vllm, docs, serving, paged-attention, scheduler]
---

# vLLM Docs

## Why It Matters

vLLM 文档是 PagedAttention、KV cache、continuous batching 和 OpenAI-compatible serving 的核心官方入口，也是很多 LLM serving 配置参数的第一手来源。

## Key Claims

- stable docs 覆盖部署、引擎参数、并行方式、OpenAI-compatible server 和 benchmark 使用方式。
- latest docs 适合跟踪 fast-moving 变更，但稳定结论应优先引用 stable。
- vLLM 文档是 KV cache、scheduler 和 serving 参数语义的重要官方依据。

## Limits Or Caveats

- vLLM 演化较快，latest 文档中的行为不应直接当作长期稳定事实。
- 配置参数的真实效果依赖模型、GPU、并发 workload 和服务模式。
- 性能判断必须结合本地 benchmark、server 日志和 trace。

## Links To Concepts

- [[30-inference-systems/kv-cache-paged-attention]]
- [[30-inference-systems/batching-scheduling]]
- [[30-inference-systems/llm-serving-map]]
- [[60-frameworks/vllm-sglang]]

## Follow Up

- 后续补常用 serving 参数与指标字段速查表。
- 后续补本地导出的 stable 文档快照到 `raw-sources/`。
