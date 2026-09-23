---
title: AI Infra LLM Wiki
type: hub
topic: ai-infra
level: all
status: active
last_updated: 2026-09-23
owner: local
reliability: high
tags: [ai-infra, training, inference, serving, rag, llm-wiki]
---

# AI Infra LLM Wiki

这是面向 AI Infra 训推系统的本地知识与实践系统。它将概念、来源、实验、排障、benchmark 和代码走查沉淀为可检索、可追溯、可复用的 Markdown 页面，并通过 bundle、Prompt、Checklist 和 Checkpoint 组织渐进式学习。

## 快速入口

- 新手从 [[00-index/START-HERE]] 开始。
- 查知识地图看 [[00-index/topic-index]]。
- 查概念看 [[00-index/concept-index]]。
- 查权威资料看 [[00-index/source-index]]。
- 查 raw artifact 落地图看 [[00-index/raw-sources-index]]。
- 查问题库看 [[00-index/question-bank]]。
- 查框架、硬件和平台实体看 [[00-index/entity-index]]。
- 查可用 skills 看 [[00-index/skill-index]]。
- 查学习路线看 [[01-roadmap/90-day-curriculum]]。
- 查能力矩阵看 [[01-roadmap/competency-matrix]]。
- 查 RAG 和维护规范看 [[02-llm-wiki-workflow/architecture]]。
- 查渐进式加载看 [[02-llm-wiki-workflow/progressive-loading]]。
- 查本地索引看 [[02-llm-wiki-workflow/local-indexing]]。
- 查模板看 [[03-templates/concept-note-template]]、[[03-templates/source-note-template]]、[[03-templates/experiment-note-template]]。
- 查验收记录看 [[99-maintenance/acceptance-audit]]。
- 查仓库缺口与优化方案看 [[99-maintenance/current-repository-gaps]]、[[99-maintenance/optimization-plan]]。
- 查原始资料层看仓库根目录 `raw-sources/README.md`。
- 做实验看 [[90-experiments/experiment-ladder]]。
- 遇到线上问题看 [[80-playbooks/serving-capacity-planning]]、[[80-playbooks/nccl-hang-triage]]、[[80-playbooks/profiling-trace-playbook]] 和 [[80-playbooks/serving-production-deployment]]。

## 学习闭环

```text
选择主题 bundle
  -> bootstrap / map
  -> core 概念和公式
  -> practice 代码、实验或 playbook
  -> deep_dive 来源和源码
  -> verify checklist、问题库和 evidence
  -> checkpoint 保存下一步
```

项目根目录提供：

- `packs/`：渐进加载 bundle；
- `prompts/`：学习、实验和 checkpoint Prompt；
- `tools/manifest.yml`：工具能力清单；
- `checklists/`：主题验收标准；
- `checkpoints/`：学习状态模板和记录。

## Wiki 设计原则

1. 概念落到系统现象：显存、通信、kernel、调度、吞吐、延迟和 SLO。
2. 结论连接来源：官方文档、论文、代码、实验记录和生产复盘。
3. 每篇笔记使用 front matter，支持 RAG 过滤和索引。
4. 每个主题连接概念页、来源页和实验或排障页。
5. 掌握标准是能画图、能估算、能运行、能复现和能定位瓶颈。
6. 页面直接描述机制、条件、结果和边界；学习状态通过 Checklist 与 Checkpoint 记录。

## 目录分层

```text
00-index/              全局索引、问题库、source/skill/concept 入口
01-roadmap/            学习路线、能力矩阵、skill tree
02-llm-wiki-workflow/  Ingest / Structure / Index / Lint / RAG / Loading 规范
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
99-maintenance/        backlog、lint、审计和更新策略
```

## 索引与维护

Wiki 使用 SQLite FTS5/BM25 进行本地关键词检索，页面 metadata 支持 `topic`、`component`、`level`、`status`、`reliability` 和 `source_type` 过滤。

常用命令：

```bash
python scripts/lint_wiki.py ai-infra-wiki
python scripts/build_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
python scripts/check_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
```

当前 Wiki 已通过 front matter、wikilink、metadata、孤儿页和索引一致性检查。真实 GPU trace、serving benchmark、NCCL 输出和部署配置通过 `raw-sources/` 版本化沉淀。
