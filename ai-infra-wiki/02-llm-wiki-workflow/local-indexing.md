---
title: Local Indexing
type: workflow
topic: rag
component: sqlite-fts5
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [indexing, sqlite, fts5, bm25, rag]
---

# Local Indexing

本 Wiki 已经支持 materialized local index：使用 SQLite FTS5 将 Markdown 页面切成 chunks，并把 front matter metadata 写入 SQLite 表。当前实现是本地 BM25/keyword 检索；向量索引和 hybrid rerank 是后续扩展，不在 v1 中伪装为已实现能力。

## 构建索引

```bash
python3 scripts/build_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
```

输出示例：

```text
wiki_index_built db=/root/autodl-tmp/AI-Infra/wiki-index/ai_infra_wiki.sqlite pages=<current_pages> chunks=<current_chunks>
```

## 搜索

```bash
python3 scripts/search_wiki.py "KV cache" --filter topic=inference --limit 5
python3 scripts/search_wiki.py "FSDP ZeRO" --filter topic=training --limit 5
python3 scripts/search_wiki.py "NCCL hang" --filter component=nccl --limit 5
```

## 索引内容

每个 chunk 保存：

- `rel_path`
- `title`
- `heading`
- `heading_path`
- `content`
- `type`
- `topic`
- `component`
- `level`
- `status`
- `reliability`

## 验收标准

1. `python3 scripts/lint_wiki.py ai-infra-wiki` 通过。
2. `python3 scripts/build_wiki_index.py ...` 成功生成 SQLite DB。
3. 搜索 `KV cache`、`FSDP ZeRO`、`NCCL hang` 能返回相关页面。
4. 搜索结果包含 metadata，可按 `topic/type/component/level/status/reliability` 过滤。
5. `.ai-wiki.yml` 不声称已经实现未落地的向量索引。

## 边界

- 当前是 keyword/BM25 检索，不是 semantic embedding 检索。
- 中文检索依赖 SQLite FTS5 unicode tokenizer 和 fallback 行为，复杂中文语义召回不如向量检索。
- 后续 hybrid search 可在当前 chunk schema 上增加 embedding 表。

## 相关页面

- [[02-llm-wiki-workflow/rag-metadata-schema]]
- [[02-llm-wiki-workflow/lint-and-maintenance]]
- [[50-rag-agent-infra/embedding-retrieval-agent-infra]]
