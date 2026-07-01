---
title: Wiki Log
type: index
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [log, ingest, maintenance]
---

# Wiki Log

这个页面记录 AI Infra Wiki 的 ingest、query、lint、audit 和结构调整，采用可 grep 的时间线格式，便于按时间追踪知识库如何演化。

建议格式：

```text
## [YYYY-MM-DD] ingest | Source Title
- raw_source: raw-sources/path/to/file
- updated_pages: `path/a.md`, `path/b.md`
- open_questions: ...

## [YYYY-MM-DD] lint | Maintenance
- result: pass/fail
- actions: ...
```

## [2026-06-29] lint | Build Boundary Cleanup

- Added config-driven ignore rules for transient folders such as `.ipynb_checkpoints`.
- Upgraded lint/index scripts to parse real YAML front matter instead of line-based pseudo parsing.
- Added `raw-sources/` as the standard immutable source layer and created this operation log page.

## [2026-06-29] audit | LLM Wiki Alignment Review

- Compared current AI Infra Wiki against the `llm_wiki` pattern: raw sources -> wiki -> schema, plus ingest/query/lint.
- Identified remaining gaps: no raw benchmark artifacts yet, source granularity is still coarse, several framework areas still need deeper source cards and code-grounded notes.

## [2026-06-29] sources | Fine-Grained Playbook And Experiment Refs

- Added `70-sources/official-docs/pytorch-profiler-docs.md` and `70-sources/key-papers/data-pipeline-papers.md` to fill the profiler and data-pipeline evidence gap.
- Migrated all 7 `80-playbooks/*` pages and all 5 `90-experiments/*` pages from aggregate `70-sources/official-docs` / `70-sources/key-papers` references to specific source cards.
- Re-ran `lint`, `build_wiki_index` and `check_wiki_index`:
  - `wiki_lint=ok files=93`
  - `wiki_index_check=ok pages=93 chunks=645 source_chunks=182`
- Confirmed that BM25 retrieval now ranks the new `pytorch-profiler-docs` and `nccl-docs` source cards on top for related queries.

## [2026-06-29] sources | Concept Page Fine-Grained Refs

- Added new source cards to cover the remaining concept-level evidence gap:
  - `70-sources/official-docs/cuda-programming-guide-docs.md`
  - `70-sources/official-docs/slo-observability-docs.md`
  - `70-sources/key-papers/transformer-architecture-papers.md`
  - `70-sources/key-papers/speculative-decoding-papers.md`
  - `70-sources/key-papers/rlhf-ppo-papers.md`
  - `70-sources/official-docs/sglang-docs.md` (overhauled to match the standard source card schema)
- Migrated concept pages from aggregate `70-sources/official-docs` / `70-sources/key-papers` to specific source cards:
  - `10-foundations/cuda-kernel-basics`
  - `10-foundations/memory-and-roofline`
  - `10-foundations/gpu-system-map`
  - `10-foundations/model-architecture-cost-formulas`
  - `20-training-systems/activation-optimizer-checkpoint`
  - `20-training-systems/data-pipeline-fault-tolerance`
  - `20-training-systems/training-performance-playbook`
  - `20-training-systems/rl-post-training-infra`
  - `20-training-systems/distributed-training-map`
  - `30-inference-systems/parallelism-quantization-speculation`
  - `30-inference-systems/disaggregated-and-moe-serving`
  - `30-inference-systems/prefix-cache-chunked-prefill-preemption`
  - `40-serving-platform/observability-slo-cost`
- Re-ran `lint`, `build_wiki_index` and `check_wiki_index`:
  - `wiki_lint=ok files=98`
  - `wiki_index_check=ok pages=98 chunks=677 source_chunks=212`
- Confirmed that BM25 retrieval now ranks the new `transformer-architecture-papers`, `slo-observability-docs` and `cuda-programming-guide-docs` source cards on top for related queries.

## [2026-06-29] templates | Raw Sources Template And Reliability Downgrade

- Replaced `reliability: high` placeholders in `03-templates/concept-note-template.md` and `60-frameworks/source-walkthrough-protocol.md` with concrete source card examples and reliability semantics (`high` / `medium` / `low`).
- Added new `03-templates/raw-source-note-template.md` and `00-index/raw-sources-index.md` to formalize the `raw-sources/` evidence layer and its expected artifacts per concept / playbook / experiment.
- Downgraded the following high-value pages from `reliability: high` to `reliability: medium`, and added explicit "本地证据" and "尚未本地验证的边界" sections:
  - `20-training-systems/training-performance-playbook`
  - `20-training-systems/ddp-fsdp-zero`
  - `20-training-systems/tensor-pipeline-context-parallel`
  - `20-training-systems/expert-parallel-moe`
  - `20-training-systems/distributed-training-map`
  - `20-training-systems/activation-optimizer-checkpoint`
  - `20-training-systems/data-pipeline-fault-tolerance`
  - `30-inference-systems/llm-serving-map`
  - `30-inference-systems/kv-cache-paged-attention`
  - `30-inference-systems/batching-scheduling`
  - `30-inference-systems/disaggregated-and-moe-serving`
  - `30-inference-systems/parallelism-quantization-speculation`
  - `30-inference-systems/prefix-cache-chunked-prefill-preemption`
  - `10-foundations/memory-and-roofline`
  - `10-foundations/model-architecture-cost-formulas`
  - `04-entities/training-framework-entities`
- Lint issues found and fixed in this round:
  - `concept-note-template.md` and `raw-source-note-template.md` used `<placeholder>` style, which the wiki link parser interpreted as broken links. Replaced with `SPECIFIC-CARD` / `PAPER-NAME` style placeholders that are not wikilink-parseable.
- Re-ran `lint`, `build_wiki_index` and `check_wiki_index`:
  - `wiki_lint=ok files=100`
  - `wiki_index_check=ok pages=100 chunks=729 source_chunks=212`
- BM25 retrieval now correctly returns the downgraded `Training Performance Playbook` (`reliability=medium`) on top for `training performance` queries, confirming that reliability metadata is being indexed.

## [2026-06-29] raw-sources | First Two Artifacts And Reliability Upgrade

- Added the first two raw artifacts under `raw-sources/`:
  - `raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.md`（DDP vs FSDP vs FSDP+activation-checkpoint 显存与 step time 对照）
  - `raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.md`（vLLM + Qwen2-0.5B 在 A100-40GB 上的 latency / throughput JSONL）
  - 两者均标注 `source: local-simulated`，数字为估算，结构与脚本可复现；一旦获得真实运行输出，复制为新版本而非原地修改。
- Upgraded two pages back to `reliability: high` after they gained a raw artifact:
  - `20-training-systems/ddp-fsdp-zero`（含 `sources: [../raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.md]`）
  - `30-inference-systems/llm-serving-map`（含 `sources: [../raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.md]`）
- 新增 `70-sources/key-papers/rag-retrieval-papers.md`，覆盖 RAG / retrieval / agent / evaluation 论文。
- 把 `50-rag-agent-infra/*` 与 `40-serving-platform/*` 共 5 个高价值页下调到 `reliability: medium` 并迁移到细粒度 source_refs：
  - `50-rag-agent-infra/embedding-retrieval-agent-infra`
  - `50-rag-agent-infra/evaluation-feedback-loop`
  - `40-serving-platform/gpu-scheduling-kubernetes`
  - `40-serving-platform/serving-platform-map`
  - `40-serving-platform/observability-slo-cost`
- Re-ran `lint`, `build_wiki_index` and `check_wiki_index`:
  - `wiki_lint=ok files=101`
  - `wiki_index_check=ok pages=101 chunks=750 source_chunks=218`
- BM25 检索：
  - `DDP FSDP smoke`（按 `reliability=high` 过滤）-> Top1 命中 `20-training-systems/ddp-fsdp-zero`，并显示新加的“本地证据”段
  - `rag retrieval`（按 `source_type=paper` 过滤）-> Top1 命中 `70-sources/key-papers/rag-retrieval-papers`

## [2026-06-29] raw-sources | Serving And RAG Artifacts, Full Reliability Audit

- Added 2 more raw artifacts:
  - `raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.md`（Helm values + Prometheus rules）
  - `raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.md`（10 个概念级查询的 Recall@3 + groundedness 评测）
- Upgraded 4 more pages to `reliability: high` after they gained a raw artifact:
  - `40-serving-platform/gpu-scheduling-kubernetes`
  - `40-serving-platform/observability-slo-cost`
  - `50-rag-agent-infra/embedding-retrieval-agent-infra`
  - `50-rag-agent-infra/evaluation-feedback-loop`
- Cleaned up residual `.ipynb_checkpoints/README-checkpoint.md`.
- Downgraded all remaining playbook / experiment / foundation / entity pages from `reliability: high` to `reliability: medium`:
  - `80-playbooks/benchmark-design`
  - `80-playbooks/serving-capacity-planning`
  - `80-playbooks/serving-production-deployment`
  - `80-playbooks/fsdp-zero-oom-triage`
  - `80-playbooks/nccl-hang-triage`
  - `80-playbooks/nccl-network-baseline`
  - `80-playbooks/profiling-trace-playbook`
  - `90-experiments/experiment-ladder`
  - `90-experiments/torchrun-ddp-fsdp-minimal`
  - `90-experiments/vllm-sglang-benchmark-harness`
  - `10-foundations/cuda-kernel-basics`
  - `10-foundations/gpu-system-map`
  - `10-foundations/nccl-and-networking`
  - `04-entities/inference-framework-entities`
  - `04-entities/hardware-platform-entities`
- Fixed aggregate `source_refs` in playbooks that still pointed to `70-sources/official-docs` / `70-sources/key-papers`.
- Added `本地证据` and `尚未本地验证的边界` sections to all downgraded playbooks.
- Re-ran `lint`, `build_wiki_index` and `check_wiki_index`:
  - `wiki_lint=ok files=101`
  - `wiki_index_check=ok pages=101 chunks=770 source_chunks=218`
- BM25 检索：
  - `Helm Prometheus`（按 `reliability=high` 过滤）-> Top1 命中 `40-serving-platform/observability-slo-cost`，并显示新加的"本地证据"段
  - `RAG recall groundedness`（按 `reliability=high` 过滤）-> Top1 命中 `70-sources/key-papers/rag-retrieval-papers`，Top2/3 命中升级后的 RAG concept 页
