---
title: Ingest Workflow
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [ingest, workflow, llm-wiki]
---

# Ingest Workflow

## 输入类型

- 原始资料目录：优先放入仓库根目录 `raw-sources/`，保持不可变。
- 官方文档：API、配置、限制、版本支持。
- 论文：问题定义、核心机制、实验设置、结论边界。
- 代码：真实行为、默认值、fast path、错误处理。
- 实验：命令、硬件、版本、workload、指标、原始日志。
- 事故复盘：症状、影响面、时间线、根因、修复、预防。

## 处理步骤

1. 识别来源类型和可靠性。
2. 抽取关键事实，不复制长篇原文。
3. 优先归入一个“单一主来源”的 source card；只有导航页才保留聚合式 curated source map。
4. 更新相关 concept note 的“来源”和“实践检查”。
5. 如果产生新问题，加入 [[00-index/question-bank]]。
6. 记录本次 ingest 到 [[00-index/log]]。
7. 如果产生可复现实验，加入 `90-experiments/`。
8. 如果产生排障流程，加入 `80-playbooks/`。

## 摘要格式

每条 ingestion 输出必须包含：

- `source_url` 或本地路径。
- `last_checked`。
- `why_it_matters`。
- `key_claims`。
- `limits_or_caveats`。
- `links_to_concepts`。
- `follow_up_questions`。

## 禁止事项

- 不把未经验证的性能数据写成通用结论。
- 不把旧版本 API 写成当前事实。
- 不把内部经验和官方保证混为一谈。
- 不把无法引用的口头结论放入高可靠性笔记。
