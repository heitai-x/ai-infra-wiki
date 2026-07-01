---
title: Lint And Maintenance
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [lint, maintenance]
---

# Lint And Maintenance

## 自动检查

```bash
python3 scripts/lint_wiki.py ai-infra-wiki
python3 scripts/build_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
python3 scripts/check_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
```

## 每次更新后的检查

- 所有文件都有 YAML front matter。
- `title` 与一级标题一致或语义一致。
- 新概念至少被一个 index 链接。
- source card 有 URL、本地路径或明确来源。
- 性能结论有硬件、模型、框架版本、命令和原始指标。
- 新术语加入 [[00-index/concept-index]] 或相关主题页。
- 新问题加入 [[00-index/question-bank]]。
- 新增 ingest 或结构调整写入 [[00-index/log]]。
- 临时目录如 `.ipynb_checkpoints` 不应进入 lint/index 输入集。

## 每月维护

- 检查官方文档链接是否变更。
- 将过期 API 标为 `stale`。
- 合并重复概念页。
- 将高频问答变成正式 concept 或 playbook。
- 对 RAG 评测集跑回归。

## 质量分级

High：

- 官方文档、论文、代码、可复现实验共同支持。

Medium：

- 官方文档或论文支持，但缺少本地实验。

Low：

- 个人经验、博客、未复现 benchmark、版本不明的结论。

## Wiki 增量指令模板

```text
请把这段资料 ingest 到 AI Infra Wiki：
1. 识别 source_type、topic、component、level、reliability。
2. 新建或更新 source card。
3. 更新相关 concept/playbook/experiment。
4. 更新索引和 question bank。
5. 更新 [[00-index/log]] 与 [[99-maintenance/content-coverage-audit]] 中相关状态。
6. 列出你新增的链接和仍需验证的问题。
```
