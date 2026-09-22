# Run Experiment Prompt

## Inputs

- `experiment_page`: 实验说明页。
- `bundle`: 当前主题 bundle。
- `checkpoint`: 当前 study checkpoint。
- `environment`: GPU、CPU、driver、CUDA、framework、model 和 precision。

## Procedure

1. 读取实验页中的 question、variables、metrics 和 procedure。
2. 检查环境字段是否能够支撑本次实验，并记录实际环境。
3. 固定 workload，只改变当前实验变量。
4. 保存原始命令、日志、指标和输出文件。
5. 将 observed、inferred、local-simulated 和待验证内容分别记录。
6. 用 checklist 验收实验产物，并把 artifact 路径写入 checkpoint。

## Response structure

```markdown
## 实验问题

## 环境

## 命令

## 原始结果

## 指标对比

## 机制解释

## 结论与适用条件

## 失败尝试与后续实验

## Checkpoint 更新
```

## Evidence convention

- 每个性能结论关联硬件、模型、框架版本、workload 和命令。
- 每个图表关联原始输出路径。
- 模拟数据保留 `local-simulated` 标记。
- 真实运行结果使用新的版本化 artifact 记录。
