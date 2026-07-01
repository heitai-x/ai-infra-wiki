---
title: Concept Note Template
type: template
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [template, concept]
---

# Concept Note Template

新建概念页时，请直接复制下面的 front matter + 章节骨架。所有 `source_refs` 必须用具体 source card，而不是聚合导航页。`reliability` 字段的语义：

- `high`：官方文档 + 关键论文 + 本地 raw artifact 都已落地。
- `medium`：官方文档 + 关键论文已落地，但尚未在本地 `raw-sources/` 找到证据。
- `low`：只有一两条来源，或结论还在反复推敲。

```markdown
---
title: Concept Name
type: concept
topic: training | inference | serving | hardware | ops | rag
component: component-name
level: beginner | intermediate | advanced
status: active
last_updated: YYYY-MM-DD
owner: local
reliability: high | medium | low
tags: []
source_refs:
  - 70-sources/official-docs/SPECIFIC-CARD
  - 70-sources/key-papers/SPECIFIC-PAPER
sources:
  - ../raw-sources/TOPIC/ARTIFACT-ID.md
---

## 一句话

这个概念解决什么问题。

## 系统位置

它发生在训练 step / 推理请求 / 平台控制面 / 数据面中的哪里。

## 核心机制

1. 输入是什么。
2. 输出是什么。
3. 状态如何移动。
4. 通信或同步点在哪里。

## 代价与边界

- 显存代价：
- 计算代价：
- 通信代价：
- IO/调度代价：
- 常见失败模式：

## 如何观测

- metrics：
- logs：
- profiler trace：
- benchmark：

## 本地证据

- 来自 `raw-sources/` 的引用（命令、配置、输出、trace）：
- 尚未本地验证的边界：

## 来源

- 70-sources/official-docs/SPECIFIC-CARD
- 70-sources/key-papers/SPECIFIC-PAPER

## 相关页面

- 前置：
- 后续：
- playbook：
```

## 写作约束

- 任何被加进 `reliability: high` 的页面，必须同时满足：
  - 至少 1 个 `70-sources/official-docs/具体` 与 1 个 `70-sources/key-papers/具体`，或 2 个不同具体 source card。
  - 至少 1 条 `raw-sources/` 引用，包含命令、原始输出或 trace 路径。
  - 在 `99-maintenance/acceptance-audit.md` 与 `00-index/log.md` 中登记本地证据。
- 缺本地证据的页面，下调到 `reliability: medium`，并写明“尚未本地验证的边界”。
- source card 选择规则：
  - 论文：使用 `70-sources/key-papers/PAPER-NAME.md`。
  - 官方文档：使用 `70-sources/official-docs/DOC-NAME.md`。
  - 内部 raw artifact：使用 `../raw-sources/TOPIC/ARTIFACT.md`。
- 写新概念前，先查 `99-maintenance/content-coverage-audit.md` 确认不会重复造卡。

## 参考样例

- 写过的范本页：
  - `30-inference-systems/kv-cache-paged-attention.md`（多 source + reliability=high，2026-06-29 复核后下调为 medium）
  - `20-training-systems/training-performance-playbook.md`（可靠性复核后下调为 medium）
