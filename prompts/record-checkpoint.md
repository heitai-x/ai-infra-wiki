# Record Checkpoint Prompt

## Inputs

- `bundle`: 当前学习 bundle。
- `checklist`: 当前主题 checklist。
- `checkpoint`: 已有 checkpoint 或 `checkpoints/template.yml`。
- `session_result`: 本次完成的阅读、代码、实验和回答。

## Procedure

1. 将本次读取过的 stage 和页面加入 `context`。
2. 将已经满足的 checklist 条目加入 `progress.completed`，并为每项关联 evidence。
3. 将仍在学习的条目加入 `progress.in_progress`。
4. 将需要后续解释或实验的问题加入 `open_questions`。
5. 在 `next` 中记录下一步动作、stage 和 checklist 路径。
6. 更新 `updated_at`，保留已有的创建时间和历史 evidence。

## Output structure

```yaml
checkpoint_id: learning-topic-001
status: in_progress
context:
  loaded_stages: []
  loaded_pages: []
progress:
  completed: []
  in_progress: []
evidence:
  artifacts: []
  experiments: []
  answers: []
open_questions: []
next:
  action: ""
  stage: core
```
