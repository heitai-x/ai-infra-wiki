---
title: Skill Index
type: index
topic: ai-infra
level: intermediate
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [skills, codex, tools]
---

# Skill Index

本页记录当前环境可用于 AI Infra 学习和实践的 Codex skills。它们不是课程本身，而是把 Wiki 知识落到真实任务的执行工具。

## Serving / Benchmark

- `llm-serving-auto-benchmark`：在 SGLang、vLLM、TensorRT-LLM 等框架之间做公平部署和 benchmark。
- `llm-serving-capacity-planner`：解析 serving 启动日志，估算 KV cache、静态显存、最大并发。
- `sglang-sota-humanize-loop`：围绕 SGLang 做 benchmark、profile、patch、revalidate 的性能闭环。
- `vllm-sota-humanize-loop`：围绕 vLLM 做同类性能闭环。

## Profiling / Kernel / Compute

- `llm-torch-profiler-analysis`：分析 torch profiler trace，输出 kernel、overlap、fusion 表。
- `llm-pipeline-analysis`：分析 forward pass、layer timing、kernel 边界和 Perfetto 时间段。
- `model-compute-simulation`：从 operator 级别估算 FLOPs、MFU、并行策略影响。
- `tilelang-developer`：开发和优化 GPU kernel，包括 GEMM、attention、MLA 等。

## Training / Memory

- `megatron-memory-estimator`：估算 Megatron dense/MoE 训练显存和并行策略。
- `slime-user`：SLIME RL post-training 框架使用、配置和排障。

## Architecture / Diagrams

- `hf-architecture-tikz`：为 HuggingFace decoder-only LLM 生成 TikZ 架构图和参数公式。
- `model-architecture-diagram`：查找公开模型架构图或结构链接。

## 使用建议

- 学概念时先读 Wiki，再调用 skill 做实验。
- 做性能结论时必须保留 skill 运行输入、版本、命令和原始输出。
- 排障时先写 playbook 记录假设，再用 skill 收集证据，最后把复盘沉淀回 Wiki。
