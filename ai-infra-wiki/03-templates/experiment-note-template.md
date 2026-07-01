---
title: Experiment Note Template
type: template
topic: wiki
level: all
status: active
last_updated: 2026-06-13
owner: local
reliability: high
tags: [template, experiment]
---

# Experiment Note Template

```markdown
# Experiment Name

---
title: Experiment Name
type: experiment
topic: training | inference | serving
component: component-name
level: intermediate
status: draft
last_updated: YYYY-MM-DD
owner: local
reliability: medium
tags: []
---

## Question

本实验要回答什么问题。

## Environment

- GPU：
- CPU：
- network：
- driver / CUDA：
- framework commit：
- model：
- precision：

## Commands

```bash
...
```

## Metrics

- throughput：
- latency：
- memory：
- utilization：
- errors：

## Raw Artifacts

- logs：
- traces：
- benchmark outputs：

## Interpretation

结论、边界、下一步。
```
