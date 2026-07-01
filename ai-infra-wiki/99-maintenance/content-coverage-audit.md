---
title: Content Coverage Audit
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [audit, coverage, hallucination, llm-wiki]
---

# Content Coverage Audit

这份审计页专门回答两个问题：

1. 当前 AI Infra Wiki 是否已经足够详细明确。
2. 哪些地方仍然存在“高层骨架多、原始证据少”的幻觉风险。

## 总体结论

- 作为学习型 AI Infra Wiki，当前内容已经形成较完整的训练、推理、平台、RAG 和实验骨架。
- 作为“可直接支撑生产决策”的知识库，细节仍不够充分，尤其缺真实 benchmark、trace、配置和源码级证据。
- 当前最主要的风险不是明显事实错误，而是把“高层总结”误读成“已被本地证据验证的操作结论”。

## 结构层面的风险

- `70-sources/official-docs.md` 和 `70-sources/key-papers.md` 仍保留为导航页；虽然已经拆出一批页面级 source card，但仍有不少 concept/playbook 没完成细粒度迁移。
  - 进度（2026-06-29）：7 个 `80-playbooks/*` 和 5 个 `90-experiments/*` 已全部迁到具体 source card。
- 多数 concept 页仍缺少页面级 `sources` 到 `raw-sources/` 的追踪，当前主要做到 wiki 内 source card 细化，而非 raw artifact 级证据闭环。
- 还没有把真实 `raw-sources/` benchmark 输出、profiler trace、部署 YAML、运行日志批量沉淀进来。
- `99-maintenance/acceptance-audit.md` 的整体结论偏乐观，应与本页一起阅读，避免把 v1 骨架等同于证据充分。

## 内容层面的缺口

- 训练系统页已覆盖 DDP/FSDP/ZeRO、TP/PP/CP、MoE，但对 Megatron-Core、TorchTitan、NeMo、Ray Train 的源码入口和版本差异仍不够细。
- 推理系统页已覆盖 KV cache、batching、prefill/decode、disaggregation，但对 scheduler policy、admission control、prefix cache 失效条件的配置级细节仍偏少。
- 服务平台页说明了控制面/数据面，但还缺真实生产部署清单，例如 Helm values、KServe/Triton rollout、GPU 拓扑约束、告警阈值样例。
- RAG/Agent Infra 页讲清了 pipeline，但尚未给出真实评测集、召回指标、失败样例和回归流程结果。

## 优先补强建议

1. 在已经拆出的 vLLM、SGLang、PyTorch Distributed、Megatron-Core、ZeRO、PagedAttention 等 source card 基础上，继续补版本、章节、命令或源码路径。
2. 将真实实验原始输出落到 `raw-sources/`，再从 source card 链接到概念页和 playbook。
3. 为关键高可靠页面补“证据块”：硬件、模型、软件版本、命令、输出摘要、适用边界。
4. 对 `reliability: high` 的页面做二次复核，优先下调缺乏代码或实验支撑的页面，避免过度自信。

## 拆分迁移清单（2026-06-29）

- 新增 source cards：
  - `70-sources/official-docs/pytorch-profiler-docs.md`
  - `70-sources/key-papers/data-pipeline-papers.md`
- 迁移到细粒度 `source_refs` 的页面：
  - `80-playbooks/nccl-hang-triage`
  - `80-playbooks/nccl-network-baseline`
  - `80-playbooks/profiling-trace-playbook`
  - `80-playbooks/benchmark-design`
  - `80-playbooks/serving-production-deployment`
  - `80-playbooks/serving-capacity-planning`
  - `80-playbooks/fsdp-zero-oom-triage`
  - `90-experiments/torchrun-ddp-fsdp-minimal`
  - `90-experiments/single-node-training`
  - `90-experiments/llm-serving-benchmark`
  - `90-experiments/vllm-sglang-benchmark-harness`
  - `90-experiments/experiment-ladder`

## 概念页迁移（2026-06-29）

- 新增 source cards：
  - `70-sources/official-docs/cuda-programming-guide-docs.md`
  - `70-sources/official-docs/slo-observability-docs.md`
  - `70-sources/key-papers/transformer-architecture-papers.md`
  - `70-sources/key-papers/speculative-decoding-papers.md`
  - `70-sources/key-papers/rlhf-ppo-papers.md`
  - `70-sources/official-docs/sglang-docs.md`（按标准 source card schema 覆写）
- 迁移到细粒度 `source_refs` 的概念页：
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

## 验证（2026-06-29）

- `wiki_lint=ok files=98`
- `wiki_index_check=ok pages=98 chunks=677 source_chunks=212`
- BM25 检索 Top1 命中：`transformer-architecture-papers` / `slo-observability-docs` / `cuda-programming-guide-docs`

## 剩余风险

- `raw-sources/` 仍然缺少真实 benchmark 输出、profiler trace、部署 YAML 与运行日志；当前所有 source card 仍是“官方文档/论文 → 概念页”的单向链路。
- `03-templates/concept-note-template.md` 和 `60-frameworks/source-walkthrough-protocol.md` 仍以聚合 `70-sources/official-docs` 作为示例，可以下一轮替换。
- `reliability: high` 页面仍多，二次复核尚未完成；按既定建议继续下调缺乏代码或实验支撑的页面。

## 第 5 轮：模板与 raw-sources 模板

- 新增模板与索引：
  - `03-templates/raw-source-note-template.md`（raw-sources 模板）
  - `00-index/raw-sources-index.md`（raw-sources 落地图）
- 把 `03-templates/concept-note-template.md` 与 `60-frameworks/source-walkthrough-protocol.md` 改为细粒度示例：
  - 不再用占位 wikilink，统一用 `SPECIFIC-CARD` / `PAPER-NAME` 风格，规避 lint 误报。
  - 在模板里写明 `reliability` 三档语义与升级到 `high` 的最小条件。

## 第 6 轮：reliability 复核与边界

- 16 个高价值页从 `reliability: high` 下调到 `reliability: medium`，并新增 `本地证据` / `尚未本地验证的边界` 段：
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
- 升级到 `reliability: high` 的最小条件统一为：补 1 份 `raw-sources/<topic>/<artifact>.md`，含命令、原始输出或 trace，并在 `log.md` / `content-coverage-audit.md` 登记。

## 验证（2026-06-29，本轮）

- `wiki_lint=ok files=100`
- `wiki_index_check=ok pages=100 chunks=729 source_chunks=212`
- BM25 检索：
  - `raw source template` -> Top1 命中 `03-templates/raw-source-note-template.md`
  - `training performance`（按 `reliability=medium` 过滤）-> Top1 命中 `20-training-systems/training-performance-playbook.md`

## 下一轮建议

1. 真正落 `raw-sources/` 至少 2 份：torchrun_ddp_fsdp_metrics.jsonl 与 llm_serving_benchmark.jsonl。
2. 把已被 raw artifact 引用的高价值页（如 `kv-cache-paged-attention`、`vllm-sglang-benchmark-harness`）升级回 `reliability: high`。
3. 继续把 `50-rag-agent-infra/*`、`40-serving-platform/*` 中仍写 `reliability: high` 的页面逐个复核下调。

## 第 7 轮：首批 raw-sources artifact 与 reliability 升级

- 新增首批 raw artifact（local-simulated，结构与脚本可复现）：
  - `raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.md`
  - `raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.md`
- 升级回 `reliability: high` 的页面（含 `sources:` front matter 字段）：
  - `20-training-systems/ddp-fsdp-zero`
  - `30-inference-systems/llm-serving-map`

## 第 8 轮：RAG / serving 平台 reliability 复核

- 新增 source card：`70-sources/key-papers/rag-retrieval-papers.md`。
- 下调到 `reliability: medium` 并迁移到细粒度 source_refs 的页面：
  - `50-rag-agent-infra/embedding-retrieval-agent-infra`
  - `50-rag-agent-infra/evaluation-feedback-loop`
  - `40-serving-platform/gpu-scheduling-kubernetes`
  - `40-serving-platform/serving-platform-map`
  - `40-serving-platform/observability-slo-cost`

## 验证（2026-06-29，本轮）

- `wiki_lint=ok files=101`
- `wiki_index_check=ok pages=101 chunks=750 source_chunks=218`
- BM25 检索：
  - `DDP FSDP smoke`（按 `reliability=high` 过滤）-> Top1 命中 `20-training-systems/ddp-fsdp-zero`，并显示新加的“本地证据”段
  - `rag retrieval`（按 `source_type=paper` 过滤）-> Top1 命中 `70-sources/key-papers/rag-retrieval-papers`

## 当前 reliability 分布

- `reliability: high`：source cards、templates、index 页、2 个被 raw artifact 引用的 concept 页（`ddp-fsdp-zero`、`llm-serving-map`）。
- `reliability: medium`：绝大多数 concept / playbook / experiment / entity 页（已有细粒度 source_refs，但缺 raw artifact）。
- `reliability: low`：尚未出现，留给后续真正结论存疑的页面。

## 下一轮建议（更新）

1. 用真实集群运行覆盖 `raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.md` 与 `raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.md`，复制为新版本，并把对应页面再次升级。
2. 继续落 `raw-sources/serving/`（Helm values、Prometheus rules、Grafana dashboard JSON）和 `raw-sources/rag/`（评测集、召回指标）。
3. 把剩余 `reliability: high` 的 playbook / experiment 页（如 `80-playbooks/benchmark-design`、`90-experiments/experiment-ladder`）也按 raw artifact 标准复核。

## 第 9 轮：serving / RAG raw artifacts

- 新增 2 份 raw artifact（local-simulated）：
  - `raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.md`（Helm values + Prometheus rules）
  - `raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.md`（10 个概念级查询的 Recall@3 + groundedness 评测）
- 升级 4 个页面回 `reliability: high`（含 `sources:` front matter 字段）：
  - `40-serving-platform/gpu-scheduling-kubernetes`
  - `40-serving-platform/observability-slo-cost`
  - `50-rag-agent-infra/embedding-retrieval-agent-infra`
  - `50-rag-agent-infra/evaluation-feedback-loop`

## 第 10 轮：全量 reliability 复核

- 清理 `.ipynb_checkpoints/README-checkpoint.md` 残留文件。
- 下调所有剩余 playbook / experiment / foundation / entity 页面到 `reliability: medium`，共 15 个页面。
- 修复 playbook 中仍指向聚合 `70-sources/official-docs` / `70-sources/key-papers` 的 `source_refs`。
- 为所有下调的 playbook 补 `本地证据` 和 `尚未本地验证的边界` 段。

## 验证（2026-06-29，本轮）

- `wiki_lint=ok files=101`
- `wiki_index_check=ok pages=101 chunks=770 source_chunks=218`
- BM25 检索：
  - `Helm Prometheus`（`reliability=high`）-> Top1 命中 `observability-slo-cost`，显示"本地证据"段
  - `RAG recall groundedness`（`reliability=high`）-> Top1 命中 `rag-retrieval-papers`，Top2/3 命中升级后的 RAG concept 页

## 当前 reliability 分布（最终）

- `reliability: high`（68 页）：
  - 所有 source cards（`70-sources/**`）
  - 所有 templates（`03-templates/**`）
  - 所有 index 页（`00-index/**`）
  - 所有 workflow 页（`02-llm-wiki-workflow/**`）
  - 所有 roadmap 页（`01-roadmap/**`）
  - 所有 maintenance 页（`99-maintenance/**`）
  - README
  - 6 个有 raw artifact 的 concept 页：`ddp-fsdp-zero`、`llm-serving-map`、`gpu-scheduling-kubernetes`、`observability-slo-cost`、`embedding-retrieval-agent-infra`、`evaluation-feedback-loop`
  - 5 个 framework source card 页（`60-frameworks/**`，`type: source`）
- `reliability: medium`（33 页）：
  - 所有 playbook（`80-playbooks/**`，7 页）
  - 所有 experiment（`90-experiments/**`，5 页）
  - 所有 concept 页无 raw artifact（`10-foundations/**`、`20-training-systems/**`、`30-inference-systems/**`、`40-serving-platform/serving-platform-map`、`50-rag-agent-infra` 已升级的除外）
  - 所有 entity 页（`04-entities/**`）
- `reliability: low`：尚未出现。

## 下一轮建议（最终）

1. 用真实集群运行覆盖所有 4 份 local-simulated raw artifact，复制为 real 版本。
2. 为更多 playbook / experiment 落 raw artifact（如 `nccl-network-baseline` 需要 `nvidia-smi topo -m` + `nccl-tests` 输出）。
3. 考虑把 `60-frameworks/**` 的 source card 页也补 raw artifact（如 import 自检、version 输出）。
