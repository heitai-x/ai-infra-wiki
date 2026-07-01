---
title: AI Infra LLM Wiki
type: hub
topic: ai-infra
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [ai-infra, training, inference, serving, rag, llm-wiki]
---

# AI Infra LLM Wiki

这是一个面向 AI Infra 训推系统的本地 LLM Wiki。它不是静态资料夹，而是一个可被 AI 代理持续维护的结构化知识系统：每次阅读、实验、排障、benchmark、代码走查，都应该沉淀为可检索、可追溯、可复用的 Markdown 笔记。

## 快速入口

- 新手从 [[00-index/START-HERE]] 开始。
- 查知识地图看 [[00-index/topic-index]]。
- 查概念看 [[00-index/concept-index]]。
- 查权威资料看 [[00-index/source-index]]。
- 查已有 Codex/AI Infra skills 看 [[00-index/skill-index]]。
- 查框架/硬件/平台实体看 [[00-index/entity-index]]。
- 查学习路线看 [[01-roadmap/90-day-curriculum]]。
- 查 RAG/维护规范看 [[02-llm-wiki-workflow/architecture]]。
- 查本地索引化看 [[02-llm-wiki-workflow/local-indexing]]。
- 查标准 LLM Wiki 对齐看 [[02-llm-wiki-workflow/architecture]]、[[00-index/log]] 和 [[99-maintenance/content-coverage-audit]]。
- 查模板看 [[03-templates/concept-note-template]]、[[03-templates/source-note-template]]、[[03-templates/experiment-note-template]]。
- 查验收记录看 [[99-maintenance/acceptance-audit]]。
- 查原始资料层看仓库根目录 `raw-sources/README.md`。
- 做实验看 [[90-experiments/experiment-ladder]]，重点是 [[90-experiments/torchrun-ddp-fsdp-minimal]] 和 [[90-experiments/vllm-sglang-benchmark-harness]]。
- 遇到线上问题看 [[80-playbooks/serving-capacity-planning]]、[[80-playbooks/nccl-hang-triage]]、[[80-playbooks/profiling-trace-playbook]] 和 [[80-playbooks/serving-production-deployment]]。

## Wiki 设计原则

1. 概念必须能落到系统现象：显存、通信、kernel、调度、吞吐、延迟、SLO。
2. 结论必须能追溯来源：官方文档、论文、代码、实验记录、生产复盘。
3. 每篇笔记必须有 front matter，方便 RAG 过滤和索引。
4. 每个主题至少连接三类页面：概念页、来源页、实验/排障页。
5. 不把“知道名词”当作掌握。掌握的标准是能画图、能估算、能复现、能定位瓶颈。

## 目录分层

```text
00-index/              全局索引、问题库、source/skill/concept 入口
01-roadmap/            学习路线、能力矩阵、skill tree
02-llm-wiki-workflow/  Ingest / Structure / Index / Lint / RAG 维护规范
03-templates/          概念页、来源页、实验页模板
04-entities/           框架、硬件、平台对象页
10-foundations/        GPU、CUDA、内存、NCCL、网络、roofline
20-training-systems/   DDP、FSDP、ZeRO、TP、PP、CP、EP、checkpoint
30-inference-systems/  KV cache、batching、scheduler、量化、投机解码、PD 分离
40-serving-platform/   Kubernetes、Triton、Ray Serve、KServe、SLO、观测性、成本
50-rag-agent-infra/    RAG、向量检索、reranker、agent runtime、反馈闭环
60-frameworks/         PyTorch、DeepSpeed、Megatron、vLLM、SGLang、TensorRT-LLM
70-sources/            官方文档与论文 source cards
80-playbooks/          排障、容量规划、benchmark、事故响应
90-experiments/        可复现实验阶梯
99-maintenance/        backlog、lint、更新策略
```

## 当前版本边界

这是 Wiki v1：已经具备系统性结构、核心概念、主线框架、权威来源、实验路线和 RAG 维护规范。当前已补齐标准 `llm_wiki` 所强调的 raw source 边界、操作日志和更严格的构建输入规则；后续最有价值的增量不是继续堆名词，而是加入真实代码仓库走查、GPU trace、benchmark 原始结果、故障复盘和模型部署配置。
