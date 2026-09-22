---
title: Project Optimization Plan
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-09-23
owner: local
reliability: high
tags: [maintenance, design, optimization, agent-agnostic, checkpoint]
---

# Project Optimization Plan

## 项目定位

本项目定位为 Agent-agnostic 的 AI Infra 学习与实践底座：

```text
Wiki + raw evidence + experiments
  -> progressive context bundles
  -> reusable task prompts
  -> declared tool capabilities
  -> checkpoint / checklist records
```

不同 Agent 负责执行任务，项目负责提供稳定的知识、工具、Prompt 和状态协议。项目不把知识库和某一个 Agent runtime 绑定。

## 设计原则

### Agent 无关

页面、bundle、Prompt、工具清单和 checkpoint 使用通用文本与 YAML。Agent 通过自己的适配层读取这些文件。

### 渐进加载

任务先加载入口和地图，再加载核心页面，需要证据时加载 source card，需要实践时加载实验和 playbook，最后加载 checklist 完成验收。

### 学习优先

实现优先服务阅读、练习、复盘和恢复。文件数量、字段数量和脚本复杂度保持在学生能够理解的范围内。

### 证据优先

概念解释、实验数据和推断结论分别表达。性能结论继续绑定硬件、模型、版本、命令、指标和原始输出。

### 正面直接表达

Wiki 页面直接描述概念、机制、条件、结果和边界。设计文档记录当前实现状态与下一步，不用大量“不是……也不是……”的防御性句式替代主体说明。

### 可恢复

学习进度写入可版本控制的 checkpoint。下一个 Agent 或人类只需读取 checkpoint，就能知道当前目标、已有证据和下一步动作。

## 目标目录

```text
ai-infra-wiki/       知识库与 Wiki 工作流
raw-sources/         原始资料和证据
artifacts/           实验产物
scripts/             可运行工具和实验脚本
packs/               渐进加载 bundle
prompts/             可组合任务 Prompt
tools/               工具能力清单
checklists/          主题验收清单
checkpoints/         学习状态模板和记录
```

## Bundle 方案

每个 bundle 表达一个可以独立学习或执行的目标。核心字段如下：

```yaml
bundle_id: inference.mha-kv-cache
version: 1
title: MHA and KV Cache
goal: Understand attention shapes, decode cache, and KV memory
stages:
  bootstrap: []
  map: []
  core: []
  practice: []
  deep_dive: []
  verify: []
checklist: checklists/inference-mha-kv-cache.yml
```

阶段语义：

- `bootstrap`：项目入口、学习目标和当前能力要求。
- `map`：主题地图和系统位置。
- `core`：完成目标所需的核心概念集合。
- `practice`：代码、实验和 playbook。
- `deep_dive`：论文、源码和更细的实现细节。
- `verify`：Checklist、问题库和已有证据。

bundle 中的路径相对于仓库根目录。loader 只负责按阶段读取并输出内容，不负责自动决定学习路线。

## Prompt Pack 方案

第一批 Prompt 按任务组织：

- `prompts/learn-topic.md`：概念学习和逐步讲解。
- `prompts/run-experiment.md`：实验前置条件、记录和解释。
- 后续增加 `ingest`、`review`、`incident` 等任务 Prompt。

每个 Prompt 都提供：

1. 输入参数；
2. 推荐加载阶段；
3. 证据要求；
4. 输出结构；
5. checkpoint 更新字段。

Prompt 只描述任务协议，具体工具调用由 Agent 自己完成。

## 工具契约方案

`tools/manifest.yml` 只登记项目已有能力：

| 工具 | 作用 | 状态 |
|---|---|---|
| `wiki.search` | 使用 SQLite FTS5/BM25 搜索 Wiki | 已有脚本 |
| `wiki.load_bundle` | 按 stage 输出 bundle 上下文 | 本轮实现 |
| `wiki.lint` | 检查 front matter、链接和孤儿页 | 已有脚本 |
| `wiki.build_index` | 构建本地 SQLite 索引 | 已有脚本 |
| `learning.check` | 汇总 checklist 和 checkpoint 状态 | 已实现 |
| `learning.record_checkpoint` | 创建或更新 study checkpoint | 已实现 |
| `experiment.run` | 执行具体实验脚本 | 由实验页提供命令 |

每项能力记录输入、输出和副作用。当前以本地 CLI 为主，后续可以由不同 Agent 映射为自己的工具调用。

## Checkpoint / Checklist 方案

### Checkpoint

Checkpoint 保存一个学习任务的状态快照：

```yaml
checkpoint_id: learning-mha-kv-cache-001
kind: learning
status: in_progress
bundle: inference.mha-kv-cache
loaded_pages: []
completed: []
evidence: []
open_questions: []
next_action: ""
next_stage: core
```

### Checklist

Checklist 保存可验证的完成标准：

```yaml
checklist_id: inference.mha-kv-cache
items:
  - id: qkv-shape
    criterion: "能够说明 Q/K/V 的 shape"
    status: todo
    evidence: []
```

Checkpoint 记录状态，Checklist 记录标准，实验 artifact 记录证据，三者互相链接。

## 分阶段实施

### Phase 0：文档和边界

产物：

- `current-repository-gaps.md`；
- `optimization-plan.md`；
- 更新 Wiki 入口和维护日志。

验收：文档清楚说明当前基础、缺口、边界和后续实现顺序。

### Phase 1：渐进加载实现

产物：

- `packs/inference-mha-kv-cache.yml`，作为首个可复用主题包；
- `scripts/load_bundle.py`；
- 一个 `inference.mha-kv-cache` bundle。

验收：

```bash
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --stage map
python scripts/load_bundle.py packs/inference-mha-kv-cache.yml --stage core
```

命令输出 bundle 元信息、页面路径和页面正文，便于人类阅读或 Agent 继续处理。

### Phase 2：Prompt、工具和学习状态

产物：

- `prompts/learn-topic.md`；
- `prompts/run-experiment.md`；
- `tools/manifest.yml`；
- `checklists/inference-mha-kv-cache.yml`；
- `checkpoints/template.yml`；
- `scripts/check_learning.py`；
- `scripts/record_checkpoint.py`。

验收：能够从 bundle 进入学习任务，读取 checklist，查看 checkpoint 状态，并得到下一步动作。

### Phase 3：接入现有 Wiki 维护流

产物：

- 更新 `README.md` 和 Wiki workflow 文档；
- 将新协议加入维护日志；
- 修复现有 orphan page；
- 运行 lint 和脚本检查。

验收：现有知识库检索和维护流程继续可用，新增文件都能被人类直接阅读。

### Phase 4：扩展主题

首轮主题包已经按同样的 bundle/checklist 结构加入：

- `inference.mha-kv-cache`；
- `training.ddp-fsdp`；
- `training.nccl-performance`；
- `serving.capacity-planning`；
- `rag.wiki-retrieval`。

每个主题都有对应的页面阶段、Checklist 和共享 Checkpoint 模板。后续新增主题沿用同一协议。

每个主题先形成一个适用的主题 bundle，再逐步补充实验和真实 raw artifact。

## 本轮不做的事情

- 不建立 Agent runtime。
- 不加入远程状态服务。
- 不加入全量 hash、复杂缓存失效和自动同步系统。
- 不要求向量数据库、reranker 或生产级编排才能使用。
- 不把 local-simulated 数据升级成真实实验结论。
- 不为了协议完整而给每个页面增加大量元字段。

## 成功标准

本轮完成后，一个新 Agent 或人类可以：

1. 读取项目入口；
2. 选择一个 bundle；
3. 按 stage 加载当前阶段所需的上下文；
4. 使用通用 Prompt 完成学习或实验任务；
5. 用 Checklist 记录完成状态；
6. 用 Checkpoint 保存下一步；
7. 通过现有 lint、搜索和 Git diff 检查修改。
