---
title: Raw Sources Index
type: index
topic: ai-infra
component: raw-sources
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [raw-sources, evidence, index]
---

# Raw Sources Index

本页给出 AI-Infra Wiki 中“应当被引用、但尚未落地”的 raw artifact 类型清单。新增 raw artifact 时，请同时更新本表和 `99-maintenance/content-coverage-audit.md`。

> 模板与命名约定见 [[../03-templates/raw-source-note-template]]。

## 应当落地的 artifact

| 主题 | 期望 artifact | 关联 concept | 关联 playbook | 关联 experiment |
|---|---|---|---|---|
| Training | FSDP/ZeRO 显存峰值与 step time 对照表 | [[20-training-systems/ddp-fsdp-zero]] | [[80-playbooks/fsdp-zero-oom-triage]] | [[90-experiments/torchrun-ddp-fsdp-minimal]] |
| Training | TP/PP/CP profile trace | [[20-training-systems/tensor-pipeline-context-parallel]] | [[80-playbooks/profiling-trace-playbook]] | （待补） |
| Training | 数据 pipeline 故障日志 + 复现命令 | [[20-training-systems/data-pipeline-fault-tolerance]] | [[80-playbooks/nccl-hang-triage]] | （待补） |
| Training | NCCL all-reduce 跨节点带宽矩阵 | [[10-foundations/nccl-and-networking]] | [[80-playbooks/nccl-network-baseline]] | （待补） |
| Inference | vLLM/SGLang 启动命令 + TTFT/TPOT JSONL | [[30-inference-systems/llm-serving-map]] | [[80-playbooks/serving-capacity-planning]] | [[90-experiments/vllm-sglang-benchmark-harness]] |
| Inference | Prefix cache 命中率与 TTFT 关系 | [[30-inference-systems/prefix-cache-chunked-prefill-preemption]] | [[80-playbooks/benchmark-design]] | [[90-experiments/llm-serving-benchmark]] |
| Inference | PD 分离部署 YAML + 网络拓扑 | [[30-inference-systems/disaggregated-and-moe-serving]] | [[80-playbooks/serving-production-deployment]] | （待补） |
| Inference | Speculative decoding acceptance rate 日志 | [[30-inference-systems/parallelism-quantization-speculation]] | [[80-playbooks/benchmark-design]] | （待补） |
| Serving | Kubernetes deployment + HPA 配置 | [[40-serving-platform/gpu-scheduling-kubernetes]] | [[80-playbooks/serving-production-deployment]] | （待补） |
| Serving | Prometheus rules + Grafana dashboard JSON | [[40-serving-platform/observability-slo-cost]] | [[80-playbooks/serving-production-deployment]] | （待补） |
| Serving | Rollout / canary 决策记录 | [[40-serving-platform/serving-platform-map]] | [[80-playbooks/serving-production-deployment]] | （待补） |
| Hardware | `nvidia-smi topo -m` 与 `nccl-tests` 输出 | [[10-foundations/gpu-system-map]] | [[80-playbooks/nccl-network-baseline]] | （待补） |
| RAG/Agent | 召回 / 排序评测集与指标 | [[50-rag-agent-infra/embedding-retrieval-agent-infra]] | （待补） | （待补） |

## 状态

- 当前已落地：4 份（local-simulated）。
  - `raw-sources/training/torchrun-ddp-fsdp-smoke-2026-06-29.md`
  - `raw-sources/inference/llm-serving-benchmark-smoke-2026-06-29.md`
  - `raw-sources/serving/llm-serving-k8s-helm-prometheus-2026-06-29.md`
  - `raw-sources/rag/rag-retrieval-eval-smoke-2026-06-29.md`
- 下一轮目标：用真实集群运行覆盖上述 4 份；新增 `raw-sources/hardware/`（`nvidia-smi topo -m`、`nccl-tests`）和 `raw-sources/traces/`（torch profiler、Nsight Systems）。

## 维护规则

- 新增 raw artifact：
  1. 在 `raw-sources/<topic>/` 下按 `raw-source-note-template` 创建。
  2. 在本表登记“已落地”。
  3. 在关联概念页的 `sources` / `本地证据` 段添加引用。
  4. 在 `00-index/log.md` 与 `99-maintenance/content-coverage-audit.md` 同步登记。
- 删除 raw artifact 时不能原地删除，复制为 `*-archived.md` 后再保留 commit 链接。
