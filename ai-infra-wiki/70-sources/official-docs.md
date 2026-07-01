---
title: Official Docs Source Map
type: source
source_type: curated
source_url: https://mlsysbook.ai/
topic: ai-infra
level: all
status: active
last_updated: 2026-06-29
last_checked: 2026-06-13
owner: local
reliability: high
tags: [sources, official-docs, curated]
---

# Official Docs Source Map

这是 AI Infra 官方资料的导航页。讨论具体 API、配置、命令、行为边界时，优先引用下面的细粒度 source card，而不是只引用本页。

## Training

- [[70-sources/official-docs/mlsys-book-docs]]
- [[70-sources/official-docs/pytorch-distributed-docs]]
- [[70-sources/official-docs/deepspeed-docs]]
- [[70-sources/official-docs/megatron-core-docs]]
- [[70-sources/official-docs/nccl-docs]]

## Inference And Serving

- [[70-sources/official-docs/vllm-docs]]
- [[70-sources/official-docs/sglang-docs]]
- [[70-sources/official-docs/tensorrt-llm-docs]]
- [[70-sources/official-docs/triton-inference-server-docs]]
- [[70-sources/official-docs/ray-serve-docs]]
- [[70-sources/official-docs/kserve-docs]]
- [[70-sources/official-docs/nvidia-k8s-device-plugin-docs]]

## Why This Map Exists

- 把原本聚合在一起的官方资料拆成页面级来源，方便 concept/playbook 精确引用。
- 保留一个总导航入口，便于快速浏览某个主题下有哪些一手官方资料。
- 后续仍可继续补章节定位、版本号和本地 `raw-sources/` 快照路径。

## Usage Notes

- 讨论 API、配置、命令或支持矩阵时，优先引用细粒度官方来源页。
- 当多个官方来源都相关时，再把本页当作导航入口引用。
- 后续继续为 fast-moving 文档补版本/章节定位，并把关键页面导出到 `raw-sources/`。
