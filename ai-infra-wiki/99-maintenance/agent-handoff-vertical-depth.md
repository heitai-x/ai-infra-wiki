---
title: Agent Handoff Vertical Depth
type: workflow
topic: wiki
level: all
status: active
last_updated: 2026-09-23
owner: local
reliability: high
tags: [handoff, vertical-depth, transformer, learning, continuation]
---

# Agent Handoff: Vertical Depth

## 交接目标

下一阶段围绕一条完整的模型到系统主线增加内容纵向深度：

```text
safe softmax / activation
  -> RMSNorm
  -> MHA
  -> GQA
  -> KV Cache
  -> Transformer block
  -> prefill / decode
  -> batching / serving
```

目标是让学习者能够从一个具体 Python 文件出发，解释 tensor shape、dtype、计算、显存、kernel、缓存和 serving 指标之间的联系，并且能够用代码、公式和实验结果完成验证。

工作重点是补齐一条可运行、可解释、可验收的学习链。主题数量保持稳定，新增页面围绕已有代码和已有 Wiki 连接。

## 当前仓库状态

当前分支和远端状态：

```text
branch: main
HEAD: 0cb6ef6 docs: refresh project and wiki readmes
origin/main: 0cb6ef6
working tree: clean
```

当前 Wiki 与项目协议：

- 104 个 Wiki Markdown 页面。
- 32 个 source card 页面。
- 7 个 playbook 页面。
- 5 个 experiment 页面。
- 5 个 progressive-loading bundle。
- 5 个主题 Checklist。
- Prompt、工具清单、Checkpoint 模板和本地状态脚本已经存在。
- `wiki_lint=ok files=104`。
- `wiki_index_check=ok pages=104 chunks=806 source_chunks=218`。

先阅读：

- [[00-index/START-HERE]]
- [[01-roadmap/90-day-curriculum]]
- [[01-roadmap/competency-matrix]]
- [[02-llm-wiki-workflow/progressive-loading]]
- [[99-maintenance/current-repository-gaps]]
- [[99-maintenance/optimization-plan]]
- [[99-maintenance/content-coverage-audit]]
- [[00-index/question-bank]]

## 当前代码入口

IDE 当前学习代码位于仓库外层工作区，常用文件包括：

```text
D:\桌面\code\softmax.py
D:\桌面\code\ReLu.py
D:\桌面\code\RMSNorm.py
D:\桌面\code\MHA.py
D:\桌面\code\GQA.py
D:\桌面\code\kvcache.py
```

接手时先逐个读取这些文件，记录当前实现、输入输出 shape、已经完成的部分和待补部分。代码进入仓库前，先确定统一目录和文件命名，再把代码路径写入实验记录或学习 Checkpoint。

当前代码到 Wiki 的连接关系：

| 代码入口 | 对应知识主题 | 需要形成的证据 |
|---|---|---|
| `softmax.py` | masked softmax、数值稳定性、causal mask | 数值测试、全 mask 行、dtype 对比 |
| `ReLu.py` | activation、非线性、计算路径 | forward 结果、shape、激活分布练习 |
| `RMSNorm.py` | normalization、残差路径、dtype | 公式、数值对照、精度说明 |
| `MHA.py` | QKV projection、attention score、head reshape | shape 表、mask 测试、复杂度估算 |
| `GQA.py` | query heads、KV heads、group 映射 | MHA/GQA 对照、KV 显存计算 |
| `kvcache.py` | append、索引、历史 K/V 复用 | prefill/decode 测试、缓存布局说明 |

## 纵向学习主线

### 1. 数值基础

先把 `softmax.py` 作为第一个完整样例，形成以下内容：

- 输入、mask、输出的 shape 和 broadcast 规则；
- `max -> subtract -> exp -> normalize` 的稳定计算路径；
- causal mask 和 padding mask 的差异；
- fully masked row 的输出约定；
- fp32、fp16、bf16 下的数值行为；
- 代码结果和数学公式的逐项对应。

对应页面可以扩展：

```text
ai-infra-wiki/10-foundations/attention-masks-and-softmax.md
```

### 2. Transformer 基础组件

围绕 `RMSNorm.py` 和 `ReLu.py` 补齐组件级说明：

- RMSNorm 的公式、参数 shape、残差连接位置和 dtype；
- ReLU 的输入输出、非线性作用、计算和内存访问；
- Transformer 中 activation、normalization 和 residual 的数据流；
- 后续连接到 SwiGLU、RoPE 和 decoder block 的位置。

建议页面：

```text
ai-infra-wiki/10-foundations/normalization-and-activation.md
```

### 3. MHA 和 GQA

围绕 `MHA.py` 和 `GQA.py` 建立 attention 主线：

- `X -> Q/K/V` projection；
- `[B, T, H * D]` 与 `[B, H, T, D]` 的 reshape；
- `QK^T / sqrt(D)` 的 score shape；
- causal mask 的位置；
- softmax 权重与 `weights @ V`；
- head concat 和 output projection；
- MHA、MQA、GQA 的 query heads / KV heads 关系；
- GQA 对参数、通信和 KV memory 的影响。

建议页面：

```text
ai-infra-wiki/30-inference-systems/mha-gqa-attention.md
```

每个公式都配一个具体参数例子。每个 shape 都配一个可以运行的 tensor test。

### 4. KV Cache

围绕 `kvcache.py` 和现有 [[30-inference-systems/kv-cache-paged-attention]] 深化：

- prefill 阶段的 `Tq`、`Tk` 和完整 prompt；
- decode 阶段的单 token query 和历史 key/value；
- KV append、索引和 batch 内不同长度请求；
- MHA、MQA、GQA 的 KV memory 公式；
- tensor parallel 下 per-rank 与 global 口径；
- contiguous cache 和 paged cache 的数据结构；
- block table、prefix reuse、eviction 和 admission 的连接。

建议页面：

```text
ai-infra-wiki/30-inference-systems/kv-cache-compute-path.md
```

### 5. 从模型代码连接到 Serving

把组件学习连接到现有 serving 页面：

- prefill 计算量与长 prompt；
- decode 的 HBM 读取和 KV 访问；
- continuous batching 的请求加入和退出；
- scheduler 对 batch、queue time、TTFT、TPOT 和 ITL 的影响；
- KV capacity 与 admission control；
- benchmark 命令、raw output 和 Checklist。

已有入口：

- [[30-inference-systems/llm-serving-map]]
- [[30-inference-systems/batching-scheduling]]
- [[80-playbooks/serving-capacity-planning]]
- [[90-experiments/llm-serving-benchmark]]

## 推荐的仓库落点

纵向内容优先补充下面四类页面：

```text
10-foundations/
  attention-masks-and-softmax.md
  normalization-and-activation.md

30-inference-systems/
  mha-gqa-attention.md
  kv-cache-compute-path.md
```

新页面统一使用现有 concept template，并包含：

1. 一句话和系统位置；
2. 输入、输出、shape、dtype 和 layout；
3. 正向数据流和关键公式；
4. 计算、显存、通信和调度代价；
5. 代码路径和可运行例子；
6. 数值、长度、并发和拓扑边界；
7. source card、实验或 raw artifact；
8. 相关问题和下一步页面。

页面内容直接描述机制、条件、结果和适用边界。性能数字关联硬件、模型、框架版本、命令和 workload。

## 实验推进顺序

优先使用 CPU 或单 GPU 可以运行的组件测试，让学生先获得可观察结果：

1. safe softmax：随机输入、causal mask、全 mask row、fp32/bf16。
2. RMSNorm：公式实现与参考实现的数值对照。
3. MHA：小 batch、小 sequence 下的 shape、mask 和输出一致性。
4. GQA：同一组 Q 下比较 MHA 与 GQA 的 KV head 数和显存公式。
5. KV Cache：prefill 写入、decode 追加、历史 K/V 读取。
6. Serving 连接：将 KV cache 参数带入 TTFT、TPOT、吞吐和 admission 讨论。

每个实验保存：

- 研究问题；
- 环境；
- 命令；
- 输入 shape 和 dtype；
- 原始输出；
- 结果解释；
- 未完成问题；
- 对应 Checklist 项和 Checkpoint。

真实硬件结果通过 `raw-sources/` 版本化记录。CPU 或模拟结果标注其运行环境和使用范围。

## Bundle 和 Checklist 交接任务

完成内容页后，新增一个主题包：

```text
packs/transformer-model-components.yml
checklists/transformer-model-components.yml
```

推荐阶段：

```text
bootstrap: START-HERE、competency matrix
map: GPU system map、model architecture cost formulas
core: softmax、normalization、MHA、GQA、KV Cache 页面
practice: 组件测试和 KV Cache 实验
deep_dive: Transformer paper、PagedAttention、runtime source card
verify: question bank、组件 Checklist、代码 evidence
```

Checkpoint 使用现有 `checkpoints/template.yml`，记录已读取页面、完成的组件、代码路径、实验 artifact、开放问题和下一步 stage。

## 交接阶段

### Stage A：代码盘点

- 读取六个 IDE 代码文件；
- 记录函数、输入输出和当前测试；
- 确认代码是否进入仓库以及统一目录；
- 在 checkpoint 中记录代码入口。

### Stage B：概念页面

- 按推荐仓库落点创建四个纵向页面；
- 连接已有 model architecture、KV Cache、serving 和 source card 页面；
- 为每个页面补 shape、dtype、公式和代码路径。

### Stage C：组件实验

- 创建组件级实验脚本或扩展现有 experiment 页面；
- 先验证数值和 shape；
- 再补显存、复杂度和 serving 解释；
- 保存可复现输出。

### Stage D：Bundle 和学习验收

- 创建 `transformer-model-components` bundle；
- 创建对应 Checklist；
- 使用 `load_bundle.py` 验证所有 stage；
- 使用 `check_learning.py` 验证 Checklist；
- 用 `record_checkpoint.py` 记录接手后的学习进度。

### Stage E：维护和交付

运行：

```bash
python scripts/lint_wiki.py ai-infra-wiki
python scripts/build_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
python scripts/check_wiki_index.py --wiki-root ai-infra-wiki --db wiki-index/ai_infra_wiki.sqlite
python scripts/load_bundle.py packs/transformer-model-components.yml --through core
python scripts/check_learning.py --checklist checklists/transformer-model-components.yml
git diff --check
```

最后更新：

- `ai-infra-wiki/99-maintenance/current-repository-gaps.md`；
- `ai-infra-wiki/99-maintenance/content-coverage-audit.md`；
- `ai-infra-wiki/00-index/log.md`；
- 对应 Checkpoint。

## 交付验收标准

完成本次纵向加深后，应当能够：

- 从 `softmax.py` 解释 attention mask 和数值稳定性；
- 从 `RMSNorm.py` 解释 normalization、dtype 和残差路径；
- 从 `MHA.py` 画出 QKV、score、softmax、value aggregation 和 output projection；
- 从 `GQA.py` 计算 query heads、KV heads 和 KV memory；
- 从 `kvcache.py` 解释 prefill、decode、append 和历史读取；
- 将模型组件的 shape、显存和计算连接到 TTFT、TPOT、throughput 和 KV capacity；
- 用至少一个代码测试和一个实验记录支撑结论；
- 用 Checklist 和 Checkpoint 记录完成项、证据和下一步。

## 工作边界

当前阶段把内容深度集中在模型组件和推理系统主线。每页优先形成清晰解释、公式、代码、实验和证据链接，再扩展新的框架或平台主题。Wiki 继续使用 Markdown、YAML、现有 FTS5/BM25 索引和已有维护脚本。

