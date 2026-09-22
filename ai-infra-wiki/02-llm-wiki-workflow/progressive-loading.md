---
title: Progressive Loading
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-09-22
owner: local
reliability: high
tags: [progressive-loading, context, bundle, agent-agnostic]
---

# Progressive Loading

本 Wiki 使用 progressive loading 将一个学习目标组织成多个上下文阶段。每个阶段服务一个清晰任务，学习者或 Agent 按目标加载对应页面。

## 阶段模型

```text
bootstrap -> map -> core -> practice -> deep_dive -> verify
```

- `bootstrap`：项目入口、学习目标、能力要求。
- `map`：主题在训练或推理系统中的位置，以及相关资源。
- `core`：完成当前目标需要理解的核心机制、公式、shape、dtype 和系统代价。
- `practice`：代码、实验、benchmark 和 playbook。
- `deep_dive`：论文、源码、kernel 和版本细节。
- `verify`：Checklist、question bank、实验结果和 checkpoint。

## Bundle

Bundle 是一份仓库根目录下的 YAML 文件，例如：

```text
packs/inference-mha-kv-cache.yml
```

Bundle 通过 `stages` 列出每个阶段的页面，通过 `checklist` 和 `checkpoint_template` 连接学习记录。页面路径保持为相对于仓库根目录的稳定路径。

## 加载规则

1. 先读取 bundle 元数据和 `bootstrap`。
2. 根据目标读取 `map`，确认主题边界。
3. 进入 `core`，建立机制、shape、dtype、内存和通信模型。
4. 进入 `practice`，运行代码或实验并保存证据。
5. 使用 `deep_dive` 解释具体框架和源码行为。
6. 在 `verify` 中完成 Checklist，更新 checkpoint。

每次加载以当前学习目标为中心，页面由 bundle 明确选择。现有 SQLite FTS5/BM25 检索继续负责主题搜索，bundle 负责学习顺序和上下文范围。

## 与页面 metadata 的关系

页面 front matter 中的 `level` 表示学习难度。Bundle stage 表示当前任务中的加载顺序，两者各自表达一个维度：

```text
level      -> 学习难度
stage      -> 当前任务的上下文阶段
reliability -> 证据可靠性
```

## 当前主题

首个主题包是 `inference.mha-kv-cache`，连接：

- `softmax.py` 的数值稳定性；
- MHA/GQA 的 Q、K、V shape；
- prefill / decode；
- KV cache 显存公式；
- PagedAttention 和 batching；
- serving benchmark；
- 学习 Checklist 和 study checkpoint。

对应文件：

- `packs/inference-mha-kv-cache.yml`
- `checklists/inference-mha-kv-cache.yml`
- `checkpoints/template.yml`
- `scripts/load_bundle.py`

## 使用命令

```bash
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --stage map
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --stage core --format json
python scripts/check_learning.py --checklist checklists/inference-mha-kv-cache.yml
```

## 学习记录

Checkpoint 保存已经加载的页面、完成的 checklist 项、代码和实验 artifact、开放问题以及下一步 stage。它是跨学习会话和跨 Agent 继续任务的共享状态文件。
