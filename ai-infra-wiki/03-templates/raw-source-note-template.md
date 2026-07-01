---
title: Raw Source Note Template
type: template
topic: wiki
level: all
status: active
last_updated: 2026-06-29
owner: local
reliability: high
tags: [template, raw-sources, evidence]
---

# Raw Source Note Template

> 该模板必须配合 [[../raw-sources/README]] 使用。`raw-sources/` 是不可变证据层，所有 `reliability: high` 的概念页 / playbook / experiment 都应至少引用一份 raw artifact。

## 路径约定

- `raw-sources/training/<topic>-<short-id>.md`
- `raw-sources/inference/<runtime>-<short-id>.md`
- `raw-sources/serving/<platform>-<short-id>.md`
- `raw-sources/hardware/<hw>-<short-id>.md`
- `raw-sources/ops/<tool>-<short-id>.md`
- `raw-sources/benchmarks/<date>-<name>.md`
- `raw-sources/traces/<date>-<trace-name>.md`
- `raw-sources/configs/<date>-<yaml-or-json>.md`

`short-id` 推荐使用 `<框架>-<硬件>-<commit-short>`，例如 `fsdp-h100-2d3a9`。

## 模板

```markdown
---
title: <artifact title>
type: raw
topic: training | inference | serving | hardware | ops | rag
component: <component>
level: beginner | intermediate | advanced
status: active
last_updated: YYYY-MM-DD
owner: local
reliability: high | medium | low
tags: [raw, <topic>, <component>]
artifact:
  kind: benchmark | trace | config | log | dump
  source: local | vendor | community
  collected_at: YYYY-MM-DD
  framework: <framework-name>
  framework_commit: <git-sha>
  hardware: <GPU model, count, network>
  driver: <driver-version>
  cuda: <cuda-version>
  command: <exact command>
  raw_output: <path or inline snippet>
  sha256: <optional checksum>
related_sources:
  - 70-sources/official-docs/<specific-card>
  - 70-sources/key-papers/<specific-paper>
related_concepts:
  - <path/to/concept-page>
related_playbooks:
  - <path/to/playbook>
related_experiments:
  - <path/to/experiment>
---

# <artifact title>

## 来源

- 命令：
- Commit：
- 硬件：
- 软件：
- 关联 source card：
- 关联概念页：

## 原始输入

```text
<command, config, or workload>
```

## 原始输出

```text
<raw output snippet or summary>
```

## 解读

- 结论 1：
- 结论 2：
- 边界：

## 复现步骤

1. ...
2. ...

## 引用建议

- 在 CONCEPT-PAGE 的 “本地证据” 段直接引用本文件。
- 在 [[80-playbooks/benchmark-design]] 中作为对照样例。
```

## 写作约束

- `raw-sources/` 页面尽量简明：聚焦“原始输入 + 原始输出 + 短解读”，避免长篇综述。
- 必须含 `artifact.framework_commit` 与 `artifact.command`，否则不能算作可信证据。
- 解读段只能写可由原始输出直接支持的结论，不允许把“可能性”写成“事实”。
- 一旦 `artifact.sha256` 或 `framework_commit` 变化，复制一份新 raw artifact，而不是原地修改。

## 与 Wiki 其它页的关系

- 概念页 / playbook / experiment 通过 `sources: [.../raw-sources/PATH.md]` 或正文链接引用。
- 同一份 raw artifact 可被多个页面引用，但要明确“哪条结论来自哪条引用”。
- raw artifact 的 `reliability` 字段只是描述“采集时的可信度”，不能反过来抬高概念页的 `reliability`。
