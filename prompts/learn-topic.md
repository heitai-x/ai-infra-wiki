# Learn Topic Prompt

## Inputs

- `topic`: 当前学习主题。
- `bundle`: 对应的 progressive-loading bundle。
- `checkpoint`: 当前 study checkpoint，可为空。
- `learner_context`: 已有代码、问题和学习目标。

## Procedure

1. 读取 bundle 的 `bootstrap` 和 `map` 阶段，说明主题在训练或推理系统中的位置。
2. 按当前目标加载 `core` 阶段，先解释输入、输出、状态移动、shape、dtype 和系统代价。
3. 根据 learner context 选择 `practice` 阶段中的代码或实验。
4. 需要更细实现时加载 `deep_dive` 阶段，并关联具体 source card。
5. 使用 `verify` 阶段的 checklist 和 question bank 组织自测。
6. 把已完成项目、证据、开放问题和下一步加载阶段写入 checkpoint。

## Response structure

```markdown
## 学习目标

## 系统位置

## 核心机制

## Shape / dtype / memory

## 代码或实验连接

## 证据与边界

## 自测问题

## Checkpoint 更新
```

## Evidence convention

- 概念解释引用 concept page 和 source card。
- 性能数字引用 experiment 或 raw artifact。
- 推断结论标注推断依据。
- 尚未运行的实验记录为待验证事项，并给出复现命令。
