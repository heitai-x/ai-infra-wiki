# AI Infra Learning Workspace

这是一个面向 AI Infra 训练、推理、Serving 和 RAG 的学习与实践工作区。项目把 Wiki、原始证据、实验脚本、渐进式上下文 bundle、任务 Prompt、Checklist 和学习 Checkpoint 组织成一套可以被不同 Agent 复用的学习底座。

项目保持 Agent-agnostic：Agent 负责执行学习、实验、检索和复盘任务；仓库提供稳定的知识、工具和状态协议。

## 从这里开始

- [AI Infra LLM Wiki](ai-infra-wiki/README.md)：概念、来源、实验、playbook 和维护规范。
- [Start Here](ai-infra-wiki/00-index/START-HERE.md)：学习入口和第一轮阅读顺序。
- [Progressive Loading](ai-infra-wiki/02-llm-wiki-workflow/progressive-loading.md)：bundle 和上下文阶段说明。
- [Learning Bundles](packs/README.md)：按主题加载学习内容。
- [Project Gaps](ai-infra-wiki/99-maintenance/current-repository-gaps.md)：当前仓库缺口和已完成修复。
- [Optimization Plan](ai-infra-wiki/99-maintenance/optimization-plan.md)：项目协议和推进方案。
- [Agent Handoff](ai-infra-wiki/99-maintenance/agent-handoff-vertical-depth.md)：下一阶段纵向加深的工作说明。

## 项目协议

```text
ai-infra-wiki/       Markdown / Obsidian 风格知识库
raw-sources/         原始资料、实验记录和证据
artifacts/           实验产物
scripts/             索引、搜索、lint、bundle 和 checkpoint 工具
packs/               渐进加载 bundle
prompts/             学习、实验和记录 Prompt
tools/               工具能力清单
checklists/          主题学习验收标准
checkpoints/         学习状态模板和记录
```

## 快速使用

列出一个主题的加载阶段：

```bash
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --list-stages
```

加载从入口到核心内容的连续上下文：

```bash
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --through core
```

查看学习 Checklist 和 Checkpoint：

```bash
python scripts/check_learning.py \
  --checklist checklists/inference-mha-kv-cache.yml \
  --checkpoint checkpoints/template.yml
```

记录一个学习会话：

```bash
python scripts/record_checkpoint.py \
  --output checkpoints/session.yml \
  --bundle inference.mha-kv-cache \
  --stage core \
  --action "Continue the core lesson"
```

构建并检查 Wiki 索引：

```bash
python scripts/lint_wiki.py ai-infra-wiki
python scripts/build_wiki_index.py \
  --wiki-root ai-infra-wiki \
  --db wiki-index/ai_infra_wiki.sqlite
python scripts/check_wiki_index.py \
  --wiki-root ai-infra-wiki \
  --db wiki-index/ai_infra_wiki.sqlite
```

## 当前学习主题

- `inference.mha-kv-cache`：MHA、GQA、safe softmax、prefill/decode、KV Cache 和 PagedAttention。
- `inference.transformer-model-components`：safe softmax、RMSNorm、MHA、GQA、KV Cache 和组件实验。
- `training.ddp-fsdp`：DDP、FSDP、ZeRO、显存账本和训练通信。
- `training.nccl-performance`：NCCL collective、GPU 拓扑、通信和 profiler。
- `serving.capacity-planning`：请求 workload、KV capacity、调度、SLO 和部署。
- `rag.wiki-retrieval`：ingestion、metadata、BM25、引用和检索评测。

每个主题都按照下面的路径组织：

```text
bootstrap -> map -> core -> practice -> deep_dive -> verify
```

学习记录遵循：

```text
读取概念
  -> 加载来源
  -> 运行代码或实验
  -> 保存 evidence
  -> 完成 checklist
  -> 更新 checkpoint
```

## 典型学习路线

- GPU、CUDA、NCCL、内存和 Roofline。
- DDP、FSDP、ZeRO、TP、PP、CP 和 EP。
- LLM serving、KV Cache、batching、调度和容量规划。
- profiler、kernel timeline、通信 overlap 和故障排查。
- Kubernetes GPU scheduling、SLO、可观测性和成本。
- RAG ingestion、metadata、检索、引用和评测。

## 运行支持

仓库包含静态代码结构工具、AI Infra 学习 skills、实验脚本和本地 SQLite FTS5/BM25 索引。真实 GPU、serving server、NCCL 和 Kubernetes 实验需要相应运行环境；教学样例会明确标记 `local-simulated`，真实结果以新的 raw artifact 记录。
