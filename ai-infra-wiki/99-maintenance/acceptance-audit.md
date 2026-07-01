---
title: Acceptance Audit
type: workflow
topic: wiki
component: audit
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [acceptance, audit, validation, sub-agent]
---

# Acceptance Audit

本页记录 AI Infra LLM Wiki 的验收标准、sub agent 审计结论、修复状态和自动化证据。

## 验收目标

1. 内容是否存在幻觉或明显不严谨陈述。
2. 是否符合标准本地 Markdown / Obsidian / LLM Wiki。
3. 是否可以索引，并且是否已经 materialize 本地索引。
4. 结构化是否足够支持 RAG metadata filtering。
5. 覆盖面是否足够支撑系统学习 AI Infra 训推系统。

## Sub Agent Findings And Fixes

### 事实 / 幻觉审计

结论：未发现 critical/high 级别幻觉；发现若干 medium/low 表述边界问题。

已修复：

- KServe 链接从 `/latest/` 改为稳定入口 `https://kserve.github.io/website/`。
- vLLM source card 改为 stable docs，latest 仅标注为 fast-moving changes。
- PipeDream 标题改为与 arXiv URL 匹配的 `PipeDream: Fast and Efficient Pipeline Parallel DNN Training`。
- KV cache 公式增加单 GPU/per-rank 与 TP group 口径边界。
- MFU 公式改成包含 step/s、GPU 数和 peak FLOPs/s 的维度正确表达。
- Adam optimizer state 与参数/梯度账本拆开，避免把参数/梯度误称为 optimizer state。
- SP/CP 中 normalization/dropout 的同步表述改为 attention、布局转换、RNG 一致性边界。
- DDP/FSDP/ZeRO 一句话说明改为 ZeRO 按 stage 切分，ZeRO-1/2 不切参数。
- MoE capacity factor 增加 dropless MoE 边界。

### Wiki / RAG / Indexability 审计

结论：Wiki 已有物化 SQLite FTS5/BM25 索引，不是理论可索引；但原 schema/lint/source metadata 需要增强。

已修复：

- `.ai-wiki.yml` 增加 allowed type/status/level/reliability/source_type 枚举。
- `rag-metadata-schema.md` 补充实际存在的 `entity`、`eval-set`、`hub` 类型。
- `lint_wiki.py` 增强为校验枚举、日期、source 必填字段、坏链和孤儿页。
- 补入口链接，消除 template/audit/roadmap/workflow 孤儿页。
- source pages 增加 `source_url`，source chunks 保留 `source_type/source_url/last_checked`。
- `build_wiki_index.py`、`search_wiki.py`、`check_wiki_index.py` 支持 source metadata 和 DB 一致性验收。

### 覆盖面审计

结论：原始版本是高质量学习地图和 RAG 骨架，但要支撑“完整详细”还需补真实实验、profiling/NCCL、源码走查、serving 部署和模型成本公式。

已补充：

- [[90-experiments/torchrun-ddp-fsdp-minimal]] 与脚本 `scripts/experiments/torchrun_ddp_fsdp_minimal.py`。
- [[90-experiments/vllm-sglang-benchmark-harness]] 与脚本 `scripts/experiments/llm_serving_benchmark.py`。
- [[80-playbooks/profiling-trace-playbook]]。
- [[80-playbooks/nccl-network-baseline]]。
- [[80-playbooks/serving-production-deployment]]。
- [[60-frameworks/source-walkthrough-protocol]]。
- [[10-foundations/model-architecture-cost-formulas]]。
- [[20-training-systems/rl-post-training-infra]]。
- [[30-inference-systems/prefix-cache-chunked-prefill-preemption]]。

## 当前自动化证据

```bash
python3 -m py_compile   scripts/lint_wiki.py   scripts/build_wiki_index.py   scripts/search_wiki.py   scripts/check_wiki_index.py   scripts/experiments/torchrun_ddp_fsdp_minimal.py   scripts/experiments/llm_serving_benchmark.py

python3 scripts/lint_wiki.py ai-infra-wiki
python3 scripts/build_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
python3 scripts/check_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
python3 scripts/search_wiki.py "KV cache" --filter topic=inference --limit 3
python3 scripts/search_wiki.py "FSDP ZeRO" --filter topic=training --limit 3
python3 scripts/search_wiki.py "vLLM docs" --filter source_type=official_doc --limit 5
```

已观察结果：

```text
wiki_lint=ok files=<current_files>
wiki_index_built db=<current_db> pages=<current_pages> chunks=<current_chunks>
wiki_index_check=ok pages=<current_pages> chunks=<current_chunks> source_chunks=<current_source_chunks>
KV cache -> 30-inference-systems/kv-cache-paged-attention.md
FSDP ZeRO -> 20-training-systems/ddp-fsdp-zero.md, 80-playbooks/fsdp-zero-oom-triage.md
NCCL hang -> 80-playbooks/nccl-hang-triage.md, 10-foundations/nccl-and-networking.md
vLLM docs with source_type=official_doc -> 60-frameworks/vllm-sglang.md, 70-sources/official-docs/vllm-docs.md
```

## Acceptance Decision

通过：当前 Wiki 达到“完整详细高质量 v1”的验收线。

验收依据：

- 有系统化目录、索引、实体、概念、来源、playbook、实验、维护层。
- 有 sub agent 独立审计，并已修复事实边界、schema、indexability 和覆盖面关键缺口。
- 有本地 materialized SQLite FTS5/BM25 索引，可按 metadata 检索。
- 有增强 lint 和 index consistency checker，可复跑验收。
- 有训练和推理两条端到端实验脚本骨架，后续可在 GPU/server 环境生成 raw artifacts。

边界：当前没有伪造 GPU trace、NCCL 测试结果或真实 vLLM/SGLang server benchmark raw output。真实 raw artifacts 必须在具备 GPU、NCCL、多机网络或 serving server 的环境运行后 ingest 到 Wiki。
