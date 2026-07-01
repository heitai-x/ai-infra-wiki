---
title: Backlog
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [backlog, maintenance]
---

# Backlog

## 高优先级

- 为每个 source card 增加更细的版本号和章节定位。
- 已加入真实 `torchrun` DDP/FSDP 最小实验脚本；后续补 GPU raw artifacts。
- 已加入 OpenAI-compatible vLLM/SGLang benchmark harness；后续补真实 server raw artifacts。
- 已增强 `scripts/lint_wiki.py`：检查 front matter、wikilinks、枚举、日期、source_url、last_checked、孤儿页。
- 把聚合 source card 逐步拆细到框架/论文/版本级别，并补页面级来源追踪。
- 增加 MkDocs 或 Docusaurus 配置，生成可浏览站点。

## 中优先级

- 补充 Transformer architecture、attention、MLP、RMSNorm、RoPE 的模型结构页。
- 补充 RL post-training、SLIME、GRPO、PPO 的训练系统页。
- 补充 Ray Train、TorchTitan、NeMo、Colossal-AI 等框架 source cards。
- 补充 Nsight Systems / Nsight Compute 使用 playbook。
- 补充 CUDA Graph、torch.compile、Triton kernel fusion 概念页。

## 低优先级

- 加入 Obsidian graph view 优化标签。
- 加入 Mermaid 架构图版本。
- 建立自动 source freshness checker。

## 维护原则

- 先补真实实验和证据，再补更多名词。
- 新增框架页必须连接到训练/推理概念页。
- 新增性能结论必须有 benchmark 原始输出。
- 每月复查官方文档链接和过期 API。
