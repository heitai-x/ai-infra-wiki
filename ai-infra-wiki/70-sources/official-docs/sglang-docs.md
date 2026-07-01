---
title: SGLang Docs
type: source
source_type: official_doc
source_url: https://docs.sglang.io/
topic: inference
component: sglang
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-29
owner: local
reliability: high
tags: [sglang, docs, serving, radix-attention, scheduler]
---

# SGLang Docs

## Why It Matters

SGLang 文档是 radix attention、prefix cache、structured generation、OpenAI-compatible server 和多模型 serving 的官方依据，也是与 vLLM 在 serving 策略上做对比的核心入口。

## Key Claims

- 文档说明 SGLang 提供的 server 启动方式、模型支持、并行选项和 cache 控制。
- 文档解释 radix attention 在 prefix cache 复用和 token-level reuse 上的工作机制。
- 文档覆盖 OpenAI-compatible API 和函数调用、tool use 接口。
- 文档说明 batched generation、structured output、speculative decoding 集成方式。

## Limits Or Caveats

- SGLang 演化快，latest 文档中的行为不应直接当作长期稳定事实。
- 文档是 API 视角，不直接覆盖生产部署的所有运维配置。
- 性能结论必须结合本地 benchmark、server 日志和 trace。

## Links To Concepts

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/prefix-cache-chunked-prefill-preemption]]
- [[30-inference-systems/batching-scheduling]]
- [[60-frameworks/vllm-sglang]]

## Follow Up

- 后续补 SGLang 与 vLLM 在 prefix cache 命中率下的对比笔记。
- 后续补本地导出的 stable 文档快照到 `raw-sources/`。
