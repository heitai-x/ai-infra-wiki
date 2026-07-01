---
title: RAG Metadata Schema
type: workflow
topic: rag
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [rag, metadata, schema]
---

# RAG Metadata Schema

每篇 Markdown 文件必须包含 YAML front matter。最小 schema：

```yaml
---
title: Human Readable Title
type: concept | source | playbook | experiment | index | roadmap | workflow | template | entity | eval-set | hub
topic: training | inference | serving | hardware | ops | rag | wiki | ai-infra
component: fsdp | zero | nccl | vllm | sglang | triton | tensorrt-llm | kubernetes
level: beginner | intermediate | advanced | all
status: draft | active | stale | archived
last_updated: YYYY-MM-DD
owner: local
reliability: high | medium | low
tags: [tag1, tag2]
source_refs: [70-sources/official-docs, 70-sources/key-papers]
sources: [../raw-sources/path/to/file.md]
---
```

## 字段语义

- `type`：决定 RAG 的回答用途。source 用于引用，concept 用于解释，playbook 用于执行。
- `topic`：粗粒度过滤维度。
- `component`：具体组件或机制。
- `level`：学习难度，不代表可信度。
- `status`：`stale` 必须优先复查。
- `reliability`：官方文档和本地验证实验通常为 high；博客、未复现实验通常为 medium 或 low。
- `source_refs`：指向 Wiki 内部的 source card。
- `sources`：指向仓库中的原始资料路径，用于标准 `llm_wiki` 的 source traceability。

## Chunking 策略

- 按二级标题切 chunk，保留 front matter。
- 每个 chunk 保留父标题路径，例如 `Training > FSDP > Communication`。
- 表格可以单独 chunk，但必须保留表头。
- 命令、配置、错误日志不要拆散。
- source card 的 URL 和 last_checked 必须进入每个相关 chunk metadata。

## Retrieval Policy

| 问题类型 | 优先检索 |
|---|---|
| 概念解释 | concept -> source -> question bank |
| API/参数 | source official docs -> framework notes |
| 排障 | playbook -> experiment -> source |
| 性能结论 | experiment -> profiler trace -> benchmark playbook |
| 学习路线 | roadmap -> topic index -> concept index |
