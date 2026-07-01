---
title: Source Note Template
type: template
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [template, source]
---

# Source Note Template

```markdown
# Source Title

---
title: Source Title
type: source
topic: training | inference | serving | hardware | ops | rag
component: component-name
level: all
status: active
source_type: official_doc | paper | code | internal_runbook | experiment
source_url: https://example.com
last_checked: YYYY-MM-DD
owner: local
reliability: high | medium | low
tags: []
sources: [../raw-sources/path/to/source.pdf]
---

优先约定：一个 source page 对应一个主来源；只有总导航页才使用 `source_type: curated`。

## Why It Matters

为什么这份资料值得进入 Wiki。

## Key Claims

- Claim 1
- Claim 2

## Limits Or Caveats

- 版本限制：
- 硬件限制：
- 实验范围：

## Links To Concepts

- related concept link

## Follow Up

- 需要验证的问题。
```
